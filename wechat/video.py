import os
from subprocess import PIPE, Popen, call
import logging
from PIL import Image
import cStringIO

from common.textutil import get_file_b64

import pysox

import subprocess as sp
import json
import base64

JPEG_QUALITY=50

logger = logging.getLogger(__name__)

def probe(vid_file_path):
    ''' Give a json from ffprobe command line

    @vid_file_path : The absolute (full) path of the video file, string.
    '''
    if type(vid_file_path) != str:
        raise Exception('Gvie ffprobe a full file path of the video')
        return

    command = ["ffprobe",
            "-loglevel",  "quiet",
            "-print_format", "json",
             "-show_format",
             "-show_streams",
             vid_file_path
             ]
    print(" ".join(command))
    pipe = sp.Popen(command, stdout=sp.PIPE, stderr=sp.STDOUT)
    out, err = pipe.communicate()
    return json.loads(out)

def duration(vid_file_path):
    ''' Video's duration in seconds, return a float number
    '''
    _json = probe(vid_file_path)

    if 'format' in _json:
        if 'duration' in _json['format']:
            return float(_json['format']['duration'])

    if 'streams' in _json:
        # commonly stream 0 is the video
        for s in _json['streams']:
            if 'duration' in s:
                return float(s['duration'])

    # if everything didn't happen,
    # we got here because no single 'return' in the above happen.
    raise Exception('I found no duration')
    #return None

def parse_wechat_video_file(path):
    return get_file_b64(path),duration(path)
    
def parse_wechat_video_thumb(path):
    for suffix in ["png","jpg","jpeg"]:
        if os.path.exists(path+"."+suffix):
            im=Image.open(path+"."+suffix)
            buf = cStringIO.StringIO()
            try:
                im.save(buf, 'JPEG', quality=JPEG_QUALITY)
            except IOError:
                try:
                    # sometimes it works the second time...
                    im.save(buf, 'JPEG', quality=JPEG_QUALITY)
                except IOError:
                    return None
            jpeg_str = buf.getvalue()
            return base64.b64encode(jpeg_str)
    return None
        