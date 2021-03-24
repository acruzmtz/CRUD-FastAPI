from fastapi import FastAPI, HTTPException
from database import connection
from database import User
from schemas import UserRequestModel, UserUpdateModel

app = FastAPI(
    title="My fist API",
    description="This is a test of API with FastAPI",
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
    """ This function just allow post request, and add new user """

    user = User.create(
        username=user_request.username,
        email=user_request.email
    )

    return user


# this function is to return user if user exist in the database
@app.get('/get/{user_id}')
async def get_user(user_id):
    user = User.select().where(User.id == user_id).first()

    if not user:
        return HTTPException(404, 'User not found')

    return user


@app.put('/update/{user_id}')
async def update_user(user_to_update: UserUpdateModel):
    user = User.select().where(User.id == user_to_update.id).first()

    if not user:
        return HTTPException(404, 'User not found')
    else:
        user_updated = User.update(username=user_to_update.username, email=user_to_update.email).where(User.id == user_to_update.id)

    return True


# this function is to delete user if user exist in the database
@app.delete('/delete/{user_id}')
async def delete_user(user_id):
    user = User.select().where(User.id == user_id).first()

    if not user:
        return HTTPException(404, 'User not found')
    else:
        user.delete_instance()

    return "User deleted successfully"
