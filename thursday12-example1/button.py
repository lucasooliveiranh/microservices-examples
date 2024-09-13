from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Serve static files (for HTML, CSS, JavaScript)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define a model to receive the button's state
class ButtonState(BaseModel):
    state: bool

# Serve the HTML page with the button
@app.get("/", response_class=HTMLResponse)
async def get_html():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Boolean Button</title>
    </head>
    <body>
        <h1>Boolean Button Example</h1>
        <button id="toggleButton">Click me</button>
        <p>Button State: <span id="buttonState">False</span></p>

        <script>
            let button = document.getElementById('toggleButton');
            let stateDisplay = document.getElementById('buttonState');
            let buttonState = false;

            // Handle button click
            button.addEventListener('click', () => {
                buttonState = !buttonState;
                stateDisplay.innerHTML = buttonState;

                // Send the state to the FastAPI backend
                fetch('/toggle-button', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ state: buttonState }),
                }).then(response => response.json())
                  .then(data => {
                      console.log('Button state sent to server:', data);
                  });
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Handle the POST request with the button's state
@app.post("/toggle-button")
async def toggle_button(state: ButtonState):
    print(f"Button state received: {state.state}")
    return {"state": state.state}