# -*- coding: utf-8 -*-

def create():
    resourceDict = dict()
    return resourceDict

def addOne(resourceDict, key, value):
    if (len(key)<=2):
        return 'err'
    if (key[0:2]!="##"):
        print("key must be like '##xx' : %s " % key)
        return 'err'
    resourceDict[key] = value
    return 'ok'


