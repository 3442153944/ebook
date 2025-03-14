from django.http import JsonResponse

from base_api import BaseApi


class GetNoticeByID(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            data=self.format_request(request)
            limit = data.get('limit', 10)
            offset = data.get('offset', 0)
            send_user_id = data.get('send_user_id', None)
            sql='''
                select * from notice where send_user_id=%s order by time limit %s offset %s
            '''
            if send_user_id:
                result = self.execute_sql(sql, params=[send_user_id, limit, offset])
                if result:
                    return JsonResponse({'code': 200, 'msg': '获取成功', 'data': result})
                else:
                    return JsonResponse({'code':200,'msg':'没用该用户发布的公告','data':[]},status=200)
            else:
                return JsonResponse({'code': 400, 'msg': '缺少参数'},status=400)
        except Exception as e:
            self.error_log(e, request)
            print(e)
            return JsonResponse({'code': 500, 'msg': '服务器错误'},status=500)