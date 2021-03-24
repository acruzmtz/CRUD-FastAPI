from pydantic import BaseModel

class UserRequestModel(BaseModel):
    username: str
    email: str

class UserUpdateModel(UserRequestModel):
    id: int
