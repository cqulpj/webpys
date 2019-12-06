#coding=utf-8

import os
import web
import time
import sqlite3 as db
from web.contrib.template import render_jinja
import dealops

urls = (
        '/', 'index',
        '/add', 'add',
        '/(\d+)', 'index'
        )

perp = 4
#render = web.template.render('templates')
render = render_jinja(
        'templates',
        encoding='utf-8',
        )

render._lookup.globals.update(
        page_iter = dealops.page_iter,
        )

class index:
    def GET(self, page=1):
        #实例化sqldb，然后读取内容
        s = ''
        db = web.database(dbn='sqlite', db='./msg.db')
        
        page = 1 if (page=='') else int(page)
        offset = (page - 1) * perp
        rt = db.select('msgs', order='id', what='id, content, date, name', offset=offset, limit=perp)
        rc = db.query("SELECT COUNT(*) AS count FROM msgs")[0]
        print(rc)
        pages = rc.count / perp
        pages = (pages + 1) if (rc.count % perp > 0) else pages
        if page > pages:
            raise web.seeother('/')
        else:
            return render.index(rcs=rt, pages=pages, page=page)

class add:
    def POST(self):
        db = web.database(dbn='sqlite', db='./msg.db')
        i = web.input('content')
        n = web.input('user')
        #print(i, n)
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        rc = db.query("SELECT COUNT(*) AS count FROM msgs")[0]
        db.insert('msgs', id=rc.count+1, name=n.user, date=now, content=i.content)

        cp = (rc.count+1) / perp
        cp = (cp + 1) if ((rc.count+1) % perp > 0) else cp
        print('cnt=', rc.count+1, 'cp=', cp)
        return web.seeother('/'+str(cp))

    def GET(self):
        return web.seeother('/')


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
    app = web.application(urls, globals())
    app.run()

