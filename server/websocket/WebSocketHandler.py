from datetime import datetime, timezone

from jwt_auth import BaseJWTHandler
import tornado.websocket
import json

# 全局管理在线客户端
clients = {}  # 格式：{ user_id: websocket_handler_instance }
# 全局管理群组成员，群组成员以 user_id 为标识
groups = {}  # 格式：{ group_id: set(user_id1, user_id2, ...) }


class WebSocketHandler(BaseJWTHandler, tornado.websocket.WebSocketHandler):

    def check_origin(self, origin: str) -> bool:
        """覆盖 Tornado 的默认 origin 检查，允许所有来源"""
        return True  # 允许所有来源
    def open(self):
        """WebSocket 连接打开时注册客户端"""
        user_id = self.current_user.id
        #获取Sec-WebSocket-Protocol
        token=self.request.headers.get('Sec-WebSocket-Protocol')
        user=self.decode_jwt(token)
        print(user)
        print(token)
        if user_id:
            # 若用户允许多连接，则可以改为维护列表，本例假设每个用户只有一个连接
            clients[user_id] = self
            # self.info_log('WebSocket opened for user_id: {}'.format(user_id), self.request)
            print('WebSocket opened for user_id: {}'.format(user_id))
        self.write_message('Hello, world')

    def on_close(self):
        """连接关闭时注销客户端"""
        user_id = self.current_user.id
        if user_id and user_id in clients:
            del clients[user_id]
            print('WebSocket closed for user_id: {}'.format(user_id))

    def one_to_one(self, target_id, msg):
        """一对一私聊：根据 target_id 发送消息"""
        target = clients.get(target_id)
        if target:
            target.write_message(msg)
            self.info_log("Sent one_to_one msg to user_id: {}".format(target_id), self.request)
        else:
            self.write_message("目标用户不在线")

    def one_to_more(self, target_ids, msg):
        """一对多消息群发：根据 target_ids 列表发送消息"""
        not_online = []
        for uid in target_ids:
            target = clients.get(uid)
            if target:
                target.write_message(msg)
            else:
                not_online.append(uid)
        self.info_log("Sent one_to_more msg to users: {}".format(target_ids), self.request)
        if not_online:
            self.write_message("以下用户不在线: " + ", ".join(not_online))

    def more_to_more(self, group_id, msg):
        """多对多群组消息发送：将消息发送到指定群组所有在线成员"""
        if group_id in groups:
            member_ids = groups[group_id]
            for uid in member_ids:
                target = clients.get(uid)
                if target:
                    target.write_message(msg)
            self.info_log("Broadcast msg in group {} to members: {}".format(group_id, member_ids), self.request)
        else:
            self.write_message("群组不存在")

    def on_message(self, message):
        """
        根据收到的消息内容解析不同的发送场景，比如：
         - 一对一： {"type": "one_to_one", "target_id": "xxx", "msg": "hello"}
         - 一对多： {"type": "one_to_more", "target_ids": ["xxx", "yyy"], "msg": "hello"}
         - 群聊： {"type": "more_to_more", "group_id": "group1", "msg": "hello everyone"}
        实际项目中可增加消息格式校验、异常捕获等。
        """
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            if msg_type == "one_to_one":
                target_id = data.get("target_id")
                msg = data.get("msg")
                self.one_to_one(target_id, msg)
            elif msg_type == "one_to_more":
                target_ids = data.get("target_ids", [])
                msg = data.get("msg")
                self.one_to_more(target_ids, msg)
            elif msg_type == "more_to_more":
                group_id = data.get("group_id")
                msg = data.get("msg")
                self.more_to_more(group_id, msg)
            else:
                self.write_message("未知消息类型")
        except Exception as e:
            self.write_message("消息解析错误: " + str(e))

    def info_log(self, info, request):
        # 简单的日志记录函数，实际项目中可使用 logging 模块
        print("[INFO]", datetime.now(timezone.utc), info)
