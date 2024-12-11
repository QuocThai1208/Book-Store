from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote

app = Flask(__name__)
CORS(app, resources={r"/static/*": {"origins": "*"}})
app.secret_key = 'FDSDFJSKDF444JSDJFSDJFSSDF'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:%s@localhost/app-librarydb' % quote('123456')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 4
db = SQLAlchemy(app)
