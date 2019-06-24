# -*- coding: utf-8 -*-

def create(width, height, outputLocation, outputAlphaLocation, fps, duration, bgColor):
    desc = dict()
    desc['width'] = width
    desc['height'] = height
    desc['outputLocation'] = outputLocation
    desc['outputAlphaLocation'] = outputAlphaLocation
    desc['fps'] = fps
    desc['duration'] = duration
    desc['bgColor'] = bgColor

    return desc
