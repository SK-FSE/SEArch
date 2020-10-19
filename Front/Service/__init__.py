from flask import Flask
from config import Config

UPLOAD_FOLDER = 'Service/samples'

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from Service import routes
