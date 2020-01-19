#coding=utf-8

import os
import web
import time
import json
import base64
from web.contrib.template import render_jinja
import dealops
from apis import *

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


if __name__ == '__main__':
    app.run()

