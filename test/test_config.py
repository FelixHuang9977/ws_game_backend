"""測試配置文件"""

# 伺服器設定
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000
BASE_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"
WS_URL = f"ws://{SERVER_HOST}:{SERVER_PORT}"

# API 路徑
API_PATHS = {
    "register": "/register",
    "login": "/login",
    "websocket": "/ws"
}

# 測試用戶數據
TEST_USERS = {
    "valid_user": {
        "username": "testuser",
        "password": "testpass123"
    },
    "invalid_user": {
        "username": "",
        "password": ""
    }
}

# 日誌設定
LOG_CONFIG = {
    "level": "DEBUG",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}