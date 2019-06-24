# -*- coding: utf-8 -*-

import random

g_legalTransitionList = ["t2d2lines",  "t2ddropsquare",  "t2drotate",  "t2dstripe", "t2dtriangle",
                         "t2dboard", "t2drectangle", "t2dsquare", "t2dtrapezoid", "t2dwave"]

def create(value, next, type="normal2d", legalList=g_legalTransitionList):
    transitionDict = dict()
    if (value in legalList):
        transitionDict['value'] = value
        transitionDict['type'] = type
        transitionDict['next'] = next
        return transitionDict
    elif (value=="random"):
        id = random.randint(0, len(legalList)-1)
        transitionDict['value'] = legalList[id]
        transitionDict['type'] = type
        transitionDict['next'] = next
        return transitionDict
    else:
        print("ERROR create transition")
        return None

