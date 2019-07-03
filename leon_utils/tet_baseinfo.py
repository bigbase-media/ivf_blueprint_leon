# -*- coding: utf-8 -*-

import platform, subprocess, json, os
import vc_tools

codec_name_image_list = ['jpg', 'jpeg', 'bmp', 'tif', 'png', 'gif', 'tga', 'ico', 'mjpeg']


def geturlMediaInfo(url):
    baseinfo = {}
    baseinfo['filesize'] = vc_tools.get_file_size(url)

    if (platform.system()=='Windows'):
        command = ["ffprobe","-loglevel","quiet","-print_format","json","-show_format","-show_streams","-i",url]
    else:
        command = "ffprobe -loglevel quiet -print_format json -show_format -show_streams -i " +  url
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = result.stdout.read()
    # print(str(out))
    print(json.loads(out.decode('utf-8')))
    streams = json.loads(out.decode("utf-8"))["streams"]
    for stream in streams:
        if (stream['codec_type'] == "video"):
            videoinfo = {}
            videoinfo['width'] = stream['width']
            videoinfo['height'] = stream['height']
            videoinfo['codec_name'] = stream['codec_name']
            videoinfo['duration'] = stream['duration']
            videoinfo['bit_rate'] = stream['bit_rate']
            videoinfo['frame_number'] = stream['nb_frames']
            tags = stream.get('tags', None)
            if (tags is None):
                videoinfo['rotate'] = 0
            else:
                videoinfo['rotate'] = int(stream['tags'].get("rotate", 0))
            fr = stream['r_frame_rate']
            fr_list = str(fr).split('/')
            if (len(fr_list) == 2):
                videoinfo['frame_rate'] = float(fr_list[0]) / float(fr_list[1])
            else:
                videoinfo['frame_rate'] = float(fr_list[0])
            baseinfo['video'] = videoinfo
        if (stream['codec_type'] == "audio"):
            audioinfo = {}
            audioinfo['duration'] = stream['duration']
            audioinfo['codec_name'] = stream['codec_name']
            audioinfo['bit_rate'] = stream['bit_rate']
            audioinfo['sample_rate'] = stream['sample_rate']
            audioinfo['channels'] = stream['channels']
            baseinfo['audio'] = audioinfo

    return baseinfo

def get(localvideo):
    baseinfo = { }
    if (os.path.isfile(localvideo)!=True):
        return None
    filesize = os.path.getsize(localvideo)
    if (filesize<=0):
        return None

    if (platform.system()=='Windows'):
        command = ["ffprobe","-loglevel","quiet","-print_format","json","-show_format","-show_streams","-i",localvideo]
    else:
        command = "ffprobe -loglevel quiet -print_format json -show_format -show_streams -i " +  localvideo
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = result.stdout.read()
    # print(str(out))
    # print(json.loads(out.decode('utf-8')))
    try:
        streams = json.loads(out.decode("utf-8"))["streams"]
        for stream in streams:
            if (stream['codec_type']=="video"):
                videoinfo = { }
                videoinfo['width'] = stream['width']
                videoinfo['height'] = stream['height']
                videoinfo['codec_name'] = stream['codec_name']
                tags = stream.get('tags', None)
                if (tags is None):
                    videoinfo['rotate'] = 0
                else:
                    videoinfo['rotate'] = int(stream['tags'].get("rotate", 0))
                print(videoinfo['codec_name'])
                if (videoinfo['codec_name'] not in codec_name_image_list):
                    videoinfo['duration'] = stream['duration']
                    videoinfo['bit_rate'] = stream['bit_rate']
                    videoinfo['frame_number'] = stream['nb_frames']
                fr = stream['r_frame_rate']
                fr_list = str(fr).split('/')
                if (len(fr_list) == 2):
                    videoinfo['frame_rate'] = float(fr_list[0]) / float(fr_list[1])
                else:
                    videoinfo['frame_rate'] = float(fr_list[0])
                baseinfo['video'] = videoinfo
            if (stream['codec_type']=="audio"):
                audioinfo = { }
                audioinfo['duration'] = stream['duration']
                audioinfo['codec_name'] = stream['codec_name']
                audioinfo['bit_rate'] = stream['bit_rate']
                audioinfo['sample_rate'] = stream['sample_rate']
                audioinfo['channels'] = stream['channels']
                baseinfo['audio'] = audioinfo
    except Exception as e:
        print("err: tet_baseinfo get fail")
        print("except err : %s" % str(e))
        return None
    else:
        return baseinfo

def getAudioInfo(localvideo):
    audioinfo = {}
    if (os.path.isfile(localvideo) != True):
        return None
    filesize = os.path.getsize(localvideo)
    if (filesize <= 0):
        return None

    if (platform.system() == 'Windows'):
        command = ["ffprobe", "-loglevel", "quiet", "-print_format", "json", "-show_format", "-show_streams", "-i",
                   localvideo]
    else:
        command = "ffprobe -loglevel quiet -print_format json -show_format -show_streams -i " + localvideo
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = result.stdout.read()
    print(str(out))
    print(json.loads(out.decode('utf-8')))
    streams = json.loads(out.decode("utf-8"))["streams"]
    for stream in streams:
        if (stream['codec_type']=="video"):
            continue
        if (stream['codec_type']=="audio"):
            audioinfo['duration'] = stream['duration']
            audioinfo['codec_name'] = stream['codec_name']
            audioinfo['bit_rate'] = stream['bit_rate']
            audioinfo['sample_rate'] = stream['sample_rate']
            audioinfo['channels'] = stream['channels']
    return audioinfo

if __name__=="__main__":
    print("hi, this is baseinfo test program")
    bi = get("http://v4.qutoutiao.net/toutiao_video_zdgq_online/09b60562e35f4af5a6c23633260b7863/ld.mp4")
    print(bi)
    print(bi['video']["rotate"])
