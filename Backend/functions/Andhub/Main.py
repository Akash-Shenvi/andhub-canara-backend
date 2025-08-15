from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import json

from .mail_handler import mail_service,and_mail


from .auth import auth 
from .pages import pages
from .users import users
from .uploads import uploads
from .views import views
import os


app=Flask(__name__)
CORS(app)
jwt=JWTManager(app)



# JWT Tokens setup
app.config["JWT_SECRET_KEY"]='QOEROWERJ2341320230984U809REUEWIURFDUSFJLJDFLKJASDLFASDFL'
base_dir = os.path.dirname(os.path.abspath(__file__))

config_path = os.path.join(base_dir, 'Server_configurations.json')

# Load the JSON config
with open(config_path, 'r') as config_file:
    config = json.load(config_file)
    application_configurations = config["flask application configuration"]
    mail_configurations = config["server mail configurations"]



# Registering Blueprints
app.register_blueprint(auth,url_prefix='/auth')
app.register_blueprint(pages,url_prefix='/pages')
app.register_blueprint(mail_service,url_prefix='/mail')
app.register_blueprint(users,url_prefix='/users')
app.register_blueprint(uploads,url_prefix='/uploads')
app.register_blueprint(views,url_prefix='/views')


app.config['MAIL_SERVER'] = mail_configurations["mail server"]
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = mail_configurations["mail username"] 
app.config['MAIL_PASSWORD'] = mail_configurations["mail password"]
print(app.config['MAIL_PASSWORD'])
and_mail.init_app(app)

db=SQLAlchemy() 
if application_configurations["deployed"]:
    app.config['SQLALCHEMY_DATABASE_URI'] =application_configurations["production URI"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] =application_configurations["development URI"]

db.init_app(app)