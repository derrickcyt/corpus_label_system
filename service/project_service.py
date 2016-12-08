# -*- coding:utf-8 -*-
from dao import mysql, mongo


def get_project_types():
    sql = "select type_id,type_name from project_type_list"
    result = mysql.query(sql)
    type_list = dict()
    for item in result:
        type_list[item[0]] = item[1]
    return type_list


project_types = get_project_types()
project_langs = {"zh": "中文", "en": "英文"}


def get_all_project():
    sql = "select project_id, project_name, domain, type, description, lang from project_list"
    result = mysql.query(sql)
    project_list = list()
    for item in result:
        project_list.append(Project(item[0], item[1], item[2], item[3], item[4], item[5]))
    return project_list


def get_project_info(project_id):
    sql = "select project_id, project_name, domain, type, description, lang from project_list where project_id=%s" % project_id
    result = mysql.query(sql)
    item = result[0]
    if len(result) > 0:
        return Project(item[0], item[1], item[2], item[3], item[4], item[5])


def get_opinion_category_scheme(project_id):
    for item in mongo.get_col(str(project_id)).find({"type": "category_scheme"}):
        return item["scheme"]


def mg_get_all_labels(project_id):
    mgr = mongo.get_col(str(project_id)).find()
    result_list = []
    category_scheme = dict()
    for item in mgr:
        if "type" in item:
            for i, cname in enumerate(item["scheme"]):
                category_scheme[str(i)] = cname
        else:
            pairs_str = ""
            for label in item["label"]:
                if label["type"] == "explicit":
                    pair = label["type"] + ": " + label["aspect"] + "-" + label["opinion"]
                elif label["type"] == "implicit":
                    pair = label["type"] + ": " + label["opinion"]
                else:
                    pair = label["type"] + ": " + label["verb_expression"]
                pair += "\tcategory:" + category_scheme[label["category"]] + "\t" + label["polarity"]
                pairs_str += pair+"\n"
            item["label"] = pairs_str
            result_list.append(item)
    return result_list


class Project(object):
    def __init__(self, project_id, project_name, domain, project_type, description, lang):
        self.project_id = project_id
        self.project_name = project_name
        self.domain = domain
        self.project_type = project_type
        self.description = description
        self.lang = lang


print mg_get_all_labels(1)