import pytest
import requests
import logging
# 配置日誌
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('test.log')
    ]
)
logger = logging.getLogger(__name__)
        
# 伺服器設定
BASE_URL = "http://127.0.0.1:8000"

class TestRegisterAPI:
    """註冊 API 的測試類"""
    def test_register_success(self):
        """
        測試成功註冊的情況
        期望：
        1. 返回 200 狀態碼
        2. 返回成功訊息
        """
        logger.info("開始測試成功註冊")
        
        # 準備測試數據
        test_user = {
            "username": "testuser1",
            "password": "testpass123"
        }
        
        logger.debug(f"發送註冊請求到 {BASE_URL}/register: {test_user['username']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/register",
                data=test_user
            )
            
            # 驗證響應
            logger.debug(f"收到響應: {response.status_code} - {response.text}")
            assert response.status_code == 200, "註冊應該返回 200 狀態碼"
            assert "message" in response.json(), "響應中應包含 message 字段"
        
        except requests.exceptions.ConnectionError:
            logger.error(f"無法連接到伺服器 {BASE_URL}")
            raise
        except Exception as e:
            logger.error(f"測試過程中發生錯誤: {str(e)}")
            raise
    def test_register_duplicate_username(self):
        """
        測試重複用戶名註冊的情況
        期望：
        1. 返回 400 狀態碼
        2. 返回適當的錯誤訊息
        """
        logger.info("開始測試重複用戶名註冊")
        
        # 準備測試數據
        test_user = {
            "username": "testuser2",
            "password": "testpass123"
        }
        
        try:
            # 第一次註冊
            logger.debug("發送第一次註冊請求")
            first_response = requests.post(
                f"{BASE_URL}/register",
                data=test_user
            )
            assert first_response.status_code == 200, "第一次註冊應該成功"
        
            # 嘗試重複註冊
            logger.debug("發送重複註冊請求")
            second_response = requests.post(
                f"{BASE_URL}/register",
                data=test_user
            )
            
            # 驗證響應
            logger.debug(f"收到重複註冊響應: {second_response.status_code} - {second_response.text}")
            assert second_response.status_code == 400, "重複註冊應該返回 400 狀態碼"
            assert "detail" in second_response.json(), "響應中應包含 detail 字段"
            
        except requests.exceptions.ConnectionError:
            logger.error(f"無法連接到伺服器 {BASE_URL}")
            raise
        except Exception as e:
            logger.error(f"測試過程中發生錯誤: {str(e)}")
            raise

if __name__ == "__main__":
    # 如果直接運行此文件，執行所有測試
    pytest.main([__file__, '-v', '-s'])
