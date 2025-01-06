from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Response
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="test/static"), name="static")

# Serve the main test page
@app.get("/")
async def serve_test_client():
    with open("test/static/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return Response(content=html_content, media_type="text/html")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)