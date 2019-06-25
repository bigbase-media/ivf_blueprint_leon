# -*- coding: utf-8 -*-
import sys
import os

sys.path.append("../")
from blueprintBase import CBlueprintBase, make_Video
import outputDesc

class BPText2video(CBlueprintBase):

    # input: https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_7.mp4
    # output: http://test-v.oss-cn-shanghai.aliyuncs.com/hypnos-blueprint/output-8529-014172.mp4
    def __init__(self, input_data):
        super(BPText2video, self).__init__("Text2video")
        self._user_elements = input_data

    def init_outputDesc(self):
        width = 720
        height = 1280
        outputLocation = "*"
        outputAlphaLocation = ".avi"
        fps = 25.0
        duration = 1000
        bgColor = "RGBA(0,0,0,255)"
        self._outputDesc = outputDesc.create(width, height, outputLocation, outputAlphaLocation, fps, duration, bgColor)

    def init_level(self):
        for index, text in enumerate(self._user_elements):
            configDict = dict()
            configDict['id'] = 0
            configDict['name'] = "text2video" + "_" + str(index)
            configDict['actionNumber'] = 1
            configDict['elementNames'] = [self._elementNameFormat.format(configDict['name'], i) for i in
                                          range(configDict['actionNumber'])]
            configDict['newlevel_func'] = self.newLevel_shake_Func
            configDict['newelement_func'] = self.newelement_shake_Func
            configDict['fontheight']=text['fontheight'] * index
            configDict['baseTime'] = 0
            configDict['value'] = text['value']
            configDict['fontsize'] = text['fontsize']
            configDict['linesize'] = text['linesize']
            self._levelConfigs.append(configDict)

    def newLevel_shake_Func(self, configDict):
        levelName = configDict['name']
        times = [(0, 1000)]
        baseActionDict = {
            "name": levelName,
            "element": configDict['elementNames'],
            "startTime": times[0][0],
            "endTime": times[0][1],
            "resizeMode": "pointalign",
            "alignPoint": "0.5,0.5",
            "startPos": "0.5," + str(0.3+configDict['fontheight']) +",1,1",
            "endPos": "0.5," + str(0.3+configDict['fontheight']) +",1,1",
        }
        kwargs = {
            'element': configDict['elementNames']
        }

        level = self.create_level_from_action(baseActionDict, configDict, times, **kwargs)
        return level

    def newelement_shake_Func(self, configDict):
        names = configDict['elementNames']
        text_prop = {
            "textProp": {
                "fontType": "SourceHanSansCN-Medium.otf",
                "color": "#ffffff",
                "fontSize": configDict['fontsize'],
                "lineSize": configDict['linesize']
            }
        }
        for i, name in enumerate(names):
            element = {
                'name': name,
                'source': 'designer',
                'type': "text",
                'value': configDict['value']
            }
            element.update(text_prop)
            self._elements.append(element)


def test_effect():
    text_data = [{'value': "京东618","fontsize": 150, "linesize":10, "fontheight": 0.1},
                 {'value': "满2减1","fontsize": 120, "linesize":10, "fontheight": 0.1}]

    rotateVideo = make_Video(BPText2video, text_data)
    print(rotateVideo)


if __name__ == "__main__":
    test_effect()