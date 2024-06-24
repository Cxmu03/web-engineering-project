from flask import Flask, render_template, request, make_response, jsonify

from .user import *
from .fractal import get_fragment_shader

app = Flask(__name__,)

@app.route("/fragment")
def fragment_shader():
    args = {}
    for arg, typ in [("iterations", int), ("escape_radius", float), ("formula", str)]:
        if arg not in request.args:
            return make_response(
                jsonify({
                    "message": f"{arg} parameter could not be found" 
                }), 
                422
            )

        args |= {arg: typ(request.args.get(arg))}

    return make_response(
        #f'<pre>{get_fragment_shader(args["iterations"], args["escape_radius"], args["formula"])}</pre>',
        get_fragment_shader(args["iterations"], args["escape_radius"], args["formula"]),
        200
    )

@app.route("/")
def main():
    return render_template("index.html", currentPage="home")

@app.route("/create")
def create():
    return render_template("create.html", currentPage="create")
