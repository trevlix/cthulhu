#!/usr/bin/env python

import logging
import cthulhu.combat as combat
from cthulhu.char import monster, character, json_import

mychar = json_import(open('char.json').read())
mychar2 = json_import(open('char2.json').read())
mychar3 = json_import(open('char3.json').read())
byakhee = json_import(open('byakhee.json').read())
byakhee2 = json_import(open('byakhee2.json').read())

logging.basicConfig(format='%(message)s', level=logging.INFO)

combat.combat([mychar, mychar2, mychar3], [byakhee, byakhee2])

