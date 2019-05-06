from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'so amazingly secret'  # for session values

import alone_2048
