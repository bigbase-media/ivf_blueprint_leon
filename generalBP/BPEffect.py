# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from blueprintBase import CBlueprintBase, MyException
import outputDesc, BPThread

# 演示视频
# 输入:
demoInput = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_4.mp4"
# 输出:
demoOutput = "http://test-v.oss-cn-shanghai.aliyuncs.com/hypnos-blueprint/output-8480-105948.mp4"


class CBPEffectRotate(CBlueprintBase):
    def __init__(self, userVideo, videoDuration, axis, width=720, height=1280):
        super(CBPEffectRotate, self).__init__("general-Effect")
        self._userVideo = userVideo
        self._videoDuration = videoDuration
        self._axis = axis
        self._width = width
        self._height = height

    def init_outputDesc(self):
        width = self._width
        height = self._height
        outputLocation = "*"
        outputAlphaLocation = ".avi"
        fps = 25.0
        duration = self._videoDuration
        bgColor = "RGBA(0,0,0,255)"
        self._outputDesc = outputDesc.create(width, height, outputLocation, outputAlphaLocation, fps, duration, bgColor)

    def init_level(self):
        configDict = dict()
        configDict['id'] = 0
        configDict['name'] = "rotate"
        configDict['actionNumber'] = 1
        configDict['elementNames'] = [self._elementNameFormat.format(configDict['name'], i) for i in range(configDict['actionNumber'])]
        configDict['newlevel_func'] = self.newLevel_rotate_Func
        configDict['newelement_func'] = self.newelement_rotate_Func
        configDict['baseTime'] = 0
        self._levelConfigs.append(configDict)

    def newLevel_rotate_Func(self, configDict):
        levelName = configDict['name']
        times = [(0, self._videoDuration)]
        baseActionDict = {
            "name": levelName,
            "element": configDict['elementNames'],
            "startTime": times[0][0],
            "endTime": times[0][1],
            "startPos" : "0.5,0.5,0,0",
            "endPos" : "0.5,0.5,0,0",
            "resizeMode": "pointalign",
            "subactions" : ["rotate"],
            "rotateConfig": {"startAngle": "0", "endAngle": "720", "rotateAxis": self._axis}
        }

        level = self.create_level_from_action(baseActionDict, configDict, times, element=configDict['elementNames'])
        return level

    def newelement_rotate_Func(self, configDict):
        elementNames = configDict['elementNames']

        for i, name in enumerate(elementNames):
            elementDict = dict()
            elementDict['name'] = name
            elementDict['source'] = "user"
            elementDict['type'] = self.get_elementType_fromValue(self._userVideo)
            elementDict['value'] = self._userVideo
            self._elements.append(elementDict)
        return

    def fill_resource(self):
        # self._resource['##ALPHA-scroll-video'] = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/res/shanshui3/scroll_alpha.mp4"
        # self._resource['##ELEMENT-scroll-video'] = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/res/shanshui3/scroll_fg.mp4"
        pass

def make_rotateVideo(userVideo, videoDuration, axis):
    rotateUElement = CBPEffectRotate(userVideo, videoDuration, axis)
    bpDict = rotateUElement.run()
    print(bpDict)
    rotateUElement.blueprint_2_video()
    outputDict = dict()
    outputDict['outputVideo'] = rotateUElement._outputVideo
    outputDict['outputAlpha'] = rotateUElement._outputAlpha
    return outputDict

def make_rotateVideo_asyn(userVideo, videoDuration, axis):
    t = BPThread(make_rotateVideo, userVideo, videoDuration, axis)
    t.setDaemon(True)
    t.start()
    return t

def make_rotateVideo_asyn_join(t):
    return t.join()

def test_rotateEffect():
    userVideo = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_4.mp4"
    videoDuration = 3000

    rotateDict = make_rotateVideo(userVideo, videoDuration, "y")
    print(rotateDict)


if __name__=="__main__":
    test_rotateEffect()
