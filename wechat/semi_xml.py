

import re
import codecs

ESCAPE_SEQUENCE_RE = re.compile(r'''
    ( \\U........      # 8-digit hex escapes
    | \\u....          # 4-digit hex escapes
    | \\x..            # 2-digit hex escapes
    | \\[0-7]{1,3}     # Octal escapes
    | \\N\{[^}]+\}     # Unicode characters by name
    | \\[\\'"abfnrtv]  # Single-character escapes
    )''', re.UNICODE | re.VERBOSE)

def decode_escapes(s):
    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')

    return ESCAPE_SEQUENCE_RE.sub(decode_match, s)

def read_semi(data):
    #data=data.decode("raw_unicode_escape")
    result={}
    pivot=len("~SEMI_XML~")
    def get_length():
        if max_len<pivot+2:
            return 0
        hb=data[pivot:pivot+1]
        lb=data[pivot+1:pivot+2]
        length=(ord(hb)*(2**16)+ord(lb))  
        #print(length)
        return length
    max_len=len(data)
    while pivot<max_len:
        lk=get_length()
        pivot+=2
        key=data[pivot:pivot+lk]
        pivot+=lk
        lv=get_length()
        pivot+=2
        val=data[pivot:pivot+lv]
        pivot+=lv
        result[key]=val        
    
    res_title_lst=[]
    res_digest_lst=[]
    for key,val in sorted(result.iteritems(),key=lambda x: x[0]):
        if key.find("digest")>0:
            res_str=u"Digest {}".format(val)
            res_digest_lst.append(res_str)
        elif  key.find("title")>0:
            res_str=u"Title {}".format(val)        
            res_title_lst.append(res_str)
    res_str_lst=[]
    for t,d in zip(res_title_lst,res_digest_lst):
        res_str_lst.extend([t,d])
    return res_str_lst

if __name__=="__main__":   
    d='~SEMI_XML~\x00\'.msg.appmsg.mmreader.category.item4.url\x00\xc7http://mp.weixin.qq.com/s?__biz=MzA5NzIwMjQzMA==&mid=2649947452&idx=5&sn=01c13a65403289f4d315eba65bef351e&chksm=88a224adbfd5adbb6fce68feee50d671ebff41d3ab75e7b1d131794cf6fc36e80443b82aa90b&scene=0#rd\x00+.msg.appmsg.mmreader.category.item1.longurl\x00\x00\x006.msg.appmsg.mmreader.category.item.sources.source.name\x00\x07\u5317\u7f8e\u7559\u5b66\u751f\u65e5\u62a5\x00,.msg.appmsg.mmreader.category.item4.pub_time\x00\n1547305027\x00).msg.appmsg.mmreader.category.item4.title\x00$\u6fb3\u6d32\u975e\u6cd5\u5993\u9662\u904d\u5730\u5f00\u82b1\uff0c\u8fd8\u6709\u4e2d\u56fd\u5973\u5b50\u6301\u5b66\u751f\u7b7e\u8bc1\u5356\u6deb\uff01\u80cc\u540e\u539f\u56e0\u4ee4\u4eba\u550f\u5618\u3002\u3002\u3002\x00\x13.msg.appmsg.extinfo\x00\x00\x00).msg.appmsg.mmreader.category.item3.cover\x00\x94http://mmbiz.qpic.cn/mmbiz_jpg/RiacFDBX14xDkAtHQBhuYoE88ialEsFlR1sAqWIhVNFsGk3A8jnXpfEWhcVuUlrEEEiawhZic8m3ia34vYcnPiaDSWRg/300?wxtype=jpeg&wxfrom=0\x004.msg.appmsg.mmreader.category.item3.appmsg_like_type\x00\x010\x00*.msg.appmsg.mmreader.category.item5.fileid\x00\t502463747\x00*.msg.appmsg.mmreader.category.item1.fileid\x00\t502463800\x00*.msg.appmsg.mmreader.category.item3.fileid\x00\t502463777\x002.msg.appmsg.mmreader.category.item3.sources.source\x00\x19\n                        '
 
    print(read_semi(d))
    