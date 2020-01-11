#coding=utf-8

import os
import web
import time
import json
import base64
from web.contrib.template import render_jinja
import dealops

# 路径映射
urls = (
        '/', 'index',
        '/api/hexascii', 'hexascii',
        '/api/hexbase64', 'hexbase64',
        )

# 关闭调试（为了使用session）
web.config.debug = False

# 创建app
app = web.application(urls, globals())

# 使用session
session = web.session.Session(app, web.session.DiskStore('sessions'))
session.logged_in = False

# 使用Jinja2模板系统
render = render_jinja(
        'templates',
        encoding='utf-8',
        )

# 增加全局函数
render._lookup.globals.update(
        page_iter = dealops.page_iter,
        session = session,
        )

# 首页视图函数
class index:
    def GET(self):
        return render.index()

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
                ret['data'] = ''.join(cs)
                ret['status'] = 'ok'
            # ascii字符串转hex
            elif pld.ops == '1':
                ss = pld.data.strip()
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

        return json.dumps(ret)

if __name__ == '__main__':
    app.run()

