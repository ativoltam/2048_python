from flask import Flask
import alone_2048

app = Flask(__name__)
app.config['SECRET_KEY'] = 'so amazingly secret' # for session values


@app.route("/")
def main():
	return alone_2048
