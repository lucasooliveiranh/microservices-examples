from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Serve static files (for HTML, CSS, JavaScript)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define a model to receive the numbers and button state
class ButtonState(BaseModel):
    state: bool
    num1: float
    num2: float

# Serve the HTML page with input fields and button
@app.get("/", response_class=HTMLResponse)
async def get_html():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sum of Two Numbers</title>
    </head>
    <body>
        <h1>Sum Calculator</h1>
        <p>Enter two numbers:</p>
        <input type="number" id="num1" placeholder="First number">
        <input type="number" id="num2" placeholder="Second number">
        <button id="toggleButton">Calculate Sum</button>
        <p>Button State: <span id="buttonState">False</span></p>
        <p>Result: <span id="result">-</span></p>

        <script>
            let button = document.getElementById('toggleButton');
            let stateDisplay = document.getElementById('buttonState');
            let resultDisplay = document.getElementById('result');
            let buttonState = false;

            // Handle button click
            button.addEventListener('click', () => {
                let num1 = parseFloat(document.getElementById('num1').value);
                let num2 = parseFloat(document.getElementById('num2').value);

                if (isNaN(num1) || isNaN(num2)) {
                    alert('Please enter valid numbers');
                    return;
                }

                buttonState = !buttonState;
                stateDisplay.innerHTML = buttonState;

                // Send the state and numbers to the FastAPI backend
                fetch('/toggle-button', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ state: buttonState, num1: num1, num2: num2 }),
                }).then(response => response.json())
                  .then(data => {
                      if (data.state) {
                          resultDisplay.innerHTML = data.sum;
                      } else {
                          resultDisplay.innerHTML = '-';
                      }
                  });
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Handle the POST request with the button's state and numbers
@app.post("/toggle-button")
async def toggle_button(data: ButtonState):
    if data.state:
        result = data.num1 + data.num2
        return {"state": True, "sum": result}
    return {"state": False, "sum": None}