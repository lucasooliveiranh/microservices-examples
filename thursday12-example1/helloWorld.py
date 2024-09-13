# import the Flask module into a new Python file. 
from fastapi import FastAPI

# create a Flask object
app = FastAPI()

# provide a route for handling incoming requests
@app.get('/')

# add a simple function that returns the message “Hello, World!” as the response
def hello():
    return 'Hello, World!'
    
if __name__ == "__main__":
    app.run()