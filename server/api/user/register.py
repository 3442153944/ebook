import os.path
from datetime import datetime
from django.conf import settings
from base_api import BaseApi
from django.http import JsonResponse
from djangoProject.model.format_img import ReWriteImg
from django.db import connection,transaction,DatabaseError
import uuid
import json

class Register(BaseApi):
    def get_uuid(self):
        return str(uuid.uuid4())

    def post(self, request, *args, **kwargs):
        try:
            now = datetime.now()
            # 获取文件和数据
            file = request.FILES.get('file')  # 文件字段名必须与前端一致
            data_str = request.POST.get('data')  # 数据字段名为 "data"

            if not data_str:
                print('数据字段缺失')
                return JsonResponse({'code': 400, 'msg': '数据字段缺失'}, status=400)

            # 解析 JSON 数据
            try:
                data = json.loads(data_str)
            except json.JSONDecodeError:
                print('数据格式错误')
                return JsonResponse({'code': 400, 'msg': '数据格式错误'}, status=400)
            print(data)
            # 验证必填字段
            if not (file and data):
                print('信息完整度问题')
                return JsonResponse({'code': 400, 'msg': '信息完整度问题'}, status=400)

            # 文件处理
            img = ReWriteImg(file=file)
            format_file = img.copy_paste()
            if not format_file:
                return JsonResponse({'code': 500, 'msg': '文件处理失败'}, status=500)

            # 生成文件名并保存
            file_name = f"{self.get_uuid()}.png"
            # 正确拼接路径（包含文件名）
            path = os.path.join(settings.BASE_DIR, 'static', 'img', file_name)
            self.save_file(path, format_file)

            # 验证密码长度
            if not self.check_password(data.get('password')):
                return JsonResponse({'code': 400, 'msg': '密码长度不能小于6位'}, status=400)

            # 数据库插入
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO users 
                        (username, password, email, registration_date, last_login, avatar,
                         signature, user_level, phone, sex, background) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        [
                            data.get('username'),
                            data.get('password'),
                            data.get('email'),
                            now,
                            now,
                            file_name,
                            data.get('signature', ''),
                            1,
                            data.get('phone'),
                            data.get('sex', '女'),
                            data.get('background', 'default_back.jpg'),
                        ]
                    )
                if cursor.rowcount == 1:
                    return JsonResponse({'code': 200, 'msg': '注册成功'}, status=200)
                else:
                    raise DatabaseError('异常插入条数，操作回滚')
        except Exception as e:
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)
        except DatabaseError as e:
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '数据库错误'}, status=500)
    def check_password(self,password):
        if len(password)<6:
            return False
        return True
