# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from blueprintBase import CBlueprintBase, MyException
import outputDesc

class CLYBF_Scroll(CBlueprintBase):
    def __init__(self, userVideo, videoDuration):
        super(CLYBF_Scroll, self).__init__("lybf-scroll")
        self._userVideo = userVideo
        self._videoDuration = videoDuration

    def init_outputDesc(self):
        width = 720
        height = 1280
        outputLocation = "*"
        outputAlphaLocation = ".avi"
        fps = 25.0
        duration = self._videoDuration
        bgColor = "RGBA(0,0,0,255)"
        self._outputDesc = outputDesc.create(width, height, outputLocation, outputAlphaLocation, fps, duration, bgColor)

    def init_level(self):
        configDict = dict()
        configDict['id'] = 0
        configDict['name'] = "scroll"
        configDict['actionNumber'] = 1
        configDict['elementNames'] = [self._elementNameFormat.format(configDict['name'], i) for i in range(configDict['actionNumber'])]
        configDict['newlevel_func'] = self.newLevel_scroll_Func
        configDict['newelement_func'] = self.newelement_scroll_Func
        configDict['baseTime'] = 0
        self._levelConfigs.append(configDict)

        configDict = dict()
        configDict['id'] = 1
        configDict['name'] = "userVideo"
        configDict['actionNumber'] = 1
        configDict['elementNames'] = [self._elementNameFormat.format(configDict['name'], i) for i in
                                      range(configDict['actionNumber'])]
        configDict['newlevel_func'] = self.newLevel_userVideo_Func
        configDict['newelement_func'] = self.newelement_userVideo_Func
        configDict['baseTime'] = 0
        self._levelConfigs.append(configDict)

    def newLevel_scroll_Func(self, configDict):
        levelName = configDict['name']
        times = [(0, self._videoDuration)]
        baseActionDict = {
            "name": levelName,
            "element": configDict['elementNames'],
            "startTime": times[0][0],
            "endTime": times[0][1],
            "startPos" : "0,0,1,1",
            "endPos" : "0,0,1,1"
        }

        level = self.create_level_from_action(baseActionDict, configDict, times, element=configDict['elementNames'])
        return level

    def newelement_scroll_Func(self, configDict):
        elementNames = configDict['elementNames']

        for i, name in enumerate(elementNames):
            elementDict = dict()
            elementDict['name'] = name
            elementDict['source'] = "designer"
            elementDict['type'] = "video"
            elementDict['value'] = self.getResource("element", configDict, subType="video")
            visionDict = dict()
            visionDict['alpha'] = self.getResource("alpha", configDict, subType="video")
            elementDict['vision'] = visionDict
            self._elements.append(elementDict)
        return

    def newLevel_userVideo_Func(self, configDict):
        levelName = configDict['name']
        times = [(0, self._videoDuration)]
        baseActionDict = {
            "name": levelName,
            "element": configDict['elementNames'],
            "startTime": times[0][0],
            "endTime": times[0][1],
            "startPos": "0.2,0.2,0.8,0.8",
            "endPos": "0.2,0.2,0.8,0.8"
        }

        level = self.create_level_from_action(baseActionDict, configDict, times, element=configDict['elementNames'])
        return level

    def newelement_userVideo_Func(self, configDict):
        elementNames = configDict['elementNames']

        for i, name in enumerate(elementNames):
            elementDict = dict()
            elementDict['name'] = name
            elementDict['source'] = "user"
            elementDict['type'] = "video"
            elementDict['value'] = self._userVideo
            self._elements.append(elementDict)
        return

    def fill_resource(self):
        self._resource['##ALPHA-scroll-video'] = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/res/shanshui3/scroll_alpha.mp4"
        self._resource['##ELEMENT-scroll-video'] = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/res/shanshui3/scroll_fg.mp4"


def make_scrollVideo(userVideo, videoDuration):
    scrollUElement = CLYBF_Scroll(userVideo, videoDuration)
    bpDict = scrollUElement.run()
    print(bpDict)
    scrollUElement.blueprint_2_video()
    outputVideo = scrollUElement._outputVideo
    return outputVideo

def main():
    userVideo = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_4.mp4"
    videoDuration = 20000

    scrollVideo = make_scrollVideo(userVideo, videoDuration)
    newVideo = make_scrollVideo(scrollVideo, videoDuration)
    print(newVideo)


if __name__=="__main__":
    main()
