from . import database

import base64

def save_fractal_to_database(user: str, name: str, formula: str, escape_radius: float, iterations: int, center_x: float, center_y: float, width: float, preview: str):
    image_data = base64.b64decode(preview)

    database.cursor.execute("""INSERT INTO fractal (username, name, formula, escape_radius, iterations, center_x, center_y, width, preview)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                      (user, name, formula, escape_radius, iterations, center_x, center_y, width, image_data))

    database.connection.commit()

def delete_fractal_from_database(id: int):
    database.cursor.execute("DELETE FROM fractal WHERE fractal_id = ?", (id, ))

    database.connection.commit()

def get_fractal_creator(id: int):
    results = database.cursor.execute("SELECT username FROM fractal WHERE fractal_id = ?", (id, ))

    return None if results is None else results.fetchone()[0]

def get_all_fractals():
    fractals = database.cursor.execute("SELECT * FROM fractal")

    return fractals.fetchall()

def get_all_fractals_excepy_by(username: str):
    fractals = database.cursor.execute("SELECT * FROM fractal WHERE fractal.username != ?", (username, ))

    return fractals.fetchall()

def get_all_fractals_by(username: str):
    fractals = database.cursor.execute("SELECT * FROM fractal where fractal.username = ?", (username,))

    return fractals.fetchall()