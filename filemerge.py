from shutil import copyfile
from shutil import copystat

import ffmpeg
import imghdr
import os
import re
import subprocess

def merge(src_path,dst_path,pattern="\\w*",convert=None):
    def default_convert(file_name,useless):
        return file_name
    if convert is None:
        convert=default_convert
    file_list=os.listdir(src_path)
    for file_name in file_list:
        print(file_name)
        full_path=os.path.join(src_path,file_name)
        if os.path.isfile(full_path):
            if re.match(pattern,file_name) is not None:
                dst_full_path=os.path.join(dst_path,convert(file_name,full_path))
                if file_name[-4:]==".amr":
                    dst_full_path=dst_full_path[:-3]+"mp3"
                    tmp_full_path=full_path[:-3]+"pcm"
                    dir_path = os.path.dirname(os.path.realpath(__file__))
                    print(os.path.join(dir_path,full_path))
                    try:
                        subprocess.run("""silk_v3_decoder.exe "%s" "%s" """%(full_path,tmp_full_path))
                        subprocess.run("""ffmpeg -y -f s16le -ar 24000 -ac 1 -i "%s" "%s" """%(tmp_full_path,dst_full_path))
                        copystat(full_path,dst_full_path)
                    except Exception as e:
                        print(e)
                        pass
                else:
                    print(full_path,dst_full_path)
                    copyfile(full_path,dst_full_path)
                    copystat(full_path,dst_full_path)
        else:
            merge(full_path,dst_path,pattern=pattern,convert=convert)

def parser(path,full_path):
    suffix=imghdr.what(full_path)
    if path.find(".")>=0:
        path=path[:path.find(".")]
    if len(path)==0:
        path="Empty"
    if suffix is None:
        suffix=""
    return path+"."+suffix
            
if __name__=="__main__":
    merge("image2","backup\\image","\\w*",parser)
    merge("video","backup\\video","\\w*.mp4")
    merge("voice2","backup\\voice","\\w*")