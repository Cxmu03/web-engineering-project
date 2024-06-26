import sqlite3

def register_user(username: str, password: str) -> bool:
    print(username)
    user_results = cursor.execute("SELECT * FROM user WHERE user.username = ?", (username,))

    if user_results.fetchall() != []:
        return False

    hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    insertion_result = cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, hash))

    connection.commit()

    return True


def try_login_user(username: str, password: str) -> bool:
    user_results = cursor.execute("SELECT * FROM user WHERE user.username = ?", (username, ))

    user_results = user_results.fetchone()

    return bcrypt.checkpw(password.encode(), user_results[1])