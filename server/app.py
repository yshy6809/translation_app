import os
import sys
from sys import prefix

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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

