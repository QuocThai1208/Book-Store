from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager, login_user
app = Flask(__name__)
CORS(app, resources={r"/static/*": {"origins": "*"}})
app.secret_key = 'FDSDFJSKDF444JSDJFSDJFSSDF'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:%s@localhost/app-librarydb2' % quote('tinquan123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 4
db = SQLAlchemy(app)
login= LoginManager(app)