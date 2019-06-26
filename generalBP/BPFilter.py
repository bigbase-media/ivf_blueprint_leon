# -*- coding: utf-8 -*-
import sys
import os

sys.path.append("../")
from blueprintBase import CBlueprintBase, make_Video
import outputDesc, IBL_utils, BPConfig


class CBPFilter(CBlueprintBase):

    # input: https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_7.mp4
    # output: http://test-v.oss-cn-shanghai.aliyuncs.com/hypnos-blueprint/output-8535-468735.mp4
    def __init__(self, userElement, videoDuration, configDict=dict()):
        super(CBPFilter, self).__init__("Filter")
        self._width = configDict.get('width', 720)
        self._height = configDict.get('height', 1280)
        self._ele_filter = configDict.get('Filter_type', "random")
        if (self._ele_filter=="random"):
            self._ele_filter = IBL_utils.get_random(BPConfig.g_legal_filterType)
        self._user_element = userElement
        self._elemnet_duration = videoDuration
        self._element_type = self.get_elementType_fromValue(userElement)

    def init_outputDesc(self):
        outputLocation = "*"
        outputAlphaLocation = "*"
        fps = 25.0
        duration = self._elemnet_duration
        bgColor = "RGBA(0,0,0,255)"
        self._outputDesc = outputDesc.create(self._width, self._height, outputLocation, outputAlphaLocation, fps,
                                             duration, bgColor)

    def init_level(self):
        configDict = dict()
        configDict['id'] = 0
        configDict['name'] = "ele-filter"
        configDict['actionNumber'] = 1
        configDict['elementNames'] = [self._elementNameFormat.format(configDict['name'], i) for i in
                                      range(configDict['actionNumber'])]
        configDict['newlevel_func'] = self.newLevel_shake_Func
        configDict['newelement_func'] = self.newelement_shake_Func
        configDict['baseTime'] = 0
        self._levelConfigs.append(configDict)

    def newLevel_shake_Func(self, configDict):
        levelName = configDict['name']
        times = [(0, self._elemnet_duration)]
        baseActionDict = {
            "name": levelName,
            "element": configDict['elementNames'],
            "startTime": times[0][0],
            "endTime": times[0][1],
            "projectionType": "normal",
            "resizeMode": "cropimg",
            "startPos": "0,0,1,1",
            "endPos": "0,0,1,1"
        }
        kwargs = {
            'element': configDict['elementNames']
        }
        level = self.create_level_from_action(baseActionDict, configDict, times, **kwargs)
        return level

    def newelement_shake_Func(self, configDict):
        names = configDict['elementNames']
        for i, name in enumerate(names):
            element = {
                'name': name,
                'source': 'designer',
                'type': self._element_type,
                'value': self._user_element
            }
            if self._ele_filter:
                element.update({'filter': self._ele_filter})
            self._elements.append(element)


def test_effect():
    userVideo = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_7.mp4"
    videoDuration = 3000
    configDict = dict()
    configDict['Filter_type'] = 'random'
    rotateVideo = make_Video(CBPFilter, userVideo, videoDuration, configDict)
    print(rotateVideo)


if __name__ == "__main__":
    test_effect()
