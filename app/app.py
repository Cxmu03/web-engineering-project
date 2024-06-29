from flask import Flask, render_template, request, make_response, jsonify, redirect

from .server import *
from .server.rendering import get_fragment_shader, get_calculation_steps

import base64

app = Flask(__name__,)
app.jinja_env.filters['b64encode'] = base64.b64encode
database.init()

def check_arguments(provided_args, needed_args):
    args = {}
    for arg, typ in needed_args:
        if arg not in provided_args:
            return False, arg

        args |= {arg: typ(provided_args.get(arg))}

    return True, args

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if ("username" not in request.form or "password" not in request.form) \
            or (not try_login_user(request.form["username"], request.form["password"])):
            return render_template("login.html")

        access_token = get_new_access_token(request.form["username"])
        print(access_token)

        response = make_response(redirect("/", 302))

        response.set_cookie("access_token", access_token, httponly=True, max_age=86400)

        return response

    if (user := get_current_user()) != None:
        return redirect("/")
    return render_template("login.html")

@app.route("/api/user/<username>/exists")
def api_user_exists(username):
    if user_exists(username):
        return "true", 200
    
    return "false", 200

@app.route("/logout")
def logout():
    response = make_response(redirect("/login"))

    response.delete_cookie("access_token")

    return response

@app.route("/explore", methods=["GET"])
def explore():
    if (user := get_current_user()) == None:
        return redirect("/login", 302)

    fractals = get_all_fractals_excepy_by(user)

    return render_template("explore.html", username=user, fractals=fractals)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if (user := get_current_user()) != None:
            return redirect("/")
        return render_template("register.html")
    else:
        if ("username" not in request.form or "password" not in request.form) \
            or (request.form["password"] != request.form["password-repeat"]) \
            or (len(request.form["password"]) < 8) \
            or (not register_user(request.form["username"], request.form["password"])):
            return render_template("register.html")

        return redirect("/login", 302)

@app.route("/api/fractal/<id>", methods=["DELETE"])
def fractal_api(id: int):
    if (user := get_current_user()) == None:
        abort(403, "Unauthorized")

    if request.method == "DELETE":
        if (creator := get_fractal_creator(id)) is None:
            abort(404, f"Fractal with id {id} does not exist")

        if creator != user:
            abort(403, "Unauthorized")

        delete_fractal_from_database(id)

        return "Success", 200


@app.route("/api/fragment")
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

@app.route("/api/formula/<formula>/is-valid")
def formula_is_valid(formula: str):
    try:
        get_calculation_steps(formula)
        return "true"
    except:
        return "false"

@app.route("/", methods=["GET"])
def main():
    if (user := get_current_user()) == None:
        return redirect("/login")

    fractals = get_all_fractals_by(user)

    return render_template("index.html", currentPage="home", username=user, fractals=fractals)

@app.route("/create", methods=["GET", "POST"])
def create():
    if (user := get_current_user()) == None:
        return redirect("/login")

    if request.method == "GET":
        return render_template("create.html", username=user, currentPage="create", **request.args)
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

        save_fractal_to_database(user, a["name"], a["formula"], a["escape_radius"], a["iterations"], a["center_x"], a["center_y"], a["width"], a["preview"].split(",")[-1])

        return redirect("/create", 302)
    
@app.route("/docs")
def docs():
    return render_template("docs.html", username=get_current_user())