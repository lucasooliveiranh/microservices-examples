from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import time

app = FastAPI()

# Serve static files (for HTML, CSS, JavaScript)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define a model to receive the button state
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
        <title>Counter App</title>
    </head>
    <body>
        <h1>Counter App</h1>
        <button id="toggleButton">Start Counting</button>
        <div id="countContainer"></div>

        <script>
            let button = document.getElementById('toggleButton');
            let countContainer = document.getElementById('countContainer');
            let buttonState = false;

            // Handle button click
            button.addEventListener('click', () => {
                buttonState = !buttonState;

                // Send the state to the FastAPI backend
                fetch('/toggle-button', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ state: buttonState }),
                }).then(response => response.json())
                  .then(data => {
                      if (data.state) {
                          // Start receiving the count from backend
                          receiveCount();
                      }
                  });
            });

            // Function to receive and display the count
            async function receiveCount() {
                const eventSource = new EventSource("/count-stream");

                eventSource.onmessage = function(event) {
                    let newCount = event.data;
                    let newDiv = document.createElement('div');
                    newDiv.innerHTML = newCount;
                    countContainer.appendChild(newDiv);

                    // Stop receiving if count is 100000
                    if (parseInt(newCount) >= 10000) {
                        eventSource.close();
                    }
                };
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Handle the POST request to toggle the button state
@app.post("/toggle-button")
async def toggle_button(data: ButtonState):
    if data.state:
        return {"state": True}
    return {"state": False}

# Stream the count to the frontend
@app.get("/count-stream")
async def count_stream():
    def event_generator():
        for i in range(10001):
            time.sleep(0.01)  # Slow down the counting so it's visible
            yield f"data:{i}\n\n"  # SSE format: data:<message>\n\n

    return StreamingResponse(event_generator(), media_type="text/event-stream")
