import jws;
import bcrypt;

def is_valid_access_token(token: str) -> bool:
    try:
        jws.verify(token, secret, algorithms=["HS256"])
        return True
    except:
        return False 

def decode_user_from_token(token: str) -> str:
    try:
        user = jws.verify(token, secret, algorithms=["HS256"])
    except:
        abort(401, "Invalid access token")

    user = json.loads(user)

    if user["exp"] < int(datetime.now().timestamp()):
        abort(401, "Access token expired")

    if user["iat"] > int(datetime.now().timestamp()):
        abort(401, "Access token is from the future")

    return user["username"]
    

def get_current_user() -> str:
    if (access_token := request.cookies.get("access_token")) is not None:
        return decode_user_from_token(access_token)

    abort(401, "No access token could be found") 

def get_new_access_token(username: str) -> str:
    now = datetime.now()
    tomorrow = now + timedelta(days=1)

    return jws.sign({
        "username": username,
        "exp": int(tomorrow.timestamp()),
        "iat": int(now.timestamp())
    }, secret, algorithm="HS256")


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
