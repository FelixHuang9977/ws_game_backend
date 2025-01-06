from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List
from datetime import datetime, timedelta
from jose import JWTError, jwt
import json
import uvicorn

# FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001", "http://127.0.0.1:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security configurations
SECRET_KEY = "your-secret-key-keep-it-safe"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# In-memory storage (replace with database in production)
fake_users_db = {}
connected_players: Dict[str, WebSocket] = {}

# User model
class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

# Helper functions
def get_user(username: str):
    if username in fake_users_db:
        return User(username=username, password=fake_users_db[username])
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if password != user.password:
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# REST API endpoints
@app.post("/register")
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"Registration attempt for user: {form_data.username}")
    if form_data.username in fake_users_db:
        print(f"Registration failed: {form_data.username} already exists")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    fake_users_db[form_data.username] = form_data.password
    print(f"User registered successfully: {form_data.username}")
    return {"message": "User registered successfully"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"Login attempt for user: {form_data.username}")
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        print(f"Login failed for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    print(f"Login successful for user: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(f"Client connected: {client_id}")
        print(f"Active connections: {list(self.active_connections.keys())}")

    def disconnect(self, client_id: str):
        self.active_connections.pop(client_id, None)
        print(f"Client disconnected: {client_id}")
        print(f"Active connections: {list(self.active_connections.keys())}")

    async def broadcast(self, message: str, exclude: str = None):
        print(f"Broadcasting message from {exclude}: {message}")
        for client_id, connection in self.active_connections.items():
            if client_id != exclude:
                await connection.send_text(message)
                print(f"Message sent to {client_id}")

manager = ConnectionManager()

# WebSocket endpoint
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"\nReceived message from {client_id}:")
            print(f"Raw data: {data}")
            
            try:
                message = json.loads(data)
                print(f"Parsed message: {json.dumps(message, indent=2)}")
            except json.JSONDecodeError as e:
                print(f"Error parsing message from {client_id}: {e}")
                continue
                        
            # Broadcast the message to all other connected clients
            await manager.broadcast(
                json.dumps({
                    "client_id": client_id,
                        "message": message
                    })
            )
            
            
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        disconnect_message = json.dumps({
                "client_id": client_id,
                "message": "left the game"
            })
        print(f"Client disconnected: {client_id}")
        await manager.broadcast(disconnect_message)
    except Exception as e:
        print(f"Error handling websocket for {client_id}: {e}")
        manager.disconnect(client_id)
if __name__ == "__main__":
    print("Game server starting...")
    print("Listening on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)