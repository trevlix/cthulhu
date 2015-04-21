#!/usr/bin/env python

import logging
import jsonpickle

from cthulhu.skill import skill
from cthulhu.weapon import weapon, firearm
from cthulhu.roll import result

class being(object):
    def __init__(self, name, HP=0, era = 'Classic'):
        self.name = name
        self.maxHP = self.HP = HP
        self.era = era
        self.db = 0
        self.build = 0
        self.mov = 8
        self.luck = 0
        self.san = self.maxSan = 0
        self.mp = 0
        self.numAttacks = 1
        self.armor = 0
        self.currentWeapon = None

        self.status = dict()
        self.status['fightback'] = True
        self.characteristics = dict()
        self.skills = dict()
        self.weapons = dict()

    def setCharacteristic(self, characteristic, value):
        self.characteristics[characteristic] = skill(characteristic, value)

    def setSkill(self, skillName, value):
        self.skills[skillName] = skill(skillName, value)

    def addWeapon(self, weaponName, skillName, damage, weaponType='non-impaling', db=False, mal=101, ammo=0, numAttacks=1):
        if weaponType != 'firearm':
            self.weapons[weaponName] = weapon(weaponName, skillName, damage, weaponType=weaponType,  db=db, mal=mal)
        else:
            self.weapons[weaponName] = firearm(weaponName, skillName, damage, weaponType=weaponType,  db=db, mal=mal, ammo=ammo, numAttacks=numAttacks)

    def setDodge(self, value=0):
        try:
            self.skills['Dodge'] = skill('Dodge' , self.characteristics['DEX'].half)
        except:
            log.error("ERROR: Unable to set Dodge.")

    def outNumbered(self):
        """ returns True if they have already responded """
        try:
            if self.status['combat_response'] > self.numAttacks:
                return True
        except KeyError:
            self.status['combat_response'] = 0
            return False

        return False

    def jsondump(self):
        return jsonpickle.encode(self)

    def initiative_value(self):
        """ Return the initiative value for this character based on their current weapon. """
        if self.currentWeapon is not None and self.currentWeapon.weaponType == 'firearm':
            init_value = self.characteristics['DEX'].value + 50
        else:
            init_value = self.characteristics['DEX'].value

        logging.debug("Combat: {} init value is {}".format(self.name, init_value))

        return init_value

    def setCurrentWeapon(self):
        """ Ask the user what their current weapon should be. """
        chosen = False
        wlist = list(self.weapons)
        if len(wlist) == 1:
            weapon = 0
            chosen = True

        while chosen is False:

            for w in wlist:
                print '{}. {} {}'.format(wlist.index(w)+1, w, self.weapons[w].damage)
            weapon = raw_input('\n{} must choose their weapon: '.format(self.name))

            try:
                weapon = int(weapon)-1
                if 0 <= weapon <= len(wlist)-1:
                    chosen = True
            except:
                pass

        self.currentWeapon = self.weapons[wlist[weapon]]

class character(being):
    def __init__(self, name=''):
        being.__init__(self, name)
        for characteristic in ['STR', 'DEX', 'APP', 'CON', 'POW', 'INT', 'SIZ', 'EDU']:
            self.setCharacteristic(characteristic, 0)

        # only characters should check for major wounds. Is this true? Need to verify.
        self.majorWound = 0

        self.addWeapon('Unarmed',  '1d3', 'Fighting (Brawl)', db=True)  # ADD DAMAGE BONUS

    def setSecondary(self):
        self.setHP()
        self.setSAN()
        self.setBuildAndDB()
        self.setMOV()
        self.setMP()
        self.setDodge()

    def setHP(self):
        """ Sets the maximum HP and current HP based on CON and SIZ.
             Modify self.HP directly if you need to subtract or add HP.
        """
        try:
            self.maxHP = (self.characteristics['CON'].value + self.characteristics['SIZ'].value) / 10
            self.HP = self.maxHP
        except:
            logging.error("ERROR: Missing CON or SIZ. Please add those before setting HP.")

    def setBuildAndDB(self):
        """ Sets the initial damage bonus and build based on STR and SIZ. """
        try:
            combined = self.characteristics['STR'].value + self.characteristics['SIZ'].value
        except:
            logging.error("ERROR: Missing STR or SIZ. Please add before setting up DB and build.")
            return

        if 2 <= combined <= 64:
            self.db = self.build = -2
        elif 65 <= combined <= 84:
            self.db = self.build = -1
        elif 125 <= combined <= 164:
            self.db = '1d4'
            self.build = 1
        elif combined >= 165:
            self.db = '1d6'
            self.build = 2

    def setMOV(self):
        """ Sets MOV based on DEX, STR and SIZ. """
        try:
            if self.characteristics['STR'].value < self.characteristics['SIZ'].value and \
               self.characteristics['DEX'].value < self.characteristics['SIZ'].value:
                   self.mov = 7
            elif self.characteristics['STR'].value > self.characteristics['SIZ'].value and \
                   self.characteristics['DEX'].value > self.characteristics['SIZ'].value:
                   self.mov = 9
        except:
            logging.error('ERROR: Cannot set MOV. Missing STR, DEX or SIZ.')

    def setSAN(self):
        """ Sets the initial sanity. """
        try:
            self.san = self.characteristics['POW'].value
            self.maxSan = self.san
        except:
            logging.error('ERROR: Need POW before we can set SAN.')

    def setMP(self):
        """ Sets the inital POW."""
        try:
            self.mp = self.characteristics['POW'].fifth
        except:
            logging.error('ERROR: Need POW before we can set MP.')

    def checkMajorWound(self, damage):
        # check for major wound
        if self.HP > 0 and damage >= (self.maxHP / 2):
            logging.info('DAMAGE: {} suffered a major wound.'.format(self.name))
            # make a CON check
            if self.characteristics['CON'].check() < result.normal:
                logging.info('DAMAGE: {} failed their CON check - falling unconscious and will die.'.format(self.name))
                self.HP = 0


    def __str__(self):
        outstr = "Name: {}\n".format(self.name)
        outstr = outstr + "Era: {}\n".format(self.era)
        outstr = outstr +  "HP: {}\tMax HP: {}\tMP: {}\n".format(self.HP, self.maxHP, self.mp)
        outstr = outstr +  "San: {}\tMax SAN: {}\n".format(self.san, self.maxSan)
        outstr = outstr +  'DB: {}\tBuild: {}\tMOV: {}\n'.format(self.db, self.build, self.mov)
        outstr = outstr +  'Luck: {}\n\n'.format(self.luck)
        outstr = outstr +  "Characteristics:\n"
        for characteristic in self.characteristics:
            outstr = outstr +  str(self.characteristics[characteristic]) + '\n'

        outstr = outstr + "\nSkills:\n"
        for skills in sorted(self.skills):
            outstr = outstr +  str(self.skills[skills]) + '\n'

        outstr = outstr + "\nWeapons:\n"
        for weapon in sorted(self.weapons):
            outstr = outstr +  str(self.weapons[weapon]) + '\n'

        return outstr

class monster(being):
    def __init__(self, name=''):
        being.__init__(self, name)
        for characteristic in ['STR', 'DEX', 'APP', 'CON', 'POW', 'INT', 'SIZ', 'EDU']:
            self.setCharacteristic(characteristic, 0)

        self.sanLoss = '0/0'
        self.majorWound = 0

    def __str__(self):
        outstr = "Name: {}\n".format(self.name)
        outstr = outstr +  "HP: {}\tMax HP: {}\tMP: {}\n".format(self.HP, self.maxHP, self.mp)
        outstr = outstr +  'DB: {}\tBuild: {}\tMOV: {}\n'.format(self.db, self.build, self.mov)
        outstr = outstr + 'Armor: {}\tNumber of Attacks: {}\tSanity Loss: {}\n\n'.format(self.armor, self.numAttacks, self.sanLoss)
        outstr = outstr +  "Characteristics:\n"
        for characteristic in self.characteristics:
            if self.characteristics[characteristic].value > 0:
                outstr = outstr +  str(self.characteristics[characteristic]) + '\n'

        outstr = outstr + "\nSkills:\n"
        for skills in sorted(self.skills):
            outstr = outstr +  str(self.skills[skills]) + '\n'

        outstr = outstr + "\nWeapons:\n"
        for weapon in sorted(self.weapons):
            outstr = outstr +  str(self.weapons[weapon]) + '\n'
        return outstr

def json_import(myjson):
    """ Imports the char.jsondump() version of a char and returns the new object. """
    return jsonpickle.decode(myjson)


