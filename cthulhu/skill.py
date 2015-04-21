#!/usr/bin/env python

import logging
from cthulhu.roll import skillRoll, result

class skill(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.half = int(value / 2)
        self.fifth = int(value / 5)

    def __str__(self):
        return "name: {:<18}\tvalue: {}\thalf: {}\tfifth: {}".format(self.name, self.value, self.half, self.fifth)

    def check(self, penalty=0, bonus=0):
        """ This will perform a skill check and return the type of result. """

        skillroll = skillRoll(penalty=penalty, bonus=bonus)
        logstr = "{} check ({}p,{}b): rolled {} against {} ... ".format(self.name, penalty,  bonus,  skillroll, self.value)

        if (self.value < 50 and 96 <= skillroll <= 100) or (self.value >= 50 and skillroll == 100):
            logstr = logstr + "Fumble!!!"
            myresult = result.fumble
        elif skillroll == 01:
            logstr = logstr + "CRITICAL SUCCESS!!!"
            myresult = result.critical
        elif skillroll <= self.fifth:
            logstr = logstr + "Extreme success!"
            myresult = result.extreme
        elif skillroll <= self.half:
            logstr = logstr + "Hard success!"
            myresult = result.hard
        elif skillroll <= self.value:
            logstr = logstr + "Normal success."
            myresult = result.normal
        else:
            logstr = logstr + "FAIL!"
            myresult = result.fail

        logging.info(logstr)
        return myresult

    def opposedSkill(self, opposed_skill, penalty=0, bonus=0):
        """ This will perform a non-combat skill check. This is one where the PC is rolling against another
              being, but the difficulty level is set based on their skill level. (Keepers Rulebook p83)

              This function takes the opposing skill and any penalty or bonus die.
        """
        logging.info("Opposed {}({}) skill check ({}p,{}b): Against {} ({}).".format(self.name, self.value, penalty, bonus, opposed_skill.name, opposed_skill.value))
        my_result = self.check(penalty=penalty, bonus=bonus)

        logstr = "Opposed {}({}) skill check ({}p,{}b): ".format(self.name, self.value, penalty, bonus,)

        if opposed_skill.value < 50:
           logstr = logstr + "Need a normal success..."
           needed = result.normal
        elif opposed_skill.value >= 90:
            logstr = logstr +  "Need an extreme success..."
            needed = result.extreme
        else:
            logstr = logstr +  "Need a hard success..."
            needed = result.hard

        if my_result >= needed:
            logstr = logstr +  "SUCCESS!!!"
        else:
            logstr = logstr +  "FAIL!!!"

        logging.info(logstr)
