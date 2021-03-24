from fastapi import FastAPI

app = FastAPI(
    title="My fist API",
    description="This is a test of API with FastAPI",
    version="1.0.1"
)

#
@app.get('/')
def index():
    """ This function returns the greetings """
    return "Hola mundo"
