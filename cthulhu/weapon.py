#!/usr/bin/env python

import logging
from cthulhu.roll import roll

class weapon(object):
    def __init__(self, name='', damage='0', skill='', weaponType='non-impaling', db=False, mal=100):
        self.name = name
        self.damage = damage
        self.mal = mal
        self.skill = skill
        # non-impaling, firearm or penetrating weapon
        self.weaponType = weaponType
        self.db = db # does this need to use the damage bonus?

    def rollDamage(self):
        hitDam = roll(self.damage)
        logging.debug('DAMAGE: Weapon rolled {} damage'.format(hitDam))
        return hitDam

    def maxDamage(self):
        mDam = roll(self.damage, max=True)
        return mDam

    def __str__(self):
        outstr = "Name: {:15}\tSkill: {:15}\tDamage: {}\tType: {}".format(self.name, self.skill, self.damage, self.weaponType)
        if self.db is True:
            outstr = outstr + '{}'.format('+db')
        if self.mal <= 100:
            outstr = outstr + "\tMal #: {}\n".format(self.mal)

        return outstr

class firearm(weapon):
    def __init__(self, name='', damage='0', skill='', weaponType='firearm', db=False, mal=100, ammo=0, numAttacks=1):
        weapon.__init__(self, name=name, damage=damage, skill=skill, weaponType='firearm', db=False, mal=mal)
        self.ammo = ammo
        self.numAttacks = numAttacks

    def rollDamage(self):
        if self.ammo > 0:
            hitDam = roll(self.damage)
            self.ammo = self.ammo - 1
            logging.debug('DAMAGE: Weapon rolled {} damage'.format(hitDam))
        else:
            logging.info('Combat: CLICK! {} is out of ammo! Choose a different weapon next time.'.format(self.name))
            hitDam = 0
        return hitDam
