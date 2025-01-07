import pytest
from fastapi.testclient import TestClient
from game_server import app
import logging
from .test_config import BASE_URL, API_PATHS, TEST_USERS, LOG_CONFIG

# 配置日誌
logging.basicConfig(level=LOG_CONFIG["level"], format=LOG_CONFIG["format"])
logger = logging.getLogger(__name__)

# 設定測試客戶端
client = TestClient(app, base_url=BASE_URL)

class TestRegisterAPI:
    """註冊 API 的測試類"""

    def test_register_success(self):
        """測試成功註冊的情況"""
        logger.info(f"開始測試成功註冊 - {BASE_URL}{API_PATHS['register']}")
        
        response = client.post(
            API_PATHS["register"],
            data=TEST_USERS["valid_user"]
        )
        
        logger.debug(f"收到響應: {response.status_code} - {response.json()}")
        assert response.status_code == 200
        assert "message" in response.json()
    def test_register_duplicate_username(self):
        """測試重複用戶名註冊的情況"""
        logger.info(f"開始測試重複用戶名註冊 - {BASE_URL}{API_PATHS['register']}")
        
        # 第一次註冊
        logger.debug("發送第一次註冊請求")
        first_response = client.post(
            API_PATHS["register"],
            data=TEST_USERS["duplicate_user"]
        )
        assert first_response.status_code == 200, "第一次註冊應該成功"
    
        # 嘗試重複註冊
        logger.debug("發送重複註冊請求")
        second_response = client.post(
            API_PATHS["register"],
            data=TEST_USERS["duplicate_user"]
        )
        
        # 驗證響應
        logger.debug(f"收到重複註冊響應: {second_response.status_code} - {second_response.json()}")
        assert second_response.status_code == 400, "重複註冊應該返回 400 狀態碼"
        assert "detail" in second_response.json(), "響應中應包含 detail 字段"
        assert second_response.json()["detail"] == "Username already registered", "應返回正確的錯誤訊息"

    def test_register_invalid_username(self):
        """測試無效用戶名的情況"""
        logger.info(f"開始測試無效用戶名 - {BASE_URL}{API_PATHS['register']}")
        
        for test_case in TEST_USERS["invalid_username"]:
            response = client.post(
                API_PATHS["register"],
                        data=test_case
            )
            assert response.status_code == 400, "無效用戶名應該返回 400 狀態碼"
            assert "detail" in response.json(), "響應中應包含 detail 字段"

    def test_register_invalid_password(self):
        """測試無效密碼的情況"""
        logger.info(f"開始測試無效密碼 - {BASE_URL}{API_PATHS['register']}")
        
        for test_case in TEST_USERS["invalid_password"]:
            response = client.post(
                API_PATHS["register"],
                data=test_case
            )
            assert response.status_code == 400, "無效密碼應該返回 400 狀態碼"
            assert "detail" in response.json(), "響應中應包含 detail 字段"
        
    def test_register_missing_fields(self):
        """測試缺少必要字段的情況"""
        logger.info(f"開始測試缺少字段 - {BASE_URL}{API_PATHS['register']}")
        
        for test_case in TEST_USERS["missing_fields"]:
            response = client.post(
                API_PATHS["register"],
                data=test_case
            )
            assert response.status_code == 422, "缺少必要字段應該返回 422 狀態碼"
            assert "detail" in response.json(), "響應中應包含 detail 字段"

    @pytest.mark.asyncio
    async def test_register_performance(self):
        """測試註冊 API 的性能"""
        logger.info(f"開始性能測試 - {BASE_URL}{API_PATHS['register']}")
        
        import time
        import asyncio
        
        start_time = time.time()
        
        for user in TEST_USERS["performance"]:
            logger.debug(f"發送性能測試請求: {user['username']}")
            response = client.post(
                API_PATHS["register"],
                data=user
            )
            assert response.status_code in [200, 400], "請求應該能夠被正確處理"
        
        end_time = time.time()
        total_time = end_time - start_time
        
        logger.debug(f"性能測試完成，總時間: {total_time:.2f}秒")
        assert total_time < 5, "5個請求應該在5秒內完成"
