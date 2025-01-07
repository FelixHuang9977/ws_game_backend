import asyncio
import websockets
import aiohttp
import json

async def login(username: str, password: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://localhost:8000/token',
            data={'username': username, 'password': password}
        ) as response:
            return await response.json()

async def game_client(uri: str, client_id: str):
    async with websockets.connect(uri) as websocket:
        # Send initial connection message
        await websocket.send(json.dumps({
            "type": "connect",
            "client_id": client_id
        }))

        # Handle incoming messages
        while True:
            try:
                message = await websocket.recv()
                print(f"Received message: {message}")
            except websockets.ConnectionClosed:
                print("Connection closed")
                break

async def main():
    # First login to get token
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    try:
        token_data = await login(username, password)
        print(f"Login successful! Token: {token_data['access_token']}")
        
        # Connect to WebSocket
        uri = f"ws://localhost:8000/ws/{username}"
        await game_client(uri, username)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())