from flask import Flask, render_template
import requests
from flask_restful import Api
from flask_cors import CORS
from config import config
from decouple import config as config_decouple

# Enviroment check (DEV/PROD)
enviroment = config['development']

if config_decouple('PRODUCTION', cast=bool, default=False):
    enviroment = config['production']

# App initialization
app = Flask(__name__)
app.config.from_object(enviroment)

# App config definition

# App's api definition
api = Api(app)

# Cors init
CORS(app, resources={r'/*': {'origins': '*'}})


# Resources

# Test
@app.route('/')
def hello():
    return 'Hello'
