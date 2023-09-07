from pydantic import BaseModel,validator
from datetime import datetime
from werkzeug.security import generate_password_hash

class UserRequestSchema(BaseModel):
    name : str
    email : str 
    username : str
    password : str

    
    @validator("password")
    def hash__password(cls, password):
        return generate_password_hash(password)

    class config:
        orm_mode = True

class UserResponseSchema(BaseModel):
    id: int
    name : str
    email : str 
    username : str
    password : str

    class config:
        orm_mode = True
