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
        '/index.html', 'index',
        '/page/(\d+)', 'page',
        '/post/(\d+)', 'post',
        '/install', 'install',
        '/login', 'login',
        '/register', 'register',
        '/logout', 'logout',
        '/createpost', 'createpost',
        )

# 每页博文数
perp = 3

# 数据库
db = models.sqldb()

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
        raise web.seeother('/page/1')
        #return render.index()

# 首页/某页博文
class page:
    def GET(self, page=1):
        cur = int(page)
        total = db.count_posts()
        pages = (total / perp) + (total % perp != 0)
        pts = db.query_posts(perp, cur)
        return render.index(cp=cur, pages=pages, pts=pts)

# 文章视图函数
class post:
    def GET(self, postid=1):
        post = db.get_post_byID(postid)
        post.content = post.content.replace('\n', '<br>')
        return render.post(post=post)

# 安装/初始化数据库视图函数
class install:
    def GET(self):
        if db.initdb():
            return '<head><meta charset="utf-8"></head><body><h1>数据库初始化成功</h1></body>'
        else:
            return '<head><meta charset="utf-8"></head><body><h1>数据库已存在</h1></body>'

# 登录
class login:
    def GET(self):
        return render.login(LoginTips=u'请登录')

    def POST(self):
        i = web.input()
        user = i.get('Name')
        pswd = i.get('Password')
        print(user,pswd)
        ret = db.query_user_byname(user)
        if (ret!=None) and (ret.password == pswd):
            session.logged_in = True
            session.user = user
            session.userid = ret.id
            print('ok,loginin')
            raise web.seeother('/')
        else:
            print('fail,error')
            return render.login(LoginTips=u'用户名或密码错误')

# 注销
class logout:
    def GET(self):
        session.logged_in = False
        raise web.seeother('/')

# 注册用户
class register:
    def GET(self):
        return render.register(LoginTips=u'注册')

    def POST(self):
        i = web.input()
        user = i.get('Name')
        pswd = i.get('Password')
        email = i.get('Email')
        print(user, pswd, email)
        ret = db.create_user(user, pswd, email)
        if ret:
            return '<head><meta charset="utf-8"></head><body><h1>注册成功！</h1></body>'
        else:
            return '<head><meta charset="utf-8"></head><body><h1>注册失败.</h1></body>'

# 增加博文
class createpost:
    def GET(self):
        cts = db.query_categorys()
        return render.createpost(cates=cts)

    def POST(self):
        if session.logged_in:
            i = web.input()
            title = i.get('title')
            content = i.get('content')
            cate = i.get('category')
            userid = session.userid
            ret = db.create_post(userid, title, content, cate)
            if ret:
                return '<head><meta charset="utf-8"></head><body><h1>添加成功！</h1></body>'
            else:
                return '<head><meta charset="utf-8"></head><body><h1>添加失败.</h1></body>'
        else:
            raise web.seeother('/login')
    
if __name__ == '__main__':
    app.run()

