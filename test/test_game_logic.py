import pytest
from game_server import ConnectionManager

@pytest.fixture
def connection_manager():
    """創建連接管理器實例"""
    return ConnectionManager()

def test_game_state_initialization(connection_manager):
    """測試遊戲狀態初始化"""
    assert connection_manager.game_state.players == {}
    assert connection_manager.game_state.game_started == False
    assert connection_manager.game_state.current_turn is None

@pytest.mark.asyncio
async def test_broadcast_message(connection_manager):
    """測試廣播消息功能"""
    # 這需要模擬 WebSocket 連接
    pass

@pytest.mark.asyncio
async def test_player_disconnect(connection_manager):
    """測試玩家斷開連接的處理"""
    # 這需要模擬玩家斷開連接的情況
    pass