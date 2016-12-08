# -*- coding:utf-8 -*-
from dao import mysql, mongo
import codecs

BATCH_NUM = 2000


def db_save_new_project(project_name, username, project_type, domain, filename, desc, lang):
    sql = "insert into project_list (project_name,username,filename,domain,type,description,lang) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (
        project_name, username, filename, domain, project_type, desc, lang)
    print sql
    mysql.execute(sql)


def mg_create_new_col(category_scheme_str, project_id):
    mongo.create_col(str(project_id))
    mg_save_category_scheme(category_scheme_str, str(project_id))


def db_query_project_id(project_name):
    sql = "select project_id from project_list where project_name='%s'" % (project_name)
    result = mysql.query(sql)
    if result:
        return result[0][0]


def db_save_file(filepath, project_id):
    sql = "insert into review_list (content,project_id) VALUES (%s,%s)"
    with codecs.open(filepath, "r", "utf-8") as in_f:
        data = list()
        count = 0
        for line in in_f:
            review = line.strip().encode("utf-8")
            print review
            data.append((review, project_id))
            count += 1
            if count % BATCH_NUM == 0:
                mysql.batch_insert(sql, data)
                data = list()


def mg_save_category_scheme(category_scheme_str, col_name):
    categories = [x for x in category_scheme_str.split("\n") if x.strip()]
    insert_data = {
        "type": "category_scheme",
        "scheme": categories
    }
    mongo.get_col(col_name).insert(insert_data)


def del_project(project_id):
    mongo.db.drop_collection(str(project_id))
    sql = "delete from review_list where project_id=%s"%project_id
    mysql.execute(sql)
    sql = "delete from project_list where project_id=%s"%project_id
    mysql.execute(sql)