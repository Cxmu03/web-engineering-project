from . import database

import base64

def save_fractal_to_database(user: str, name: str, formula: str, escape_radius: float, iterations: int, center_x: float, center_y: float, width: float, preview: str):
    image_data = base64.b64decode(preview)

    database.cursor.execute("""INSERT INTO fractal (username, name, formula, escape_radius, iterations, center_x, center_y, width, preview)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                      (user, name, formula, escape_radius, iterations, center_x, center_y, width, image_data))

    database.connection.commit()

def get_all_fractals():
    fractals = database.cursor.execute("SELECT * FROM fractal")

    return fractals.fetchall()

def get_all_fractals_by(username: str):
    fractals = database.cursor.execute("SELECT * FROM fractal where fractal.username = ?", (username,))

    return fractals.fetchall()