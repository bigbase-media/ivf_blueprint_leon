# -*- coding: utf-8 -*-

def create(filterPath=None, transitionPath=None, maxComputeTime=None):
    config = dict()
    if (filterPath is not None):
        config['filterPath'] = filterPath
    if (transitionPath is not None):
        config['transitionPath'] = transitionPath
    if (maxComputeTime is not None):
        config['maxComputeTime'] = maxComputeTime
    return config
