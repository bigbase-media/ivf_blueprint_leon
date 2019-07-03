# -*- coding: utf-8 -*-

import os, sys, importlib, http
import subprocess, json, urllib
import platform, shutil
from urllib import request

def send_msg_to_oa(name_list, msg):
    for name in name_list:
        url = "http://mcloud.d.ywopt.com/wx/sendtext"
        # url = "http://themis.innotechx.com/cbtest"
        urlclass = urllib.parse.urlparse(url)
        msgdict = { "WXName" : name, "WXText" : msg}
        print(msgdict)
        data = json.dumps(msgdict)
        params = bytes(data, 'utf-8')
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        try:
            conn = http.client.HTTPConnection(host=urlclass.hostname, port=urlclass.port, timeout=2)
            conn.request("POST", urlclass.path, params, headers)
            response = conn.getresponse()
            print(response)
            # print
            # response.status, response.reason
            data = response.read()
            print(data)
        except Exception as ex:
            print(str(ex))
            return 'err'
        else:
            conn.close()

    return 'ok'

# """通过content-length头获取文件大小
# url - 目标文件URL
# proxy - 代理
# """
def get_file_size(url, proxy=None):
    opener = urllib2.build_opener()
    if proxy:
        if url.lower().startswith('https://'):
            opener.add_handler(urllib2.ProxyHandler({'https': proxy}))
        else:
            opener.add_handler(urllib2.ProxyHandler({'http': proxy}))
    request = urllib2.Request(url)
    request.get_method = lambda: 'HEAD'
    try:
        response = opener.open(request)
        response.read()
    except Exception, e:
        print '%s %s' % (url, e)
        return 0
    else:
        return dict(response.headers).get('content-length', 0)

def get_localip_str():
    import socket;
    return str([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
           [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])

def downloadUrl(url, localfile):
    importlib.reload(sys)  # 2
    # sys.setdefaultencoding('utf-8')  # 3

    try:
        # url = url.encode('utf-8')
        # print("url: ", url)
        urllib.request.urlretrieve(url, localfile)
    except IOError:
        return "err"
    else:
        fsize = os.path.getsize(localfile)
        if (fsize == 0):
            return "err"
        return "ok"

def downloadUrl_2(url, localfile):
    import urllib3

    http = urllib3.PoolManager()
    # url = 'https://raw.githubusercontent.com/abidrahmank/OpenCV2-Python-Tutorials/master/data/left.jpg'
    try:
        r = http.request('GET', url, timeout=10)
        with open(localfile, "wb") as code:
            code.write(r.data)
    except Exception as e:
        return 'err'
    else:
        return 'ok'

def downloadUrl_retry(url, local, times=1):
    for i in range(0, times+1):
        if (downloadUrl_2(url, local)=='ok'):
            return 'ok'
    return 'err'

def modify_suffix(src_suffix):
    pos = src_suffix.find('?')
    if (pos<0):
        return src_suffix
    else:
        return src_suffix[0:pos]

def main():
    url = "http://v2.quduopai.cn/qdp-sjsp-mp4-hd/ea085b7c3ce8487fad2a0a1457f81d32/hd.mp4?_v=11446"
    localname = "d://" + 'userElements-' + str(1) + \
                modify_suffix(os.path.splitext(url)[1])
    # modify_suffix(".mp4")

    print(localname)
    ret = downloadUrl(url, localname)
    print(ret)

def download_csv(csvName):
    videoDir = "D:\\workroom\\dataset-3\\meaningless-video\\video\\"
    with open(csvName, 'rt') as fp_csv:
        lines = fp_csv.readlines()

    for i, line in enumerate(lines):
        url = line.replace("\n", "")
        localvideo = videoDir + "bad-" + str(i) + ".mp4"
        downloadUrl_2(url, localvideo)


if __name__ == '__main__':
    csvName = "D:\\workroom\\dataset-3\\meaningless-video\\bad.csv"
    download_csv(csvName)


