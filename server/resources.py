import os

from flask_restful import Resource
from flask import request

from server import app, db
from server.models import SrcFile, TextFlow, Project
from server.file_parser import rpy


class GetFile(Resource):
    def get(self, file_id):
        src_file_data = SrcFile.query.get(file_id)
        file_str = ""
        with open(src_file_data.file_path) as file_obj:
            file_str = file_obj.read()
        return file_str


class PostFile(Resource):
    def post(self, project_id):
        src_file = request.files.get('src')
        file_name = request.form.get('file_name')
        project = Project.query.get(project_id)
        folder_path = os.path.join(app.root_path, 'static/' + project.project_name + '/')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        src_file.save(folder_path + file_name)
        if SrcFile.query.filter(SrcFile.project_id == project_id, SrcFile.file_name == file_name).count() > 0:
            return "Already exist!"
        # src_file = open(folder_path + file_name)
        text_file = SrcFile(file_name=file_name, file_path=folder_path + file_name,
                            src_language=project.src_language, project_id=project_id)
        db.session.add(text_file)
        db.session.commit()
        print("text_id:{}".format(text_file.id))
        rpy_file = rpy.RpyFile(folder_path + file_name)
        text_flows = rpy_file.get_text_flows()
        for text_flow in text_flows:
            tf_data = TextFlow(src_text=text_flow.src, target_text=text_flow.trans,
                               translation_history="", translation_status=0, text_file_id=text_file.id)
            db.session.add(tf_data)
        db.session.commit()
        return "success!"


class ProjectResource(Resource):
    def get(self, project_id):
        pass

    def post(self, project_id):
        project_name = request.form['project_name']
        project_type = request.form['project_type']
        src_lang = request.form['project_src_language']
        project = Project(project_name=project_name, project_type=project_type, src_language=src_lang)
        db.session.add(project)
        db.session.commit()
        return "success!"