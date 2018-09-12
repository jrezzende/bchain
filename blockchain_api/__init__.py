from flask import Flask

app = Flask(__name__)

from blockchain_api import service
