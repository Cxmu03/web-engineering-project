import jws
import bcrypt
from flask import request, abort

from ..settings import secret

import json
from datetime import datetime, timedelta

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


