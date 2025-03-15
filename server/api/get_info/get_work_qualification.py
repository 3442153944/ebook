from django.http import JsonResponse
from base_api import BaseApi


class GetWorkQualification(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            if not request.user.is_login:
                return JsonResponse({'code': 401, 'msg': '未登录'}, status=401)
            data = self.format_request(request)
            novel_id = data.get('novel_id')
            if not novel_id:
                return JsonResponse({'code': 400, 'msg': '缺少参数'}, status=400)
            sql = '''
            select is_vip,status,work_status from novels where novel_id=%s
            '''
            result = self.execute_sql(sql, params=[novel_id])
            if result:
                return JsonResponse({'code': 200, 'msg': '获取成功', 'data': result[0]}, status=200)
            return JsonResponse({'code': 404, 'msg': '未找到该小说'}, status=404)

        except Exception as e:
            msg = '发生异常，发生位置：{},错误信息：{}'.format(self.__class__.__name__, e)
            self.error_log(msg, request)
            return JsonResponse({'code': 500, 'msg': '系统错误'}, status=500)
