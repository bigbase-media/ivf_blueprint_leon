# -*- coding: utf-8 -*-

# subactionions 参数这里不写了
g_action_keynames = ["name", "projectionType", "element", "startTime", "endTime", "startPos", "endPos",
                     "resizeMode","startAlpha", "endAlpha", "subactions", "alignPoint", "startScale",
                     "endScale", "startAngle", "endAngle", "track", "transition"]

g_level_keyname_copy_lst = ["projectionType", "element", "resizeMode", "subactions",
                   "alignPoint", "track", "transition"]
g_level_keyname_split_lst = ["startTime_endTime", "startPos_endPos", "startScale_endScale",
                             "startAngle_endAngle", "startAlpha_endAlpha"]
g_level_keyname = g_level_keyname_copy_lst + g_level_keyname_split_lst


def create(name, element, startTime, endTime, startPos, endPos, **kwargs):
    actionDict = {
        "name": name,
        "element": element,
        "startTime": startTime,
        "endTime": endTime,
        "startPos": startPos,
        "endPos": endPos
    }
    actionDict.update(**kwargs)
    return actionDict

def createTransition(type, value, next, duration=None):
    item = {
        "type" : type,
        "value": value,
        "next": next
    }
    if (duration is not None):
        item['duration'] = duration
    return item

