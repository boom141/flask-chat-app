from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
import os


APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(APP_PATH, 'webApplication/templates')
STATIC = os.path.join(APP_PATH, 'webApplication/static')

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False,
    template_folder=TEMPLATE, static_folder=STATIC)

    app.config.from_object('config.Config')
    
    CORS(app)
    sio = SocketIO(app, cors_allowed_origin='*')
    db.init_app(app)

    with app.app_context():

        from webApplication.scripts.views import views
        from webApplication.scripts.auth import auth

        app.register_blueprint(auth, url_prefix='/')
        app.register_blueprint(views, url_prefix='/')

        from webApplication.scripts.db_models import user_accounts
        create_database()

        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(id):
            return user_accounts.query.get(int(id))

        from webApplication.scripts.socket_events import global_chat
        sio.on_namespace(global_chat('/chatroom'))

        return app, sio
    

def create_database():
    if not os.path.exists('./instance/app.db'):
        db.create_all()
        print('database created successfully!')