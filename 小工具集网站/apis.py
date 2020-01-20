#coding=utf-8

import web
import time
import json
import base64
import dealops

# 下面是一系列数据转换或编解码API
# hex与ascii字符串互转
class hexascii:
    def POST(self):
        pld = web.input()
        print(pld)
        ret = {}
        try:
            # hex转ascii
            if pld.ops == '0':
                ss = pld.data.strip().replace(' ', '')
                cs = []
                for i in range(0, len(ss), 2):
                    tt = int(ss[i:i+2], 16)
                    cs.append(chr(tt))
                ret['data'] = ''.join(cs).decode('gbk')
                ret['status'] = 'ok'
            # ascii字符串转hex
            elif pld.ops == '1':
                ss = pld.data.strip().encode('gbk')
                d = [hex(ord(i)).upper()[2:4] for i in ss]
                ss = ' '.join(d)
                ret['data'] = ss
                ret['status'] = 'ok'
            # 无效操作
            else:
                ret['status'] = 'invalid ops'
                ret['data'] = ''
        except Exception as e:
            print(e)
            ret['status'] = 'error'
            ret['data'] = ''

        web.header('content-type', 'text/json')
        return json.dumps(ret)

# hex数据的base64编解码
class hexbase64:
    def POST(self):
        pld = web.input()
        print(pld)
        ret = {}
        try:
            # 字符串直接base64编码
            if pld.ops == '0':
                ret['data'] = base64.b64encode(pld.data)
                ret['status'] = 'ok'
            # hex形式数组base64编码
            elif pld.ops == '1':
                ss = pld.data.strip().replace(' ', '')
                cs = []
                for i in range(0, len(ss), 2):
                    tt = int(ss[i:i+2], 16)
                    cs.append(chr(tt))
                ret['data'] = base64.b64encode(''.join(cs))
                ret['status'] = 'ok'
            # base64解码为字符串 
            elif pld.ops == '2':
                ss = pld.data.strip()
                ret['data'] = base64.b64decode(ss)
                ret['status'] = 'ok'
            # base64解码为hex形式数组
            elif pld.ops == '3':
                ss = pld.data.strip()
                ss = base64.b64decode(ss)
                bs = [hex(ord(i)).upper()[2:] for i in ss]
                ret['data'] = ' '.join(bs)
                ret['status'] = 'ok'
            # 无效操作
            else:
                ret['status'] = 'invalid ops'
                ret['data'] = ''
        except Exception as e:
            print(e)
            ret['status'] = 'error'
            ret['data'] = ''

        web.header('content-type', 'text/json')
        return json.dumps(ret)

# 查询汉字内码并转换为HEX形式
# 支持unicode、gbk、utf-8三种编码格式查询
class code2hex:
    def POST(self):
        pld = web.input()
        print(pld)
        ret = {'data':'', 'status':'ok'}
        try:
            # 查询Unicode编码
            if pld.ops.lower() == 'unicode':
                ret['data'] = dealops.unicode2hex(pld.data)
            # 查询gbk编码
            elif pld.ops.lower() == 'gbk':
                ret['data'] = dealops.unicode2hex(pld.data, 'gbk')
            # 查询utf-8编码
            elif pld.ops.lower() in ('utf-8', 'utf8'):
                ret['data'] = dealops.unicode2hex(pld.data, 'utf-8')
            # 无效操作
            else:
                ret['status'] = 'invalid ops'
        except Exception as e:
            print(e)
            ret['status'] = 'error'

        web.header('content-type', 'text/json')
        return json.dumps(ret)

