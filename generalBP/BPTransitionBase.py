# -*- coding: utf-8 -*-

import sys, time
sys.path.append("../")
from blueprintBase import *
import blueprintBase
from generalBP import BPEffect
from xyl_leon import LYBF_scroll
import outputDesc, transition

# 演示视频
g_userInputs = ["https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_5.mp4",
                  "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_6.mp4",
                  "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_7.mp4",
                  "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_8.mp4"]
g_outVideo = "http://test-v.oss-cn-shanghai.aliyuncs.com/hypnos-blueprint/output-8528-875541.mp4"

class CBPTransitionBase(CBlueprintBase):
    def __init__(self, userInputs, sliceDuration, width=720, height=1280):
        super(CBPTransitionBase, self).__init__("general-TransitionBase")
        self._userInputs = userInputs
        self._sliceDuration = sliceDuration
        self._width = width
        self._height = height

    def init_outputDesc(self):
        width = self._width
        height = self._height
        outputLocation = "*"
        outputAlphaLocation = "*"
        fps = 25.0
        duration = self._sliceDuration * len(self._userInputs)
        bgColor = "RGBA(0,0,0,255)"
        self._outputDesc = outputDesc.create(width, height, outputLocation, outputAlphaLocation, fps, duration, bgColor)

    def init_level(self):
        configDict = dict()
        configDict['id'] = 0
        configDict['name'] = "userVideo"
        configDict['actionNumber'] = len(self._userInputs)
        configDict['elementNames'] = [self._elementNameFormat.format(configDict['name'], i) for i in range(configDict['actionNumber'])]
        configDict['newlevel_func'] = self.newLevel_userVideo_Func
        configDict['newelement_func'] = self.newelement_userVideo_Func
        configDict['baseTime'] = 0
        self._levelConfigs.append(configDict)

    def newLevel_userVideo_Func(self, configDict):
        levelName = configDict['name']
        times = [(i*self._sliceDuration, (i+1)*self._sliceDuration) for i in range(len(self._userInputs))]
        baseActionDict = {
            "name": levelName,
            "element": configDict['elementNames'],
            "startTime": times[0][0],
            "endTime": times[0][1],
            "startPos" : "0.5,0.5,0,0",
            "endPos" : "0.5,0.5,0,0",
            "resizeMode": "pointalign"
        }

        transitionList = []
        for i in range(len(self._userInputs)-1):
            transitionDict = transition.create("random", self._actionNameFormat.format(configDict['name'], i+1, times[i+1][0], times[i+1][1]))
            transitionList.append(transitionDict)
        transitionList.append(None)
        # exit(0)

        level = self.create_level_from_action(baseActionDict, configDict, times, element=configDict['elementNames'], transition=transitionList)
        return level

    def newelement_userVideo_Func(self, configDict):
        elementNames = configDict['elementNames']

        for i, name in enumerate(elementNames):
            elementDict = dict()
            elementDict['name'] = name
            elementDict['source'] = "user"
            elementDict['type'] = self.get_elementType_fromValue(self._userInputs)
            elementDict['value'] = self._userInputs[i]
            self._elements.append(elementDict)
        return

    def fill_resource(self):
        return

def make_transitionVideo(userInputs, sliceDuration):
    transitionUElement = CBPTransitionBase(userInputs, sliceDuration)
    bpDict = transitionUElement.run()
    print(bpDict)
    transitionUElement.blueprint_2_video()
    outputVideo = transitionUElement._outputVideo
    return outputVideo

def test_transitionEffect_asyn():
    userInputs = ["https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_5.mp4",
                  "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_6.mp4",
                  # "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_7.mp4",
                  "http://test-v.oss-cn-shanghai.aliyuncs.com/dd.jpg",
                  "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_8.mp4"]
    sliceDuration = 3000
    # userInputs = ["https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_5.mp4"]

    userScrolls = []
    threads = []
    xyz = "xyzxyzxyz"
    for i, video in enumerate(userInputs):
        t = blueprintBase.make_Video_asyn(BPEffect.CBPEffectRotate, video, sliceDuration, xyz[i])
        threads.append(t)

    for i, t in enumerate(threads):
        outputDict = t.join()
        userScrolls.append(outputDict['outputVideo'])

    outputVideo = make_transitionVideo(userScrolls, sliceDuration)
    print(outputVideo)

def test_transitionEffect():
    userInputs = ["https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_5.mp4",
                  "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_6.mp4",
                  "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_7.mp4",
                  "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_8.mp4"]
    sliceDuration = 3000
    # userInputs = ["https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_5.mp4"]

    userScrolls = []
    xyz = "xyzxyzxyz"
    for i, video in enumerate(userInputs):
        rotateDict = blueprintBase.make_Video(BPEffect.CBPEffectRotate, video, sliceDuration, xyz[i])
        userScrolls.append(rotateDict['outputVideo'])

    outputVideo = make_transitionVideo(userScrolls, sliceDuration)
    print(outputVideo)


if __name__=="__main__":
    startTime = time.time()
    test_transitionEffect()
    # print("同步的时间： ", time.time()-startTime)
    startTime = time.time()
    test_transitionEffect_asyn()
    print("异步的时间： ", time.time() - startTime)
