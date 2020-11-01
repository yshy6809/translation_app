import os
import sys

import click
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

from .file_parser import rpy

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.cli.command()
def initdb():
    db.create_all()
    click.echo('Initialized database')


class TextFlow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    src_text = db.Column(db.Text)
    target_text = db.Column(db.Text)
    translation_history = db.Column(db.Text)
    translation_status = db.Column(db.Integer)
    text_file_id = db.Column(db.Integer)


class SrcFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.Text)
    file_path = db.Column(db.Text)
    src_language = db.Column(db.String(length=10))
    project_id = db.Column(db.Integer)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.Text)
    project_type = db.Column(db.Integer)
    src_language = db.Column(db.String(length=10))


tfs = ["abc", "def", "ghi"]


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class GetFile(Resource):
    def get(self, file_id):
        return tfs


class PostFile(Resource):
    def post(self, project_id):
        src_file = request.files.get('src')
        file_name = request.form.get('file_name')
        project = Project.query.get(project_id)
        folder_path = os.path.join(app.root_path, 'static/' + project.project_name + '/')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        src_file.save(folder_path + file_name)
        #src_file = open(folder_path + file_name)
        text_file = SrcFile(file_name=file_name, file_path=folder_path+file_name,
                            src_language=project.src_language, project_id=project_id)
        db.session.add(text_file)
        db.session.commit()
        print("text_id:{}".format(text_file.id))
        rpy_file = rpy.RpyFile(folder_path+file_name)
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


api.add_resource(HelloWorld, '/')
api.add_resource(GetFile, "/api/file/get/<int:file_id>")
api.add_resource(PostFile, "/api/file/upload/<int:project_id>")
api.add_resource(ProjectResource, "/api/project/<int:project_id>")





