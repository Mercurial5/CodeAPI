from flask import Flask

app = Flask(__name__)

from codeapi.api import routes
