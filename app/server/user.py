import bcrypt

from . import database

def user_exists(username: str) -> bool:
    results = database.cursor.execute("SELECT * FROM user WHERE user.username = ?", (username, ))

    return results.fetchone() is not None

def register_user(username: str, password: str) -> bool:
    user_results = database.cursor.execute("SELECT * FROM user WHERE user.username = ?", (username,))

    if user_results.fetchall() != []:
        return False

    hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    insertion_result = database.cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, hash))

    database.connection.commit()

    return True

def try_login_user(username: str, password: str) -> bool:
    user_results = database.cursor.execute("SELECT * FROM user WHERE user.username = ?", (username, ))

    user_results = user_results.fetchone()

    if user_results is None:
        return False

    return bcrypt.checkpw(password.encode(), user_results[1])