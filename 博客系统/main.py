#coding=utf-8

import os
import web
import time
from web.contrib.template import render_jinja
import dealops
import models

# 路径映射
urls = (
        '/', 'index',
        '/install', 'install',
        )

# 分页
perp = 4

# 使用Jinja2模板系统
render = render_jinja(
        'templates',
        encoding='utf-8',
        )

# 增加全局函数
render._lookup.globals.update(
        page_iter = dealops.page_iter,
        )

# 数据库
db = models.sqldb()

# 首页视图函数
class index:
    def GET(self):
        return render.index()

# 安装/初始化数据库视图函数
class install:
    def GET(self):
        if db.initdb():
            return '<head><meta charset="utf-8"></head><body>数据库初始化成功</body>'
        else:
            return '<head><meta charset="utf-8"></head><body>数据库已存在</body>'


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()

