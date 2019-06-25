# -*- coding: utf-8 -*-
import sys

sys.path.append("../")
from blueprintBase import CBlueprintBase, make_Video
import outputDesc


class BPJiuGongGe(CBlueprintBase):

    # input: https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_7.mp4
    # output: http://test-v.oss-cn-shanghai.aliyuncs.com/hypnos-blueprint/output-10570-446757.mp4
    def __init__(self, user_element, width=720, height=1280, element_duration=None, action_configDict=None,
                 element_configDict=None):
        super(BPJiuGongGe, self).__init__("jiugongge")
        self._width = width
        self._height = height
        self._user_element = user_element
        self._action_configDict = action_configDict
        self._element_configDict = element_configDict
        self._element_duration = element_duration if element_duration else 3000
        self._element_type = self.get_elementType_fromValue(user_element)

    def init_outputDesc(self):
        outputLocation = "*"
        outputAlphaLocation = ".avi"
        fps = 25.0
        duration = self._element_duration
        bgColor = "RGBA(0,0,0,255)"
        self._outputDesc = outputDesc.create(self._width, self._height, outputLocation, outputAlphaLocation, fps,
                                             duration, bgColor)

    def init_level(self):
        configDict = dict()
        configDict['id'] = 0
        configDict['name'] = "jiugongge"
        configDict['actionNumber'] = 9
        configDict['elementNames'] = [self._elementNameFormat.format(configDict['name'], i) for i in
                                      range(configDict['actionNumber'])]
        configDict['newlevel_func'] = self.newLevel_jiugongge_Func
        configDict['newelement_func'] = self.newelement_jiugongge_Func
        configDict['baseTime'] = 0
        configDict["posList"] = [
            ('0,0,0.33,0.33', '0,0,0.33,0.33'),
            ('0.33,0,0.66,0.33', '0.33,0,0.66,0.33'),
            ('0.66,0,1,0.33', '0.66,0,1,0.33'),
            ('0,0.33,0.33,0.66', '0,0.33,0.33,0.66'),
            ('0.33,0.33,0.66,0.66', '0.33,0.33,0.66,0.66'),
            ('0.66,0.33,1,0.66', '0.66,0.33,1,0.66'),
            ('0,0.66,0.33,1', '0,0.66,0.33,1'),
            ('0.33,0.66,0.66,1', '0.33,0.66,0.66,1'),
            ('0.66,0.66,1,1', '0.66,0.66,1,1'),
        ]
        self._levelConfigs.append(configDict)

    def newLevel_jiugongge_Func(self, configDict):
        levelName = configDict['name']
        item = (0, self._element_duration)
        times = [item, item, item, item, item,
                 item, item, item, item]
        baseActionDict = {
            "name": levelName,
            "element": configDict['elementNames'],
            "startTime": times[0][0],
            "endTime": times[0][1],
            "startPos": "0,0,1,1",
            "endPos": "0,0,1,1"
        }
        kwargs = {
            'element': configDict['elementNames'],
            'startPos_endPos': configDict['posList']
        }
        if self._action_configDict:
            baseActionDict.update(self._action_configDict)
        level = self.create_level_from_action(baseActionDict, configDict, times, **kwargs)
        return level

    def newelement_jiugongge_Func(self, configDict):
        names = configDict['elementNames']
        video_prop = {
            "startTime": 0,
            "endTime": self._element_duration
        }
        for i, name in enumerate(names):
            element = {
                'name': name,
                'source': 'designer',
                'type': 'video',
                'value': self._user_element
            }
            element.update(video_prop)
            if self._element_configDict:
                element.update(self._element_configDict)
            self._elements.append(element)
        return

    def fill_resource(self):
        pass


def make_video(userVideo, videoDuration):
    maker = BPJiuGongGe(userVideo, element_duration=videoDuration)
    bpDict = maker.run()
    print(bpDict)
    maker.blueprint_2_video()
    outputVideo = maker._outputVideo
    return outputVideo


def test_effect():
    userVideo = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_7.mp4"
    videoDuration = 10000

    rotateVideo = make_video(userVideo, videoDuration)
    print(rotateVideo)


if __name__ == "__main__":
    test_effect()
