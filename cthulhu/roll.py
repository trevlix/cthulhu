#!/usr/bin/env python

import random
import re
import logging

def skillRoll(penalty=0, bonus=0):
    """
        This function will perform the roll for a skill check, which uses a
        percentage roll from 1-100, which is potentially different than a 1d100.

        This function will also take into account penalty and bonus dice.
    """
    myroll = random.randint(1, 100)
    tens = myroll / 10
    ones = myroll % 10
    #ones = random.randint(1, 10)
    #tens = random.randint(0, 9)

    logging.debug("Skill roll: Initial roll is {}".format(tens * 10 + ones))

    # Make sure we have no more than 2 bonus or penalty die
    penalty = min(penalty, 2)
    bonus = min(bonus, 2)

    # determine if we have more penalty or bonus dice
    otherdice = (penalty * -1) + bonus
    if otherdice > 0:
        for x in range(0, otherdice):
            bonus = random.randint(0, 9)
            logging.debug("\tBonus Die: Tens is currently {}, Bonus dice rolled {}".format(tens, bonus))
            if bonus < tens:
                myroll = bonus * 10 + ones
    elif otherdice < 0:
        for x in range(0, otherdice*-1):
            penalty = random.randint(0, 9)
            logging.debug("\tPenalty Dice: Tens is currently {}, Penalty dice rolled {}".format(tens, penalty))
            if penalty > tens:
                myroll = penalty * 10 + ones

    logging.debug("\tSkill roll: Final roll is {}".format(myroll))
    return (myroll)

def roll(die):
    """
        This will parse and roll a die roll string such as 1d6, 3d6*5, 1d8+1d4, etc.
        The result of the roll is returned.

        Warnings:
          - Order of operations is not kept so the string cannot be too complicated.
            However, 2d6+6*5 will work as it should.
          - Do not use this for percentage checks. They are a bit more complicated
            in Call of Cthulhu. Use the skillRoll() function instead.
    """
    dieSplit = re.compile(r"d")
    splitDie = re.compile(r"(\W)")
    total = 0
    operator = '+'
    logging.debug("Rolling a {}".format(die))

    for dice in splitDie.split(die):
        rolled = 0

        if 'd' in dice:
            # we have a dice roll
            (numTimes, numSides) = dieSplit.split(dice)
        elif dice in [ '+', '-', '*']:
            # we have an operator
            numTimes = 0
            numSides = 0
            operator = dice
            continue
        else:
            # this should just be an int - try to convert it
            numTimes = -1
            numSides = int(dice)

        if numTimes > 0:
            # roll some dice
            for i in range(int(numTimes)):
                tempRoll =  random.randint(1, int(numSides))
                rolled = rolled + tempRoll
                logging.debug('\tRolled a {}, total is now {}'.format(tempRoll, rolled))
        elif numTimes == -1:
            # we have just a number
            rolled = numSides

        if operator == '-':
            total = total - rolled
            operator = '+'
        elif operator == '*':
            total = total * rolled
            operator = '+'
        else:
            total = total + rolled

    logging.debug("\tTotal rolled is {}".format(total))
    return total

