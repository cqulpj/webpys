#coding=utf-8

import os
import web
import time
import sqlite3 as db

urls = (
        '/', 'index',
        '/add', 'add'
        )

render = web.template.render('templates')

class index:
    def GET(self):
        #实例化sqldb，然后读取内容
        s = ''
        db = sqldb()
        rt = db.cu.execute('''
            select id, content, date, name from msgs
            ''')
        rc = db.cu.fetchall()
        #print('rc:', rc)
        #print(dir(rc))
        return render.index(rc)

class add:
    def POST(self):
        j = 0
        i = web.input('content')
        n = web.input('user')
        print(i, n)
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        db = sqldb()
        rt = db.cu.execute('''
            select * from msgs
            ''')
        rc = db.cu.fetchall()
        for k in rc:
            j = k[0] + 1
        t = (j, n.user, date, i.content)
        print('t=:', t)
        db.cu.execute('''
            insert into msgs values(?,?,?,?)''', t)
        db.conn.commit()
        return web.seeother('/')

    def GET(self):
        return web.seeother('/')

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
    app = web.application(urls, globals())
    app.run()

