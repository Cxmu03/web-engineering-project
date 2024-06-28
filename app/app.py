from flask import Flask, render_template, request, make_response, jsonify, redirect

from .server import *
from .server.rendering import get_fragment_shader

app = Flask(__name__,)
database.init()

def check_arguments(provided_args, needed_args):
    args = {}
    for arg, typ in needed_args:
        if arg not in provided_args:
            return False, arg

        args |= {arg: typ(provided_args.get(arg))}

    return True, args

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/fragment")
def fragment_shader():
    success, args = check_arguments(request.args, [("iterations", int), ("escape_radius", float), ("center_x", float), ("center_y", float), ("width", float), ("formula", str)])

    if success == False:
        return make_response(
            jsonify({
                "message": f"Query argument {args} could not be found"
            }),
            422
        )

    return make_response(
        #f'<pre>{get_fragment_shader(args["iterations"], args["escape_radius"], args["formula"])}</pre>',
        get_fragment_shader(args["iterations"], args["escape_radius"], args["center_x"], args["center_y"], args["width"], args["formula"]),
        200
    )

@app.route("/")
def main():
    return render_template("index.html", currentPage="home")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("create.html", currentPage="create")
    elif request.method == "POST":
        print(request.form)
        success, a =  check_arguments(request.form, [("name", str), ("iterations", int), ("escape_radius", float), ("center_x", float), ("center_y", float), ("width", float), ("formula", str), ("preview", str)])
        
        if not success:
            return make_response(
                jsonify({
                    "message": f"Form parameter {a} could not be found"
                }),
                422
            )

        save_fractal_to_database("Marek", a["name"], a["formula"], a["escape_radius"], a["iterations"], a["center_x"], a["center_y"], a["width"], a["preview"].split(",")[-1])

        return redirect("/create", 302)