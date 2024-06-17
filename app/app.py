from flask import Flask, render_template

from .user import *

app = Flask(__name__,)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/create")
def create():
    return render_template("create.html")
