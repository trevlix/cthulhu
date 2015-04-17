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
newChar.setSkill('Fighting (Shotgun)', 55)
newChar.setSkill('Sneak', 40)
newChar.setSkill('Listen', 55)
newChar.setSkill('Sleight of Hand', 25)

myjson = newChar.jsondump()
jsonChar = json_import(myjson)
print newChar
