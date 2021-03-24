from fastapi import FastAPI, HTTPException
from database import connection, User
from schemas import UserRequestModel, UserUpdateModel, UserResponseModel

app = FastAPI(
    title="My first API",
    description="This is a simple API with FastAPI (CRUD)",
    version="1.0.1"
)

@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()

    connection.create_tables([User])


@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()


# index route, just support get method
@app.get('/')
async def index():
    """ This function returns the greetings """
    return "Hello world"


# this route is to create new users, just support the post method (add new user to database)
@app.post('/users')
async def create_user(user_request: UserRequestModel):
    """ class UserUpdateModel as parameter, create new user and return user created """

    user = User.create(
        username=user_request.username,
        email=user_request.email
    )

    return user


@app.get('/get/{user_id}')
async def get_user(user_id):
    """
    this function is to return user if user exist in the database, needs user_id:int
    return user selected
    """

    user = User.select().where(User.id == user_id).first()

    if not user:
        return HTTPException(404, 'User not found')

    return UserResponseModel(
        id=user.id,
        username=user.username,
        email=user.email
    )


@app.put('/update')
async def update_user(user_to_update: UserUpdateModel):
    """
    class UserUpdateModel as parameter, if user_id exist update username and email
    return user updated
    """

    user = User.select().where(User.id == user_to_update.id).first()

    if not user:
        return HTTPException(404, 'User not found')
    else:
        User.update(username=user_to_update.username, email=user_to_update.email).where(User.id == user_to_update.id).execute()

    return UserResponseModel(
        id=user.id,
        username=user_to_update.username,
        email=user_to_update.email
    )


@app.delete('/delete/{user_id}')
async def delete_user(user_id):
    """
    this function is to delete user if user_id exist in the database,
    needs user_id:int and return user deleted
    """
    
    user = User.select().where(User.id == user_id).first()

    if not user:
        return HTTPException(404, 'User not found')
    else:
        user.delete_instance()

    return f"User {user.username} deleted successfully"
