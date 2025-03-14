from django.http import JsonResponse
from base_api import BaseApi


class GetUserInfo(BaseApi):

    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            user = request.user
            print(user.is_login)
            if user.is_login is False:
                return JsonResponse({'code': 200, 'msg': '请先登录'}, status=200)
            sql = '''
            select * from users where user_id=%s
            '''
            data = self.execute_sql(sql, params=[user.id])
            for i in data:
                i.pop('password', None)
                i.pop('user_level', None)

            if data:
                return JsonResponse({'code': 200, 'msg': '获取成功', 'data': data[0]}, status=200)
            else:
                return JsonResponse({'code': 200, 'msg': '获取失败'}, status=200)
        except Exception as e:
            print(e)
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)
