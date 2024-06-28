import sqlite3

connection = None
cursor = None

def init():
    global connection
    global cursor

    connection = sqlite3.connect("database.sqlite", check_same_thread=False)
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS user (username VARCHAR PRIMARY KEY, password VARCHAR)")

    cursor.execute("""CREATE TABLE IF NOT EXISTS fractal (username VARCHAR,
                                                          name VARCHAR,
                                                          fractal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                          formula VARCHAR,
                                                          escape_radius REAL,
                                                          iterations INTEGER,
                                                          center_x REAL,
                                                          center_y REAL,
                                                          width REAL,
                                                          preview BLOB,
                                                          FOREIGN KEY (username) REFERENCES user(username) ON UPDATE CASCADE)""")