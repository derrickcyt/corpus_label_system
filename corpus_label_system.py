# -*- coding:utf-8 -*-
from flask import Flask, render_template, request
from service import new_project, label_service, project_service
import sys
import json

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)

UPLOAD_FOLDER = r"D:\PythonProjects\corpus_label_system\temp\\"


@app.route('/')
def home_page():
    project_list = project_service.get_all_project()
    return render_template("index.html", project_list=project_list)


@app.route("/project/<int:project_id>")
def project_home(project_id):
    project_info = project_service.get_project_info(project_id)
    corpus_num = label_service.corpus_num(project_id)
    labeled_num = label_service.labeled_num(project_id)
    useless_num = label_service.useless_num(project_id)
    category_scheme = project_service.get_opinion_category_scheme(project_id)
    return render_template("project_home.html", project_info=project_info, corpus_num=corpus_num,
                           labeled_num=labeled_num, useless_num=useless_num, category_scheme=category_scheme)


@app.route("/project/<int:project_id>/browser")
def project_browser(project_id):
    browser_list = project_service.mg_get_all_labels(project_id)
    project_info = project_service.get_project_info(project_id)
    return render_template("project_browser.html", browser_list=browser_list,project_info=project_info)


@app.route("/project/<int:project_id>/label")
def label_page(project_id):
    project_info = project_service.get_project_info(project_id)
    ready_review = label_service.get_unlabeled_review(project_id)
    category_scheme = [(i, x) for i, x in enumerate(project_service.get_opinion_category_scheme(project_id))]
    return render_template("custom_label_page/opinion_mining.html", ready_review=ready_review,
                           project_info=project_info, category_scheme=category_scheme)


@app.route("/label/submit", methods=["POST"])
def label_submit():
    if request.method == "POST":
        review_id = request.form["review_id"]
        submit_type = request.form["submit_type"]
        if submit_type == "neglect":
            label_service.set_label_flag(2, review_id)
            return "SUCCESS"
        elif submit_type == "labeled":
            json_data = json.loads(request.form["json_data"])
            review_info = label_service.get_review_info_by_id(review_id)
            print json_data
            label_service.mg_save_label(json_data, review_info)
            return "SUCCESS"


@app.route("/new")
def new_project_page():
    return render_template("project_new.html")


@app.route("/new/upload", methods=["POST"])
def new_project_submit():
    if request.method == 'POST':
        project_name = request.form["project_name"]
        user_name = request.form["user_name"]
        project_type = request.form['project_type']
        domain = request.form["domain"]
        desc = request.form["desc"]
        lang = request.form["lang"]
        category_scheme_str = request.form["category_scheme"]
        f = request.files["corpus_file"]
        filename = project_name + "_" + user_name + "_" + project_type + "_" + domain + ".txt"
        f.save(UPLOAD_FOLDER + filename)
        if new_project.db_query_project_id(project_name):
            return "项目名称已存在"
        new_project.db_save_new_project(project_name, user_name, project_type, domain, filename, desc, lang)
        project_id = new_project.db_query_project_id(project_name)
        print project_id
        new_project.mg_create_new_col(category_scheme_str, project_id)
        new_project.db_save_file(UPLOAD_FOLDER + filename, project_id)
    return "创建成功"


@app.route("/del/project", methods=["POST"])
def del_project():
    if request.method == 'POST':
        project_id = request.form["project_id"]
        new_project.del_project(project_id)
        return "SUCCESS"

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
