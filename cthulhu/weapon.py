#!/usr/bin/env python

from cthulhu.roll import roll

class weapon(object):
    def __init__(self, name='', damage='0', skill='', mal=100):
        self.name = name
        self.damage = damage
        self.mal = mal
        self.skill = skill

    def damage(self):
        return roll(self.damage)

    def __str__(self):
        return "Name: {:15}\tSkill: {:15}\tDamage: {:10}\tMal #: {}\n".format(self.name, self.skill, self.damage, self.mal)
