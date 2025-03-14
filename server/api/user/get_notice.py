from django.http import JsonResponse

from base_api import BaseApi


class GetNotice(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            user=request.user
            data=self.format_request(request)
            if user.is_login and user.status==1:
                sql='''
                select * from notice where target_user_id=%s order by time 
                '''
                get_total='''
                select count(*) as total from notice where target_user_id=%s
                '''
                result=self.execute_sql(sql, [user.id])
                total=self.execute_sql(get_total,[user.id])
                if result:
                    return JsonResponse({'code': 200, 'msg': '获取成功', 'data': result,'total': total[0]['total']})
                else:
                    return JsonResponse({'code': 200, 'msg': '获取成功', 'data': [],'total': 0})
            else:
                return JsonResponse({'code':200,'msg':'未登录'},status=200)
        except Exception as e:
            self.error_log(e, request)
            print(e)
            return JsonResponse({'code': 500, 'msg': '服务器错误'},status=500)