#!/usr/bin/env python

# script to test various skill checks

import logging
from cthulhu.skill import skill
from cthulhu.roll import roll

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

#testskill = skill('Spot Hidden', 65)
#testskill.dump()
#testskill.check()
#otherskill = skill('Sneak', 25)
#testskill.opposedSkill(otherskill)
roll('1d6+1d6', max=True)
