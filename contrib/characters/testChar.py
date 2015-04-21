#!/usr/bin/env python

# script to create a test character

import logging

from cthulhu.char import character, json_import
from cthulhu.roll import roll

logging.basicConfig(format='%(message)s', level=logging.INFO)


newChar = character('Tyler')
for characteristic in ['STR', 'DEX', 'APP', 'CON', 'POW']:
    newChar.setCharacteristic(characteristic, roll('3d6*5'))

for characteristic in ['INT', 'SIZ', 'EDU']:
    newChar.setCharacteristic(characteristic, roll('2d6+6*5'))

newChar.luck = roll('2d6+6*5')
newChar.setSecondary()

newChar.setSkill('Spot Hidden', 70)
newChar.setSkill('Fighting (Brawl)', 55)
newChar.setSkill('Firearms (handgun)', 55)
newChar.setSkill('Sneak', 40)
newChar.setSkill('Listen', 55)
newChar.setSkill('Sleight of Hand', 25)
newChar.addWeapon('Unarmed', '1d3', 'Fighting (Brawl)', 'non-impaling', db=True)
#newChar.addWeapon('Machete', '1d8', 'Fighting (Brawl)', 'penetrating', db=True)
newChar.addWeapon('.38 Automatic', '1d10', 'Firearms (handgun)', 'firearm', db=False, mal=99, ammo=8, numAttacks=3)

myjson = newChar.jsondump()
jsonChar = json_import(myjson)
print myjson
