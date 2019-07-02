# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from blueprintBase import *
import transition, IVF_pipeline

class CMerger(CBlueprintBase):
    def __init__(self, userInputs, sliceDuration, width=720, height=1280, configDict=None):
        super(CMerger, self).__init__("Merger")
        self._userInputs = userInputs
        self._sliceDuration = sliceDuration
        self._width = width
        self._height = height
        self._configDict = configDict
        if (self._configDict is None):
            self._configDict = dict()
        self._bgmusic = self._configDict.get("bgmusic", None)
        self._bgPic = self._configDict.get("bgPic", None)
        self._userAlpha = self._configDict.get("userAlpha", None)
        self._transitionFlag = self._configDict.get("Merger_transitionFlag", 0)
        self._effectList = self._configDict.get("Merger_effects", [])
        if (self._sliceDuration<=0):
            self._durations = self._configDict['durations']
        else:
            self._durations = [self._sliceDuration for i in range(len(self._userInputs))]

    def preprocess_userInput(self):
        print(sys._getframe().f_code.co_name)
        if (len(self._effectList)==0):
            return
        threads = []
        for i, input in enumerate(self._userInputs):
            if (self._sliceDuration<=0):
                duration = self._durations[i]
            else:
                duration = self._sliceDuration
            t = IVF_pipeline.IVF_pipeline_asyn(input, duration, self._effectList, dict())
            threads.append(t)
        self._userInputs = []
        for t in threads:
            output = t.join()
            self._userInputs.append(output)

    def init_outputDesc(self):
        width = self._width
        height = self._height
        outputLocation = "*"
        outputAlphaLocation = "*"
        fps = 25.0
        if (self._sliceDuration<=0):
            duration = sum(self._durations)
        else:
            duration = self._sliceDuration * len(self._userInputs)
        bgColor = "RGBA(0,0,0,255)"
        self._outputDesc = outputDesc.create(width, height, outputLocation, outputAlphaLocation, fps, duration, bgColor)

    def init_level(self):
        id = 0
        if (self._bgPic is not None):
            configDict = self.init_level_bgPic()
            self._levelConfigs.append(configDict)
            id += 1

        configDict = dict()
        configDict['id'] = id
        id += 1
        configDict['name'] = "userVideo"
        configDict['actionNumber'] = len(self._userInputs)
        configDict['elementNames'] = [self._elementNameFormat.format(configDict['name'], i) for i in
                                      range(configDict['actionNumber'])]
        configDict['newlevel_func'] = self.newLevel_userVideo_Func
        configDict['newelement_func'] = self.newelement_userVideo_Func
        configDict['baseTime'] = 0
        self._levelConfigs.append(configDict)

    def fill_resource(self):
        if (self._bgmusic is not None):
            self._resource[
                BPConfig.g_bgmusic_resourceName] = self._bgmusic
        self._resource["##ALPHA-userVideo-video"] = self._userAlpha
        return

    def newLevel_userVideo_Func(self, configDict):
        levelName = configDict['name']
        # times = [(i*self._sliceDuration, (i+1)*self._sliceDuration) for i in range(len(self._userInputs))]
        times = [(sum(self._durations[0:i]), sum(self._durations[0:i+1])) for i in range(len(self._durations))]
        baseActionDict = {
            "name": levelName,
            "element": configDict['elementNames'],
            "startTime": times[0][0],
            "endTime": times[0][1],
            "startPos" : "0.5,0.5,0,0",
            "endPos" : "0.5,0.5,0,0",
            "resizeMode": "pointalign"
        }


        if (self._transitionFlag!=0):
            transitionList = []
            for i in range(len(self._userInputs)-1):
                transitionDict = transition.create("random", self._actionNameFormat.format(configDict['name'], i+1, times[i+1][0], times[i+1][1]))
                transitionList.append(transitionDict)
            transitionList.append(None)
        else:
            transitionList = None
        # exit(0)

        level = self.create_level_from_action(baseActionDict, configDict, times, element=configDict['elementNames'], transition=transitionList)
        return level

    def newelement_userVideo_Func(self, configDict):
        elementNames = configDict['elementNames']

        for i, name in enumerate(elementNames):
            elementDict = dict()
            elementDict['name'] = name
            elementDict['source'] = "user"
            print(self._userInputs[i])
            elementDict['type'] = self.get_elementType_fromValue(self._userInputs[i])
            elementDict['value'] = self._userInputs[i]
            if (self._userAlpha is not None):
                visionDict = dict()
                visionDict['alpha'] = self.getResource("alpha", configDict, subType=self.get_elementType_fromValue(self._userAlpha))
                elementDict['vision'] = visionDict
            self._elements.append(elementDict)
        return

    def init_level_bgPic(self):
        configDict = dict()
        configDict['id'] = 0
        configDict['name'] = "bgPic"
        configDict['actionNumber'] = 1
        configDict['elementNames'] = [self._elementNameFormat.format(configDict['name'], i) for i in
                                      range(configDict['actionNumber'])]
        configDict['newlevel_func'] = self.newLevel_bgPic_Func
        configDict['newelement_func'] = self.newelement_bgPic_Func
        configDict['baseTime'] = 0
        return configDict

    def newLevel_bgPic_Func(self, configDict):
        levelName = configDict['name']
        # times = [(0, self._sliceDuration*len(self._userInputs))]
        times = [(0, sum(self._durations))]
        baseActionDict = {
            "name": levelName,
            "element": configDict['elementNames'],
            "startTime": times[0][0],
            "endTime": times[0][1],
            "startPos" : "0.5,0.5,0,0",
            "endPos" : "0.5,0.5,0,0",
            "resizeMode": "pointalign"
        }
        level = self.create_level_from_action(baseActionDict, configDict, times, element=configDict['elementNames'])
        return level

    def newelement_bgPic_Func(self, configDict):
        elementNames = configDict['elementNames']

        for i, name in enumerate(elementNames):
            elementDict = dict()
            elementDict['name'] = name
            elementDict['source'] = "user"
            elementDict['type'] = self.get_elementType_fromValue(self._bgPic)
            elementDict['value'] = self._bgPic
            self._elements.append(elementDict)
        return

def mergeElements(userInputs, sliceDuration, bgPic=None, durations=None):
    configDict = dict()
    configDict['bgPic'] = bgPic
    configDict['bgmusic'] = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/res/dior/diorCopy.aac"
    #"https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/res/duopai/jiezoubg.mp3"
    configDict['Merger_transitionFlag'] = 1
    configDict['Merger_effects'] = ['Filter', 'scroll']
    configDict['userAlpha'] = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/res/shanshui3/jz_alpha2.mp4"
    configDict['durations'] = durations
    merger = CMerger(userInputs, sliceDuration, configDict=configDict)
    bpDict = merger.run()
    print(bpDict)
    merger.blueprint_2_video()
    outputVideo = merger._outputVideo
    return outputVideo

def test():
    bgPic = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_2.mp4"
    userInputs = ["https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_5.mp4",
                  "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_6.mp4",
                  # "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_7.mp4",
                  "http://test-v.oss-cn-shanghai.aliyuncs.com/dd.jpg",
                  "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_8.mp4"]
    output = mergeElements(userInputs, 0, bgPic=bgPic, durations=[2000, 3000, 4000, 5000])

if __name__=="__main__":
    test()
