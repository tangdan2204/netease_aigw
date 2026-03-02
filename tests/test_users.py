# ========================================
# 用户模块测试用例
# ========================================
"""
pytest测试用例

测试用户注册、登录、信息查询等功能的正确性
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models.user import User
from app.schemas import UserCreate, UserLogin
from app.services.user_service import UserService


# ========================================
# 测试数据库设置
# ========================================

# 使用内存SQLite进行测试
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """覆盖数据库依赖"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def test_db():
    """测试数据库 fixture"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    yield
    # 清理数据
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """测试客户端 fixture"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def db_session(test_db):
    """数据库会话 fixture"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def user_service(db_session):
    """用户服务 fixture"""
    return UserService(db_session)


# ========================================
# 测试数据
# ========================================

TEST_USER_DATA = {
    "username": "testuser",
    "email": "test@example.com",
    "phone": "13800138000",
    "password": "password123",
    "confirm_password": "password123",
}

TEST_LOGIN_DATA = {"username": "testuser", "password": "password123"}


# ========================================
# 测试用例
# ========================================


class TestUserRegistration:
    """用户注册测试"""

    def test_register_success(self, client, test_db):
        """测试成功注册"""
        response = client.post("/api/v1/users/register", json=TEST_USER_DATA)
        assert response.status_code == 200

        data = response.json()
        assert data["code"] == 0
        assert data["msg"] == "注册成功"
        assert data["data"]["username"] == TEST_USER_DATA["username"]
        assert data["data"]["email"] == TEST_USER_DATA["email"]
        assert "id" in data["data"]

    def test_register_duplicate_username(self, client, test_db):
        """测试重复用户名"""
        # 第一次注册
        client.post("/api/v1/users/register", json=TEST_USER_DATA)

        # 第二次注册相同用户名
        response = client.post(
            "/api/v1/users/register",
            json={
                **TEST_USER_DATA,
                "email": "another@example.com",
                "phone": "13900139000",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 2002  # USER_EXISTS
        assert "用户名已存在" in data["msg"]

    def test_register_duplicate_email(self, client, test_db):
        """测试重复邮箱"""
        # 第一次注册
        client.post("/api/v1/users/register", json=TEST_USER_DATA)

        # 第二次注册相同邮箱
        response = client.post(
            "/api/v1/users/register",
            json={**TEST_USER_DATA, "username": "anotheruser", "phone": "13900139000"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 2002
        assert "邮箱已被注册" in data["msg"]

    def test_register_password_mismatch(self, client, test_db):
        """测试密码不匹配"""
        response = client.post(
            "/api/v1/users/register",
            json={**TEST_USER_DATA, "confirm_password": "differentpassword"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 1001  # PARAM_INVALID
        assert "两次密码不一致" in data["msg"]

    def test_register_invalid_email(self, client, test_db):
        """测试无效邮箱"""
        response = client.post(
            "/api/v1/users/register", json={**TEST_USER_DATA, "email": "invalid-email"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 1001
        assert "邮箱" in str(data["data"])

    def test_register_short_password(self, client, test_db):
        """测试密码过短"""
        response = client.post(
            "/api/v1/users/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "123",  # 小于6位
                "confirm_password": "123",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 1001

    def test_register_short_username(self, client, test_db):
        """测试用户名过短"""
        response = client.post(
            "/api/v1/users/register",
            json={
                "username": "ab",  # 小于3位
                "email": "test@example.com",
                "password": "password123",
                "confirm_password": "password123",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 1001


class TestUserLogin:
    """用户登录测试"""

    def test_login_success(self, client, test_db):
        """测试成功登录"""
        # 先注册用户
        client.post("/api/v1/users/register", json=TEST_USER_DATA)

        # 登录
        response = client.post("/api/v1/users/login", json=TEST_LOGIN_DATA)

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["msg"] == "登录成功"
        assert "user" in data["data"]
        assert data["data"]["user"]["username"] == TEST_USER_DATA["username"]

    def test_login_wrong_password(self, client, test_db):
        """测试密码错误"""
        # 注册用户
        client.post("/api/v1/users/register", json=TEST_USER_DATA)

        # 错误密码登录
        response = client.post(
            "/api/v1/users/login",
            json={"username": TEST_USER_DATA["username"], "password": "wrongpassword"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 3001  # PASSWORD_WRONG
        assert "密码错误" in data["msg"]

    def test_login_nonexistent_user(self, client, test_db):
        """测试不存在的用户"""
        response = client.post(
            "/api/v1/users/login",
            json={"username": "nonexistent", "password": "password123"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 2001  # USER_NOT_FOUND

    def test_login_with_email(self, client, test_db):
        """测试使用邮箱登录"""
        # 注册用户
        client.post("/api/v1/users/register", json=TEST_USER_DATA)

        # 使用邮箱登录
        response = client.post(
            "/api/v1/users/login",
            json={
                "username": TEST_USER_DATA["email"],
                "password": TEST_USER_DATA["password"],
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0


class TestUserQuery:
    """用户查询测试"""

    def test_get_user_success(self, client, test_db):
        """测试获取用户信息"""
        # 注册用户
        register_response = client.post("/api/v1/users/register", json=TEST_USER_DATA)
        user_id = register_response.json()["data"]["id"]

        # 获取用户信息
        response = client.get(f"/api/v1/users/{user_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["id"] == user_id
        assert data["data"]["username"] == TEST_USER_DATA["username"]

    def test_get_user_not_found(self, client, test_db):
        """测试获取不存在的用户"""
        response = client.get("/api/v1/users/99999")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 2001  # USER_NOT_FOUND


class TestUserUpdate:
    """用户更新测试"""

    def test_update_user_success(self, client, test_db):
        """测试成功更新用户信息"""
        # 注册用户
        register_response = client.post("/api/v1/users/register", json=TEST_USER_DATA)
        user_id = register_response.json()["data"]["id"]

        # 更新用户信息
        response = client.put(
            f"/api/v1/users/{user_id}",
            json={"nickname": "新昵称", "avatar": "https://example.com/avatar.jpg"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["nickname"] == "新昵称"
        assert data["data"]["avatar"] == "https://example.com/avatar.jpg"


class TestUserStatus:
    """用户状态测试"""

    def test_deactivate_user(self, client, test_db):
        """测试禁用用户"""
        # 注册用户
        register_response = client.post("/api/v1/users/register", json=TEST_USER_DATA)
        user_id = register_response.json()["data"]["id"]

        # 禁用用户
        response = client.post(f"/api/v1/users/{user_id}/deactivate")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["is_active"] is False

    def test_activate_user(self, client, test_db):
        """测试启用用户"""
        # 注册用户
        register_response = client.post("/api/v1/users/register", json=TEST_USER_DATA)
        user_id = register_response.json()["data"]["id"]

        # 禁用后再启用
        client.post(f"/api/v1/users/{user_id}/deactivate")
        response = client.post(f"/api/v1/users/{user_id}/activate")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["is_active"] is True


class TestCheckAvailability:
    """检查可用性测试"""

    def test_check_username_available(self, client, test_db):
        """检查可用用户名"""
        response = client.get("/api/v1/users/check/username/newuser")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["exists"] is False

    def test_check_username_exists(self, client, test_db):
        """检查已存在用户名"""
        # 注册用户
        client.post("/api/v1/users/register", json=TEST_USER_DATA)

        # 检查该用户名
        response = client.get(
            f"/api/v1/users/check/username/{TEST_USER_DATA['username']}"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["exists"] is True

    def test_check_email_available(self, client, test_db):
        """检查可用邮箱"""
        response = client.get("/api/v1/users/check/email/new@example.com")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["exists"] is False

    def test_check_email_exists(self, client, test_db):
        """检查已存在邮箱"""
        # 注册用户
        client.post("/api/v1/users/register", json=TEST_USER_DATA)

        # 检查该邮箱
        response = client.get(f"/api/v1/users/check/email/{TEST_USER_DATA['email']}")

        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        assert data["data"]["exists"] is True


class TestHealthCheck:
    """健康检查测试"""

    def test_root_endpoint(self, client):
        """测试根路由"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        assert "version" in data


# ========================================
# 运行测试
# ========================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
