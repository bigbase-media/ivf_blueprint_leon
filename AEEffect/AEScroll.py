# -*- coding: utf-8 -*-

import sys
import os, json
import urllib, http.client

class CAEScroll():
    def __init__(self, userImage_jpg, *args):
        self._apiurl = "http://hypnos-ae.innotechx.com/task"
        self._input_jpg = userImage_jpg
        self._outputVideo = None
        self._outputAlpha = None

    def run(self):
        if (os.path.splitext(self._input_jpg)[1].lower()!=".jpg"):
            print('image type is not .jpg ')
            return 'err'
        aeDescDict = dict()
        aeDescDict['aeType'] = "luoyebingfen"
        aeDescDict['token'] = 'leon'
        userElements = []
        userElement = dict()
        userElement['elementName'] = 'userImage'
        userElement['value'] = self._input_jpg
        userElements.append(userElement)
        aeDescDict['userElements'] = userElements
        outputDict = self.hypnos_ae(aeDescDict)
        if (outputDict is None):
            print("hypnos ae fail")
            return 'err'
        self._outputVideo = outputDict['data']['outputurl']
        return 'ok'

    def hypnos_ae(self, aeDescDict):
        cburlclass = urllib.parse.urlparse(self._apiurl)

        data = json.dumps(aeDescDict)
        params = bytes(data, 'utf-8')
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        try:
            conn = http.client.HTTPConnection(host=cburlclass.hostname, port=cburlclass.port, timeout=500)
            conn.request("POST", cburlclass.path, params, headers)
            response = conn.getresponse()
            if (response.status!=200):
                print("wrong status")
                return None
            # print
            # response.status, response.reason
            data = response.read()
            dataDict = json.loads(data.decode("utf-8"))
        except Exception as ex:
            print("error hypnos_ae : ", str(ex))
            return None
        else:
            # print(type(data))
            conn.close()
        return dataDict

def main():
    image_jpg = "https://cgptest.oss-cn-shanghai.aliyuncs.com/meise/2.jpg"
    handle = CAEScroll(image_jpg)
    output = handle.run()
    print(output)
    print(handle._outputVideo)

if __name__=="__main__":
    main()
