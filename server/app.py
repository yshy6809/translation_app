import os
import sys
from sys import prefix

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


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
        pass


class ProjectResource(Resource):
    def get(self, project_id):
        pass
    
    def post(self):
        pass


api.add_resource(HelloWorld, '/')
api.add_resource(GetFile, "/api/file/get/<string:file_id>")
api.add_resource(PostFile, "api/file/upload/<string:project_id>")





