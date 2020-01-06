#coding=utf-8

import web
import sqlite3 as db

# 初始化数据库
class sqldb:
    def __init__(self):
        self.conn = db.connect("./blogcms.db")
        self.cu = self.conn.cursor()

    def initdb(self):
        try:
            self.cu.execute('''
                create table user(
                    id integer primary key autoincrement,
                    name varchar(64) not null,
                    password varchar(64) not null,
                    email varchar(64),
                    createat text default (datetime('now'))
                    );
                    ''')
            self.conn.commit()
            print('create user table...')

            self.cu.execute('''
                create table post(
                    id integer primary key autoincrement,
                    authorid integer not null,
                    title text not null,
                    content text,
                    category text,
                    createat text default (datetime('now'))
                    );
                    ''')
            self.conn.commit()
            print('create post table...')

            self.cu.execute('''
                create table category(
                    id integer primary key autoincrement,
                    name text not null,
                    createat text default (datetime('now'))
                    );
                    ''')
            self.conn.commit()
            print('create category table...')

            self.cu.execute('''
                create table comments(
                    id integer primary key autoincrement,
                    author text not null,
                    content text not null,
                    postid integer not null,
                    createat text default (datetime('now')),
                    foreign key (postid) references post(id)
                    );
                    ''')
            self.conn.commit()
            print('create comments table.')
            return True
        except Exception as e:
            print(e)
            return False
    
    # 查询用户名，返回用户记录
    def query_user_byname(self, name):
        myvars = dict(name=name)
        try:
            wdb = web.database(dbn='sqlite', db='./blogcms.db')
            rt = wdb.select('user', order='id', where='name=$name', vars=myvars, limit=1)
            return rt[0]
        except Exception as e:
            #print(e)
            return None

    # 增加用户
    def create_user(self, name, password, email):
        try:
            wdb = web.database(dbn='sqlite', db='./blogcms.db')
            rt = wdb.insert('user', name=name, password=password, email=email)
            return True
        except Exception as e:
            print(e)
            return False

    # 查询类别并返回
    def query_categorys(self):
        try:
            wdb = web.database(dbn='sqlite', db='./blogcms.db')
            rt = wdb.select('category', what='name', order='id')
            return rt
        except Exception as e:
            print(e)
            return None

if __name__ == '__main__':
    mdb = sqldb()
    mdb.initdb()
    print mdb.query_user_byname('lpj')
    print mdb.query_user_byname('lpp')
    print mdb.create_user('wlm', '123456', '')

