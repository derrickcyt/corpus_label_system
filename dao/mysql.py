# -*- coding:utf-8 -*-
import MySQLdb


def init_db():
    return MySQLdb.connect('110.64.66.203', 'root', '123456', 'corpus_label', charset="utf8")


def query(sql):
    db = init_db()
    cursor = db.cursor()
    cursor.execute(sql)
    db.close()
    return cursor.fetchall()


def execute(sql):
    db = init_db()
    cursor = db.cursor()
    # print sql
    try:
        cursor.execute(sql)
        db.commit()
    except MySQLdb.Error, e:
        print "Error:%s" % str(e)
        db.rollback()
    finally:
        db.close()


def batch_insert(sql, data):
    db = init_db()
    cursor = db.cursor()
    try:
        cursor.executemany(sql, data)
        db.commit()
    except MySQLdb.Error, e:
        print "Error:%s" % str(e)
        db.rollback()
    finally:
        db.close()
