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

    # 增加博文
    def create_post(self, userid, title, content, category):
        try:
            wdb = web.database(dbn='sqlite', db='./blogcms.db')
            rt = wdb.insert('post', authorid=userid, title=title, content=content, category=category)
            return True
        except Exception as e:
            print(e)
            return False

    # 查询文章总数
    def count_posts(self):
        try:
            wdb = web.database(dbn='sqlite', db='./blogcms.db')
            rt = wdb.query('select count(*) as total from post')
            return rt[0].total
        except Exception as e:
            print(e)
            return None

    # 查询某页博文
    # perp:每页文章数
    # cur:第几页
    def query_posts(self, perp, cur):
        try:
            wdb = web.database(dbn='sqlite', db='./blogcms.db')
            rt = wdb.query('select post.id,title,content,post.createat,user.name from \
                    post,user where post.authorid=user.id order by post.createat desc \
                    limit $lm offset $of', vars={'lm':perp, 'of':(cur-1)*perp})
            return rt
        except Exception as e:
            print(e)
            return None

    # 根据ID查询某篇博文
    def get_post_byID(self, postid):
        pid = int(postid)
        try:
            wdb = web.database(dbn='sqlite', db='./blogcms.db')
            rt = wdb.query('select post.id,title,content,post.createat,user.name from \
                    post,user where post.authorid=user.id and post.id=$pid', vars={'pid':pid})
            return rt[0]
        except Exception as e:
            print(e)
            return None

if __name__ == '__main__':
    mdb = sqldb()
    #mdb.initdb()
    #print mdb.query_user_byname('lpj')
    #print mdb.query_user_byname('lpp')
    #print mdb.create_user('wlm', '123456', '')
    print mdb.get_post_byID(3)

