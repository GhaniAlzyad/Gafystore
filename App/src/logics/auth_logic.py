from hashlib import sha256
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from App.src.models import User
from App.src.schema import AuthSchema

class AuthLogic:

    @staticmethod
    async def login(param: AuthSchema):
        user = await User.get_by_email_or_username(param.username)
        if not check_password_hash(user.password, param.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password!")

        if user.token is None or user.expired_at < datetime.now():
            user.token = generate_token(user.username, user.email)
            user.expired_at = datetime.now() + timedelta(hours=1)
            await user.commit()

        return {"token": user.token}

def generate_password(password: str):
    return generate_password_hash(password)

def generate_token(username: str, email: str):
    return sha256(f"{username}{email}{datetime.now()}".encode('utf-8')).hexdigest()

async def token_validator(token: str) -> AuthSchema:
    user = await User.get_by_token(token)
    now = datetime.now()
    expired_in_five = now + timedelta(minutes=10)

    if user.expired_at < now:
        user.token = None
        await user.commit()

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired, please login again")
    elif expired_in_five > user.expired_at:
        user.expired_at = now + timedelta(hours=1)
        await user.commit()

    return user