import os
import random

from flask_restful import Resource
from flask import request
from flask import abort
from flask import jsonify

from server import app, db
from server.models import SrcFile, TextFlow, Project
from server.file_parser import rpy


class GetFile(Resource):
    def get(self, file_id):
        src_file_data = SrcFile.query.get(file_id)
        response = {'file_name': src_file_data.file_name, 'src_language': src_file_data.src_language,
                    'project_id': src_file_data.project_id, 'text_flows': []}
        text_flow_datas = TextFlow.query.filter(TextFlow.text_file_id == file_id).all()
        for tf_data in text_flow_datas:
            '''
            data_dict = {}
            data_dict['id'] = tf_data.id
            data_dict['src_text'] = tf_data.src_text
            data_dict['']
            '''
            response['text_flows'].append(dict(tf_data))
        return jsonify(response)

    def delete(self, file_id):
        file_data = SrcFile.query.get(file_id)
        if os.path.exists(file_data.file_path):
            os.remove(file_data.file_path)
        text_flow_datas = TextFlow.query.filter(TextFlow.text_file_id == file_id).all()
        db.session.delete(file_data)
        for tf_data in text_flow_datas:
            db.session.delete(tf_data)
        db.session.commit()
        return "success!"


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
            tf_data = TextFlow(src_text=text_flow.src, target_text=text_flow.trans, speaker=text_flow.speaker,
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

    def delete(self, project_id):
        project = Project.query.get(project_id)
        os.removedirs(os.path.join(app.root_path, "static/" + project.project_name))
        db.session.delete(project)
        files = SrcFile.query.filter(SrcFile.project_id == project_id).all()
        for file_data in files:
            db.session.delete(file_data)
            text_flows = TextFlow.query.filter(TextFlow.text_file_id == file_data.id).all()
            for tf_data in text_flows:
                db.session.delete(tf_data)
        db.session.commit()
        return "success!"


class TextflowResource(Resource):
    def get(self, id):
        tf = TextFlow.query.get(id)
        response = {"data":{}}
        response['data']['text'] = tf.src_text
        return jsonify(response)

    def put(self, id):
        tf = TextFlow.query.get(id)
        #tf.target_text = request.form['target']
        tf.target_text = request.get_json()['target']
        db.session.commit()
        return '1'


class Random(Resource):
    def get(self):
        response = {'randomNumber': random.randint(1, 100)}
        return jsonify(response)


