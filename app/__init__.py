from flask import Flask
from flask_caching import Cache


config = {
    "DEBUG": True,
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'so amazingly secret'  # for session values
app.config.from_mapping(config)
cache = Cache(app)

import alone_2048
