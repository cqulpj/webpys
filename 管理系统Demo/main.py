#coding=utf-8

import os
import web
import time
import sqlite3 as db
from web.contrib.template import render_jinja
import dealops

# 定义路径解析
urls = (
        '/', 'index',
        '/login', 'login',
        '/logout', 'logout'
        )

# 每页条数
perp = 4

# 使用Jinja模板系统
render = render_jinja(
        'templates',
        encoding='utf-8',
        )

# 传入全局函数
render._lookup.globals.update(
        page_iter = dealops.page_iter,
        )

# 关闭调试（为了使用session）
web.config.debug = False

# 创建app
app = web.application(urls, globals())

# 使用session
session = web.session.Session(app, web.session.DiskStore('sessions'))

# 有效的用户名密码
allowed = (
        ('admin', 'admin'),
        ('lpj', '123456'))

class index:
    def GET(self):
        if session.get('logged_in', False):
            return render.index()
        raise web.seeother('/login')

class login:
    def POST(self):
        i = web.input()
        user = i.get('Name')
        pswd = i.get('Password')
        print(user,pswd)
        if (user, pswd) in allowed:
            session.logged_in = True
            session.user = user
            print('ok,loginin')
            raise web.seeother('/')
        else:
            print('fail,error')
            return render.login(LoginTips=u'用户名或密码错误')

    def GET(self):
        return render.login(LoginTips=u'请登录')

class logout:
    def GET(self):
        session.logged_in = False
        raise web.seeother('/login')


# 初始化数据库
class sqldb:
    def __init__(self):
        self.conn = db.connect("./msg.db")
        self.cu = self.conn.cursor()
        try:
            self.cu.execute('''
                create table msgs(
                    id integer primary key,
                    name text,
                    date text,
                    content text)
                    ''')
            self.conn.commit()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    sqldb()
    app.run()

