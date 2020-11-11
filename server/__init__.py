import sys, os, click

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


app = Flask('server', template_folder='./dist', static_folder='./dist/static')
cors = CORS(app, resources={r'/api/*':{'origins': '*'}})
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


from server import apis
from server import views
