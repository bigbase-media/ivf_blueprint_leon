# -*- coding: utf-8 -*-

from generalBP import *
import BPThread, blueprintBase

g_effect_dict = {
    "DarkCorner" : BPDarkCorner.CBPDarkCorner,
    "Rotate" : BPEffect.CBPEffectRotate,
    "Filter" : BPFilter.CBPFilter
}


def IVF_pipeline(inputElement, duration, effect_list, effectConfig):
    outputVideo = inputElement
    for i, effectName in enumerate(effect_list):
        if (effectName not in g_effect_dict.keys()):
            raise Exception("illegal effect name")
        effectClass = g_effect_dict[effectName]
        configDict = effectConfig.get(effectName, dict())
        outputDict = blueprintBase.make_Video(effectClass, outputVideo, duration, configDict)
        # print(outputDict)
        outputVideo = outputDict['outputVideo']
    return outputVideo

# 异步实现，适合有多个素材需要处理的场景
def IVF_pipeline_asyn(inputElement, duration, effect_list, effectConfig):
    t = BPThread.BPThread(IVF_pipeline, duration, effect_list, effectConfig)
    t.setDaemon(True)
    t.start()
    return t

def IVF_pipeline_asyn_join(t):
    return t.join()

####   TEST PROGRAM
def test():
    inputElement = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_hp_4.mp4"
    duration = 3000
    effect_list = ['DarkCorner', 'Filter']
    effectConfig = dict()
    outputVideo = IVF_pipeline(inputElement, duration, effect_list, effectConfig)
    print(outputVideo)

if __name__=="__main__":
    test()
