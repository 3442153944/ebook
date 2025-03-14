import jwt
import tornado.web
from datetime import datetime, timezone
import pymysql
from pymysql import DatabaseError

# 密钥和算法设置
KEY = 'django-insecure-pm__s5rkwbf1#=l!j4%uh*hy5)3g!ld6_cod&e(o!yx)7#=)^z'
JWT_ALGORITHM = 'HS256'

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'forum',
    'password': '123456',
    'db': 'forum',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

class JWTUser:
    def __init__(self, payload):
        self.id = payload.get('user_id')
        self.username = payload.get('username')
        self.email = payload.get('email')
        self.phone = payload.get('phone')
        self.sex = payload.get('sex')
        self.avatar = payload.get('avatar')
        self.user_level = payload.get('user_level')
        self.background = payload.get('background')
        self.is_login = payload.get('is_login', False)
        self.status = payload.get('status', 0)

    def __str__(self):
        return (f"JWTUser(id={self.id}, username={self.username}, "
                f"email={self.email}, phone={self.phone}, "
                f"sex={self.sex}, avatar={self.avatar}, "
                f"user_level={self.user_level}, background={self.background}, "
                f"is_login={self.is_login}, status={self.status})")


class BaseJWTHandler(tornado.web.RequestHandler):
    # def prepare(self):
    #     """
    #     在请求开始时提取并解析 token，
    #     如果存在且有效，将用户信息以 JWTUser 实例赋值给 self.current_user，
    #     否则保持为 None（表示未认证）。
    #     """
    #     auth_header = self.request.headers.get("Authorization", "")
    #     if auth_header and auth_header.startswith("token "):
    #         token = auth_header.split(" ")[1]
    #         payload = self.decode_jwt(token)
    #         if payload:
    #             self.current_user = JWTUser(payload)
    #             self.current_user.is_login = True
    #         else:
    #             # token 无效或过期，置为未认证
    #             self.current_user = None
    #             # 如果需要可以直接中断请求返回401
    #             self.set_status(401)
    #             self.finish({"code": 401, "msg": "无效或过期的令牌"})
    #     else:
    #         # 没有提供 token 时，默认为匿名用户
    #         self.current_user = JWTUser({})
    #         self.current_user.is_login = False

    def decode_jwt(self, token):
        """解码 JWT 令牌，返回解码后的 payload 或 None"""
        KEY = 'django-insecure-pm__s5rkwbf1#=l!j4%uh*hy5)3g!ld6_cod&e(o!yx)7#=)^z'
        JWT_ALGORITHM = 'HS256'
        try:
            return jwt.decode(token, KEY, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            self.write({"code": 401, "msg": "令牌已过期"})
            return None
        except jwt.InvalidTokenError:
            self.write({"code": 401, "msg": "无效的令牌"})
            return None

    def execute_sql(self, sql, params=None):
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                result = cursor.fetchall()
            connection.commit()
            return result
        except DatabaseError as e:
            connection.rollback()
            print(f"Error executing SQL: {e}")
            return None
        finally:
            connection.close()

    def insert_sql(self, sql, params=None):
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
            connection.commit()
            return True
        except DatabaseError as e:
            connection.rollback()
            print(f"Error executing SQL: {e}")
            return False
        finally:
            connection.close()