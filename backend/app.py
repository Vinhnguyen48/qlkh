from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
db = SQLAlchemy()

def main_web(): 



    app = Flask(__name__, template_folder='../templates',static_folder='../static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qlkh.db' 
    app.config['SECRET_KEY'] = 'jhdsfisfjfijsfisjfisfif'


    image_users = os.path.join( '../static/image_user')
    app.config['UPLOAD_FOLDER'] = image_users
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    db.init_app(app)
    from backend.accounts.router import tk
    from backend.admin.router import admin
    app.register_blueprint(tk,url_prefix='/')
    app.register_blueprint(admin,url_prefix='/admin')
    
    migrate=Migrate(app,db)
    return app