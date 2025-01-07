"""
import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
from game_server import app
import logging
from .test_config import BASE_URL, WS_URL, API_PATHS, LOG_CONFIG

# 配置日誌
logging.basicConfig(level=LOG_CONFIG["level"], format=LOG_CONFIG["format"])
logger = logging.getLogger(__name__)

# 設定測試客戶端
client = TestClient(app, base_url=BASE_URL)

@pytest.mark.asyncio
async def test_websocket_connection():
    """測試 WebSocket 連接"""
    ws_path = f"{WS_URL}{API_PATHS['websocket']}/test-client"
    logger.debug(f"測試 WebSocket 連接到 {ws_path}")
    
    with client.websocket_connect(ws_path) as websocket:
        data = websocket.receive_json()
        logger.debug(f"收到 WebSocket 響應: {data}")
        assert "type" in data
        assert data["type"] == "connection_established"

@pytest.mark.asyncio
async def test_player_ready():
    """測試玩家準備狀態"""
    ws_path = f"{WS_URL}{API_PATHS['websocket']}/test-client"
    logger.debug(f"測試玩家準備狀態: {ws_path}")
    
    with client.websocket_connect(ws_path) as websocket:
        websocket.send_json({
            "type": "player_ready"
        })
        data = websocket.receive_json()
        logger.debug(f"收到 WebSocket 響應: {data}")
        assert "type" in data
        assert "players" in data

@pytest.mark.asyncio
async def test_game_start():
    """測試遊戲開始條件"""
    player1_ws_path = f"{WS_URL}{API_PATHS['websocket']}/player1"
    player2_ws_path = f"{WS_URL}{API_PATHS['websocket']}/player2"
    logger.debug(f"測試遊戲開始條件: {player1_ws_path}, {player2_ws_path}")
    
    # 連接兩個玩家
    with client.websocket_connect(player1_ws_path) as player1, \
         client.websocket_connect(player2_ws_path) as player2:
        
        # 兩個玩家都準備
        player1.send_json({"type": "player_ready"})
        player2.send_json({"type": "player_ready"})
        
        # 檢查遊戲是否開始
        data = player1.receive_json()
        logger.debug(f"收到 WebSocket 響應: {data}")
        assert "type" in data
        assert data["type"] == "game_started"

###