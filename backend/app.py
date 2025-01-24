from flask import Flask, redirect, url_for,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from datetime import timedelta
import os

db = SQLAlchemy()
login_manager = LoginManager()

def main_web():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qlkh.db'
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=30)
    app.config['SECRET_KEY'] = 'jhdsfisfjfijsfisjfisfif'
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config['UPLOAD_FOLDER'] = os.path.join( BASE_DIR,'../static/image_user')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    Migrate(app, db)

    # kt Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'accounts.index'

    # dk Blueprints
    from backend.accounts.router import tk
    from backend.admin.router import admin
    from backend.customers.router import customer
    app.register_blueprint(tk, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(customer, url_prefix='/customer')

    # Đăng ký user_loader
    from backend.model.qlkh import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
