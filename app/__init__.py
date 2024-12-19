from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import cloudinary

from flask_login import LoginManager, login_user
app = Flask(__name__)
CORS(app, resources={r"/static/*": {"origins": "*"}})
app.secret_key = 'FDSDFJSKDF444JSDJFSDJFSSDF'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:%s@localhost/app-librarydb' % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6
db = SQLAlchemy(app)

cloudinary.config(
    cloud_name = "ds4oggqzq",
    api_key = "393726784763992",
    api_secret = "hks4Bc8122s41z6vSN7jJdwuioI", # Click 'View API Keys' above to copy your API secret
    secure=True
)


login= LoginManager(app)