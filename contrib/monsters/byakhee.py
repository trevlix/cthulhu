#!/usr/bin/env python

# Test script to create a Byakhee monster

import logging

from cthulhu.char import monster, json_import
from cthulhu.roll import roll
from cthulhu.weapon import weapon

logging.basicConfig(format='%(message)s', level=logging.INFO)

byakhee = monster('Byakhee')

for characteristic in ['STR', 'SIZ']:
    byakhee.setCharacteristic(characteristic, roll('5d6*5'))

for characteristic in ['CON', 'INT', 'POW']:
    byakhee.setCharacteristic(characteristic, roll('3d6*5'))

byakhee.setCharacteristic('DEX', roll('3d6+3*5'))
byakhee.setDodge()

byakhee.HP = 14
byakhee.maxHP = 14
byakhee.db = '1d6'
byakhee.build = 2
byakhee.mp = 10
byakhee.sanLoss = '1/1d6'
byakhee.armor = 2

byakhee.setSkill('Listen', 50)
byakhee.setSkill('Spot Hidden', 55)
byakhee.setSkill('Fighting', 55)

byakhee.addWeapon('Fighting', '1d6+1d6', 'Fighting')

myjson = byakhee.jsondump()
newMonster = json_import(myjson)
print byakhee

