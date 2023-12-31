from pydantic import BaseModel

class AuthSchema(BaseModel):
    username: str
    password: str


class AuthSchemaResponse(AuthSchema):
    id: str