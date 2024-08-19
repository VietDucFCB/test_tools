# save this as app.py
from app import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"