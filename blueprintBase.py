# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import urllib, http.client
import copy, sys, warnings, json, BPThread, os
import blueprintDesc, element, action, hypnosConfig, outputDesc, resource
import BPConfig


class MyException(Exception): # 继承异常类
     def __init__(self, name, reason):
        self.name = name
        self.reason = reason

class CBlueprintBase():
    def __init__(self, blueprintName):
        # self._apiurl = "http://127.0.0.1:1108/task"
        self._apiurl = "http://hypnos.innotechx.com/task"
        self._outputVideo = None
        self._outputAlpha = None

        self._bpDesc = blueprintDesc.create(blueprintName)
        self._outputDesc = None
        self._resource = resource.create()
        self._elements = []
        self._actions = []
        self._hypnosConfig = hypnosConfig.create()
        self._blueprint = None

        self._actionLevels = []
        self._levelConfigs = []
        self._resourceNameSet = set()

        # action name format
        self._actionNameFormat = "ACT-{}-{}-*{}-{}*"
        self._elementNameFormat = "ELE-{}-{}"
        self._resTrackFormat0 = "##TRACK-{}"
        self._resTrackFormat1 = "##TRACK-{}-{}"
        self._resElementFormat0 = "##ELEMENT-{}-{}"
        self._resElementFormat1 = "##ELEMENT-{}-{}-{}"
        self._resAlphaFormat0 = "##ALPHA-{}-{}"
        self._resAlphaFormat1 = "##ALPHA-{}-{}-{}"

    def getResource(self, type, levelConfigDict, elementID=None, actionID=None, subType=None):
        legalTypes = ['track', "element", "alpha"]
        if (type not in legalTypes):
            raise MyException("resource illegal type", "type error")
        if (type=="track"):
            if (actionID is None):
                name = self._resTrackFormat0.format(levelConfigDict['name'])
            else:
                name = self._resTrackFormat1.format(levelConfigDict['name'], actionID)
        elif (type=="element"):
            if (subType is None):
                raise MyException("getResource fail", "no subType")
            if (elementID is None):
                name = self._resElementFormat0.format(levelConfigDict['name'], subType)
            else:
                name = self._resElementFormat1.format(levelConfigDict['name'], subType, elementID)
        elif (type=="alpha"):
            if (subType is None):
                raise MyException("getResource fail", "no subType")
            if (elementID is None):
                name = self._resAlphaFormat0.format(levelConfigDict['name'], subType)
            else:
                name = self._resAlphaFormat1.format(levelConfigDict['name'], subType, elementID)
        else:
            raise MyException("getResource fail", "not supported type : %s" % type)

        self._resourceNameSet.add(name)
        return name

    @abstractmethod
    def init_outputDesc(self):
        pass

    @abstractmethod
    def init_level(self):
        pass

    @abstractmethod
    def fill_resource(self):
        pass

    def check_elements(self):
        bgmusicName = "##bgmusic"
        if (self._resource.get(bgmusicName, None) is None):
            warnings.warn("似乎没有设置背景音乐吧")

        elementNames = []
        for i, elementDict in enumerate(self._elements):
            elementNames.append(elementDict["name"])
        actionElements = []
        for i, actionDict in enumerate(self._actions):
            actionElement = actionDict['element']
            if (actionElement not in elementNames):
                raise MyException("element %s 没定义" % actionElement, "请定义levelConfig 的 newelement_func 函数")

    def check_resource(self):
        namelist = list(self._resourceNameSet)
        for name in namelist:
            value = self._resource.get(name, None)
            if (value is None):
                raise MyException("resource %s 没定义" % name, "请在self._resource 中设置 %s 的值" % name)

    def make_actionLevels(self):
        print(sys._getframe().f_code.co_name)
        self.init_level()

        if (len(self._levelConfigs)==0):
            raise MyException("no _levelConfigs", "you must set self._levelConfigs in function: init_level")
        for i, configDict in enumerate(self._levelConfigs):
            func = configDict['newlevel_func']
            if (func is None):
                raise MyException("levelName %s no function" % configDict['name'], "you can define this function in your class")
            level = func(configDict)
            self._actionLevels.append(level)
            eleFunc = configDict['newelement_func']
            eleFunc(configDict)
        print(self._actionLevels)

    def init_bpDesc(self, **kwargs):
        self._bpDesc.update(kwargs)
        return 'ok'

    def run(self):
        self.init_outputDesc()
        self.make_actionLevels()
        if (len(self._actionLevels)==0):
            raise MyException("no self._actionLevels", "缺少action图层")
        for level in self._actionLevels:
            self._actions += level

        self.fill_resource()
        self.check_elements()
        self.check_resource()

        return self.make()

    def make(self):
        if (self._outputDesc is None):
            return None
        self._blueprint = dict()
        self._blueprint['blueprintDesc'] = self._bpDesc
        self._blueprint['outputDesc'] = self._outputDesc
        self._blueprint['resource'] = self._resource
        self._blueprint['elements'] = self._elements
        self._blueprint['actions'] = self._actions
        self._blueprint['hypnosConfig'] = self._hypnosConfig
        return self._blueprint

    def create_level_from_action(self, actDict, configDict, times, **kwargs):
        baseTime = configDict.get("baseTime", 0)
        level = []
        for i, (startTime, endTime) in enumerate(times):
            startTime += baseTime
            endTime += baseTime
            actionTmpDict = copy.deepcopy(actDict)
            actionTmpDict['startTime'] = startTime
            actionTmpDict['endTime'] = endTime
            actionTmpDict['name'] = self._actionNameFormat.format(configDict['name'], i, startTime, endTime)
            for key in kwargs:
                values = kwargs[key]
                if (key in action.g_level_keyname_copy_lst):
                    if (values[i] is not None):
                        actionTmpDict[key] = values[i]
                elif (key in action.g_level_keyname_split_lst):
                    start, end = key.split("_")
                    actionTmpDict[start] = values[i][0]
                    actionTmpDict[end] = values[i][1]
            level.append(actionTmpDict)
        return level

    def blueprint_2_video(self):
        cburlclass = urllib.parse.urlparse(self._apiurl)

        data = json.dumps(self._blueprint)
        params = bytes(data, 'utf-8')
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        try:
            conn = http.client.HTTPConnection(host=cburlclass.hostname, port=cburlclass.port, timeout=500)
            conn.request("POST", cburlclass.path, params, headers)
            response = conn.getresponse()
            # print
            # response.status, response.reason
            data = response.read()
            print(data)
            dataDict = json.loads(data.decode("utf-8"))
            self._outputVideo = dataDict["data"].get("outputurl", None)
            self._outputAlpha = dataDict['data'].get("outputAlphaurl", None)
        except Exception as ex:
            print("error blueprint_2_video : ", str(ex))
            return 'err'
        else:

            print(type(data))


            conn.close()
        return 'ok'

    def save_2_blueprint(self, bpFileName):
        with open(bpFileName, "wt", encoding="utf-8") as fp:
            json.dump(self._blueprint, fp)
        return

    @staticmethod
    def get_elementType_fromValue(elementValue):
        nameExt = os.path.splitext(elementValue)
        extLower = nameExt[1].lower()
        if (extLower in BPConfig.g_gifType_list):
            return 'gif'
        elif (extLower in BPConfig.g_imageType_list):
            return 'image'
        elif (extLower in BPConfig.g_videoType_list):
            return 'video'
        else:
            raise Exception("不支持的文件类型")

def make_Video(BPClass, *args, **kwargs):
    print("args : ", args)
    baseUElement = BPClass(*args, **kwargs)
    bpDict = baseUElement.run()
    print(bpDict)
    baseUElement.blueprint_2_video()
    outputDict = dict()
    outputDict['outputVideo'] = baseUElement._outputVideo
    outputDict['outputAlpha'] = baseUElement._outputAlpha
    return outputDict

def make_Video_asyn(BPClass, *args):
    t = BPThread.BPThread(make_Video, BPClass, *args)
    t.setDaemon(True)
    t.start()
    return t

def make_Video_asyn_join(t):
    return t.join()

####   A simple sample
class CSample(CBlueprintBase):
    def __init__(self):
        super(CSample, self).__init__("sample")

    def init_outputDesc(self):
        width = 720
        height = 1280
        outputLocation = "*"
        outputAlphaLocation = ".avi"
        fps = 25.0
        duration = 9000
        bgColor = "RGBA(0,0,0,255)"
        self._outputDesc = outputDesc.create(width, height, outputLocation, outputAlphaLocation, fps, duration, bgColor)

    def init_level(self):
        configDict = dict()
        configDict['id'] = 0
        configDict['name'] = "effect"
        configDict['actionNumber'] = 2
        configDict['elementNames'] = [self._elementNameFormat.format(configDict['name'], i) for i in range(configDict['actionNumber'])]
        configDict['newlevel_func'] = self.newLevel_effect_Func
        configDict['newelement_func'] = self.newelement_effect_Func
        configDict['baseTime'] = 20
        self._levelConfigs.append(configDict)

    def newLevel_effect_Func(self, configDict):
        levelName = configDict['name']
        times = [(0, 3000), (6000, 9000)]
        baseActionDict = {
            "name": levelName,
            "element": configDict['elementNames'],
            "startTime": times[0][0],
            "endTime": times[0][1],
            "track" : self.getResource("track", configDict)
        }

        level = self.create_level_from_action(baseActionDict, configDict, times, element=configDict['elementNames'])
        return level

    def newelement_effect_Func(self, configDict):
        elementNames = configDict['elementNames']

        for i, name in enumerate(elementNames):
            elementDict = dict()
            elementDict['name'] = name
            elementDict['source'] = "user"
            elementDict['type'] = "video"
            elementDict['value'] = self.getResource("element", configDict, subType="video")
            self._elements.append(elementDict)
        return

    def fill_resource(self):
        self._resource['##bgmusic'] = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/res/duopai/jiezoubg.mp3"
        self._resource['##ELEMENT-effect-video'] = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/video/mv_4.mp4"
        self._resource['##TRACK-effect'] = "https://videofactory.oss-cn-shanghai.aliyuncs.com/ios/res/duopai/track/t1.txt"


def main():
    bpSample = CSample()
    bpDict = bpSample.run()
    print(bpDict)
    bpSample.blueprint_2_video()
    # bpSample.save_2_blueprint("D:\\workroom\\testroom\\hypnos-v2\\sample//sample.json")

if __name__=="__main__":
    main()
