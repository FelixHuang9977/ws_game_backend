import pytest
from fastapi.testclient import TestClient
from game_server import app

client = TestClient(app)

def test_register():
    response = client.post(
        "/register",
        data={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "message" in response.json()

def test_login():
    # 先註冊
    client.post(
        "/register",
        data={"username": "testuser2", "password": "testpass"}
    )
    
    # 測試登入
    response = client.post(
        "/login",
        data={"username": "testuser2", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()

def test_invalid_login():
    response = client.post(
        "/login",
        data={"username": "nonexistent", "password": "wrongpass"}
    )
    assert response.status_code == 401

# WebSocket 測試需要額外的異步測試設置
@pytest.mark.asyncio
async def test_websocket_connection():
    # TODO: 實現 WebSocket 連接測試
    pass