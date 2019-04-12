from flask import Flask, render_template
import alone_2048

app = Flask(__name__)
app.config['SECRET_KEY'] = 'so amazingly secret' # for session values


@app.route("/")
def main():
	return render_template('index.html')
