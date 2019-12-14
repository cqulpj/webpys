#coding=utf-8

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

if __name__ == '__main__':
    mdb = sqldb()
    mdb.initdb()

