# -*- coding: utf-8 -*-

def create(name, type, source, value, filter=None, vision=None, \
           option=None, textProp=None, videoProp=None, imageProp=None):
    eleDict = dict()
    eleDict['name'] = name
    eleDict['type'] = type
    eleDict['source'] = source
    eleDict['value'] = value
    if (filter is not None):
        eleDict['filter'] = filter
    if (vision is not None):
        eleDict['vision'] = vision
    if (option is not None):
        eleDict['option'] = option
    if (textProp is not None):
        eleDict['textProp'] = textProp
    if (videoProp is not None):
        eleDict['videoProp'] = videoProp
    if (imageProp is not None):
        eleDict['imageProp'] = imageProp
    return eleDict

def createVision(alpha=None, mask=None, loops=None, alphaThreshold=None, alphaBlendRadius=None):
    visionDict = dict()
    if (alpha is not None):
        visionDict['alpha'] = alpha
    if (mask is not None):
        visionDict['mask'] = mask
    if (loops is not None):
        visionDict['loops'] = loops
    if (alphaThreshold is not None):
        visionDict['alphaThreshold'] = alphaThreshold
    if (alphaBlendRadius is not None):
        visionDict['alphaBlendRadius'] = alphaBlendRadius
    return visionDict

def createOption(filterOptions=None, typeOptions=None):
    dic = dict()
    if (filterOptions is not None):
        dic['filterOptions'] = filterOptions
    if (typeOptions is not None):
        dic['typeOptions'] = typeOptions
    return dic

def createTextProp(color=None, fontSize=None, interval=None, fontType=None, lineSize=None):
    textProp = dict()
    if (color is not None):
        textProp['color'] = color
    if (fontSize is not None):
        textProp['fontSize'] = fontSize
    if (interval is not None):
        textProp['interval'] = interval
    if (fontType is not None):
        textProp['fontType'] = fontType
    if (lineSize is not None):
        textProp['lineSize'] = lineSize
    return textProp

def createVideoProp(asbgmusic=None, startTime=None, endTime=None, rect=None, rotate=None, playSpeed=None):
    videoProp = dict()
    if (asbgmusic is not None):
        videoProp['asbgmusic'] = asbgmusic
    if (startTime is not None):
        videoProp['startTime'] = startTime
    if (endTime is not None):
        videoProp['endTime'] = endTime
    if (rect is not None):
        videoProp['rect'] = rect
    if (rotate is not None):
        videoProp['rotate'] = rotate
    if (playSpeed is not None):
        videoProp['playSpeed'] = playSpeed
    return videoProp

def createImageProp(rect=None):
    imageProp = dict()
    if (rect is not None):
        imageProp['rect'] = rect
    return imageProp
