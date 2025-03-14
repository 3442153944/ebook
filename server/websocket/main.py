import json
from typing import Any

import jwt
import tornado
from tornado import httputil

from WebSocketHandler import WebSocketHandler
import tornado.websocket
from operate_db import OperateDB


class DefaultHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        """设置默认的 CORS 头"""
        self.set_header("Access-Control-Allow-Origin", "*")  # 允许所有来源
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def options(self):
        """处理预检请求（OPTIONS）"""
        self.set_status(204)
        self.finish()

    def get(self):
        self.write("hello world")


class TestWebSocketHandler(tornado.websocket.WebSocketHandler):
    # 使用字典存储在线用户：键为 user_id，值为 WebSocket 实例
    connected_users = {}

    def __init__(self, application: tornado.web.Application, request: httputil.HTTPServerRequest, **kwargs):
        super().__init__(application, request)
        self.user_id = None

    def check_origin(self, origin):
        return True  # 允许所有来源

    def open(self):
        """连接建立时验证用户身份并加入连接池"""
        token = self.get_argument("token", default=None)
        if not token:
            self.close(code=4001, reason="Missing token")
            print("Missing token")
            return

        try:
            # 解析 JWT 并获取用户信息
            user = self.decode_jwt(token)
            user_id = user.get("user_id")
            self.user_id = user_id  # 存储到实例属性

            # 将当前用户加入连接池
            self.__class__.connected_users[user_id] = self
            print(f"User {user_id} connected. Total users: {len(self.connected_users)}")
            print("Connected users:", self.connected_users)

            # 发送欢迎消息
            self.write_message({'hello': 'connect websocket'})
        except Exception as e:
            self.close(code=4000, reason=str(e))

    def on_message(self, message):
        """处理客户端消息"""
        try:
            data = json.loads(message)
            target_user_id = data.get("target_user_id")  # 从消息中获取目标用户ID
            msg = data.get("msg")  # 获取消息内容

            print(f"Received message from {self.user_id} to {target_user_id}: {msg}")

            # 先给发送者反馈确认信息
            try:
                self.write_message({'reply_msg': msg})
            except tornado.websocket.WebSocketClosedError:
                print("Sender connection already closed, cannot send confirmation")

            # 向目标用户发送消息（如果在线）
            target = self.__class__.connected_users.get(target_user_id)
            if target:
                try:
                    target.write_message({'msg': msg})
                except tornado.websocket.WebSocketClosedError:
                    print(f"Target user {target_user_id} connection closed")
            else:
                self.write_message(f"User {target_user_id} not online")
        except Exception as e:
            try:
                self.write_message(f"Error: {str(e)}")
            except tornado.websocket.WebSocketClosedError:
                print("WebSocket already closed, cannot send error message")

    def on_close(self):
        """连接关闭时移除用户"""
        if self.user_id in self.__class__.connected_users:
            del self.__class__.connected_users[self.user_id]
            print(f"User {self.user_id} disconnected. Total users: {len(self.connected_users)}")

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


if __name__ == '__main__':
    app = tornado.web.Application([
        (r'/', DefaultHandler),
        (r'/ws', WebSocketHandler),
        (r'/ts', TestWebSocketHandler)
    ])
    print('监听2233端口')
    app.listen(2233)
    tornado.ioloop.IOLoop.current().start()
