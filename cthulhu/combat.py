#!/usr/bin/env python

import logging
import cthulhu.roll as roll

# Code to simulate combat

def initiative(combatants):
    """ Determines the order of combat based on DEX of combatants.

         combatants: iterable containing character or monster classes
    """
    return sorted([ fighter for fighter in combatants ], key=lambda x: x.initiative_value(), reverse=True)

def extremeDamage(dealer):
    """ Returns the result from an extreme damage roll."""
    logging.info('DAMAGE: EXTREME DAMAGE!')
    weapon = dealer.currentWeapon
    dbDamage = int(str(dealer.db).split('d')[-1])

    if weapon.weaponType == 'non-impaling':
        # max damage
        damage = weapon.maxDamage() + dbDamage
        logging.info('DAMAGE: Max Damage given ({}) + db ({})'.format(weapon.maxDamage(), dbDamage))
    elif weapon.weaponType == 'penetrating':
        damage = weapon.maxDamage() + int(str(dealer.db).split('d')[-1]) + weapon.rollDamage()
        logging.info('DAMAGE: Max Damage given ({}) + db ({}) plus rolling damage ({})'.format(weapon.maxDamage(), dbDamage, damage-(weapon.maxDamage()+dbDamage)))
    elif weapon.weaponType == 'firearm':
        damage = weapon.maxDamage() + weapon.rollDamage()
        logging.info('DAMAGE: Max Damage given ({}) plus rolling damage ({})'.format(weapon.maxDamage(), damage-weapon.maxDamage()))
    else:
        # unknown type
        logging.error('ERROR: Unknown weapon type: {}'.format(weapon.weaponType))

    return damage

def dealDamage(dealer, recipient, attack_result=roll.result.normal):
    """ Deals damage from the dealer to the recipient using the weapon. """

    if attack_result >= roll.result.extreme:
        # max damage
        damage = extremeDamage(dealer)
    else:
        # normal damage
        damage = dealer.currentWeapon.rollDamage()
        if dealer.currentWeapon.db is True:
            logging.debug('\tDAMAGE: Adding damage bonus.')
            damage = damage + roll.roll(str(dealer.db))

    logging.info('DAMAGE: {} rolled {} for damage.'.format(dealer.name, damage))

    damage = damage - recipient.armor
    if damage < 0:
        damage = 0

    recipient.HP = recipient.HP - damage
    logging.info('DAMAGE: {} takes {} damage from {}\'s {}'.format(recipient.name, damage, dealer.name, dealer.currentWeapon.name))
    if recipient.armor > 0:
        logging.debug('\tDAMAGE: Damage was reduced by {} due to armor.'.format(recipient.armor))
    logging.info('DAMAGE: {} is down to {} HP.'.format(recipient.name, recipient.HP))

    # check for major wound
    try:
        recipient.checkMajorWound(damage)
    except:
        # recipient doesn't have to check for a major wound, do nothing
        pass

def endCombat(teamA, teamB):
    """ Return true if one team completely is out of combat. """
    teamAdone = [ person.HP <= 0 for person in teamA ]
    teamBdone = [ person.HP <= 0 for person in teamB ]

    if False in teamAdone and False in teamBdone:
        # someone is still alive, keep going
        return False
    return True

def chooseOpponent(attacker, opponents):
    """ Choose your opponent on the other team.
        Returns either the opponent or None if no one is alive.
    """
    chosen = False
    if len(opponents) == 0:
        # no opponents are left
        logging.info('Combat: There is no one left to fight!')
        return None
    elif len(opponents) == 1:
        # only 1 opponent, auto choose
        return opponents[0]

    while chosen is False:

        for i in range(len(opponents)):
            print '{}. {}'.format(i+1, opponents[i].name)
            i = i + 1

        opp = raw_input('\n{} must choose their opponent: '.format(attacker.name))
        try:
            opp = int(opp)-1
            if 0 <= opp <= len(opponents)-1:
                chosen = True
        except:
            pass

    return opponents[opp]

def removeCombatant(fighter, teamA, teamB):
    """ Removes a combatant from the list of available fighters. """
    if fighter in teamA:
        del teamA[teamA.index(fighter):teamA.index(fighter)+1]
    else:
        del teamB[teamB.index(fighter):teamB.index(fighter)+1]

def rangedAttack(attacker, defender, range='normal'):
    """ Attack using ranged weapons or firearms.
        Range can be: normal, long, extreme, or close (ie point blank)
        THIS NEEDS CHANGED TO CALCULATE RANGE BASED ON DISTANCE
    """
    # make rolls
    bonus=0
    penalty=0
    success=False

    attack_skill = attacker.currentWeapon.skill
    logging.info('Combat: {} is shooting at {} with {} ({})'.format(attacker.name, defender.name, attacker.currentWeapon.name, attack_skill))
    if range == 'close':
        bonus = 1
    if attacker.numAttacks > 1 and attacker.currentWeapon.weaponType == 'firearm':
        # firearms that are firing multiple shots / round gain a penalty die
        penalty = 1

    attack_result = attacker.skills[attack_skill].check(bonus=bonus, penalty=penalty)

    if (range == 'normal' or range == 'close') and attack_result >= roll.result.normal:
        success = True
    elif range == 'long' and attack_result >= roll.result.hard:
        success = True
    elif range == 'extreme' and attack_result >= roll.result.extreme:
        success = True

    if success is True:
        logging.info('Combat: {} hit!'.format(attacker.name))
        dealDamage(dealer=attacker, recipient=defender, attack_result=attack_result)
    else:
        logging.info('Combat: Miss!')

def meleeAttack(attacker, defender, fight_back=True):
    """ A melee attack using weapons or unarmed combat. """

    # make rolls
    attack_skill = attacker.currentWeapon.skill
    logging.info('Combat: {} is attacking with {} ({})'.format(attacker.name, attacker.currentWeapon.name, attack_skill))
    bonus = 0
    penalty=0

    # keep track of how many times the defender has responded back
    defender.status['combat_response'] = defender.status['combat_response'] + 1
    if defender.outNumbered() is True:
        logging.info('Combat: {} is outnumbered, {} gets bonus die.'.format(defender.name, attacker.name))
        bonus = bonus + 1

    attack_result = attacker.skills[attack_skill].check(bonus=bonus, penalty=penalty)

    # choose if defender will attack back or dodge
    if fight_back is True:
        if defender.currentWeapon.weaponType == 'firearm':
            # cannot fight back w a firearm, choose unarmed
            try:
                logging.info("Combat: {} cannot fight back with firearm. Using hands instead.".format(defender.name))
                defend_weapon = defender.weapons['Unarmed']
                defend_skill = defender.weapons['Unarmed'].skill
            except err:
                print "problem"
                # doesn't have unarmed skill...not sure what to do here
                pass
        else:
            # not a firearm, using the current skill.
            defend_weapon = defender.currentWeapon
            defend_skill = defender.currentWeapon.skill
        logging.info('Combat: {} is fighting back with {} ({})'.format(defender.name, defend_weapon.name, defend_skill))
    else:
        defend_weapon = 'Dodge'
        defend_skill = 'Dodge'

    defend_result = defender.skills[defend_skill].check()

    # determine results
    if attack_result > defend_result and attack_result >= roll.result.normal:
        # attacker succeeds and deals damage
        logging.info('Combat: {} scored a hit!'.format(attacker.name))
        dealDamage(dealer=attacker, recipient=defender,  attack_result=attack_result)
    elif defend_result > attack_result and defend_result >= roll.result.normal:
        if fight_back is True:
            # attacker misses, defender succeeds and deals damage
            logging.info('Combat: {} missed, but {} scored a hit fighting back!'.format(attacker.name, defender.name))
            dealDamage(dealer=defender, recipient=attacker)
        else:
            # attacler misses
            logging.info('Combat: {} successfully dodged!'.format(defender.name))
    elif defend_result == attack_result and defend_result >= roll.result.normal:
        if fight_back is True:
            # same result, both success, attacker does damage
            logging.info('Combat: Its a tie that goes to the attacker. {} deals damage!'.format(attacker.name))
            dealDamage(dealer=attacker, recipient=defender,  attack_result=attack_result)
        else:
            # same result, both success, defender dodges
            logging.info('Combat: {} successfully dodged! No damage!'.format(defender.name))
    else:
        logging.info('Combat: Both miss!')

    return

def setUpRound(fighter, my_team, opp_team):
    """ Helper function that sets up the current fighter for their round.
         Returns who the opponent is.
    """

    fighter.status['combat_response'] = 0
    if fighter.HP <= 0:
        # they are dead, remove them
        removeCombatant(fighter, my_team, opp_team)
    else:
        opponent = chooseOpponent(fighter, opp_team)
        fighter.setCurrentWeapon()
        try:
            # if the fighter's weapon has more than 1 attack (eg firearm), set it up
            fighter.numAttacks = fighter.currentWeapon.numAttacks
        except:
            pass

        # add in choice to fight back or dodge
        fighter.status['fightback'] = True

    return opponent

def combat(teamA, teamB):
    """ Runs through the rounds of combat.
         The two parameters it takes are the two "teams" of the combatants.
    """

    round = 1
    deaths = list()

    # start combat here
    while endCombat(teamA, teamB) is False:

        # dict that keeps track of who is fighting who
        opponents = dict()

        # choose weapons for each attacker and whom is attacking whom
        for fighter in teamA:
            opponents[fighter] = setUpRound(fighter, teamA, teamB)

        for fighter in teamB:
            opponents[fighter] = setUpRound(fighter, teamB, teamA)

        # set initiative
        order = initiative(teamA + teamB)

        # go through order
        logging.info('*'*60+'\nCombat round {}'.format(round))

        for fighter in order:
            # make sure fighter is still alive
            if fighter.HP <= 0:
                # nope - skip
                continue

            # set defender
            defender = opponents[fighter]

            if defender.HP <= 0:
                # defender is dead, choose another
                logging.info('Combat: {} is already dead. Choose another.'.format(defender.name))
                if fighter in teamA:
                    defender = chooseOpponent(fighter, teamB)
                else:
                    defender = chooseOpponent(fighter, teamA)

                if defender is None:
                    # no one left to fight, likely over
                    break

            logging.info('Combat: {} is attacking {}!'.format(fighter.name, defender.name))

            for i in range(fighter.numAttacks):

                if fighter.currentWeapon.weaponType != 'firearm':
                    meleeAttack(attacker=fighter, defender=defender, fight_back=defender.status['fightback'])
                else:
                    rangedAttack(attacker=fighter, defender=defender)
                logging.info('')

                if fighter.HP <= 0 or defender.HP <= 0:
                    # someone has died - time to stop
                    break

            # if someone is dead, print it out
            if (fighter.HP <= 0):
                logging.info('DEATH: {} has died.'.format(fighter.name))
                removeCombatant(fighter, teamA, teamB)
                deaths.append((defender, fighter, round))
                continue
            elif (defender.HP <= 0):
                logging.info('DEATH: {} has died.'.format(defender.name))
                removeCombatant(defender, teamA, teamB)
                deaths.append((fighter, defender, round))
                continue
        round += 1



    logging.info('\n'+'*'*40+'\nCombat statistics\n'+'*'*40+'\n')
    logging.info('Combat lasted {} rounds.\n'.format(round-1))
    logging.info('Deaths:')
    for kill in deaths:
        logging.info('{} killed {} in round {}'.format(kill[0].name, kill[1].name, kill[2]))

    logging.info('')


