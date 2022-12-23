from flask import Flask
from dotenv import load_dotenv
from . import views

def create_app():
    load_dotenv()
    
    app = Flask(__name__)

    views.configure(app)

    return app