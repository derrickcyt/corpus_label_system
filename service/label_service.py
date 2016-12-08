# -*- coding:utf-8 -*-
from dao import mysql, mongo
import time
import threading

# 防止多个人访问同一条评论导致冲突，缓存评论id，若超时则释放
LABEL_TIMEOUT = 5 * 60
labeling_cache = dict()
# 互斥锁
lock = threading.Lock()


def update_cache():
    del_list = list()
    for review_id, start_time in labeling_cache.items():
        if time.time() - start_time > LABEL_TIMEOUT:
            del_list.append(review_id)
    for review_id in del_list:
        labeling_cache.pop(review_id)


def get_unlabeled_review(project_id, check_num=100):
    sql = "select review_id,content,project_id from review_list where project_id='%s' and is_labeled=0 limit %s" % (
        str(project_id), str(check_num))
    lock.acquire()
    update_cache()
    result = mysql.query(sql)
    for item in result:
        if item[0] not in labeling_cache:
            labeling_cache[item[0]] = time.time()
            lock.release()
            return Review(item[0], item[1], item[2])
    get_unlabeled_review(check_num + 100)


def get_review_info_by_id(review_id):
    sql = "select content, project_id from review_list where review_id='%s'" % review_id
    result = mysql.query(sql)
    for item in result:
        return Review(review_id, item[0], item[1])


def set_label_flag(is_labeled, review_id):
    sql = "update review_list set is_labeled=%s where review_id=%s" % (is_labeled, review_id)
    return mysql.execute(sql)


def labeled_num(project_id):
    sql = "select count(*) from review_list where project_id=%s and is_labeled=1" % project_id
    return mysql.query(sql)[0][0]


def corpus_num(project_id):
    sql = "select count(*) from review_list where project_id=%s" % project_id
    return mysql.query(sql)[0][0]


def useless_num(project_id):
    sql = "select count(*) from review_list where project_id=%s and is_labeled=2" % project_id
    return mysql.query(sql)[0][0]


def mg_save_label(json_data, review_info):
    mg_col = mongo.get_col(str(review_info.project_id))
    insert_data = {
        "review_id":review_info.review_id,
        "content":review_info.content,
        "label":json_data
    }
    mg_col.insert(insert_data)
    set_label_flag(1,review_info.review_id)


class Review(object):
    def __init__(self, review_id, content, project_id):
        self.review_id = review_id
        self.content = content
        self.project_id = project_id

# print get_unlabeled_review(1)[0]
# set_label_flag(1,1)
# print labeled_num(1)
# print corpus_num(1)
print get_review_info_by_id(1)
