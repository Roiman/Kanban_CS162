from flask import Flask
import os

app = Flask(__name__)
app.config['DEBUG'] = True

from Kanban_app import kanban_api