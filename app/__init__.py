from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote

app = Flask(__name__)
app.secret_key = 'FDSDFJSKDFJSDJFSDJFSSDF'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:%s@localhost/app_librarydb' % quote('123456')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 4
db = SQLAlchemy(app)
