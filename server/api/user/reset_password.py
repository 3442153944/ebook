from django.http import JsonResponse
from base_api import BaseApi

class ResetPassword(BaseApi):

    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            data=self.format_request(request)
            if data:
                user_id=data.get('username')
                email=data.get('email')
                password=data.get('password')
                sql='''
                select 1 from users where (user_id =%s or username =%s) and (email=%s or phone=%s)
                '''
                result=self.execute_sql(sql,params=[user_id,user_id,email,email])
                print(result)
                if result:
                    sql='''
                    update users set password=%s where user_id=%s
                    '''
                    if self.execute_sql(sql,params=[password,user_id])>0:
                        return JsonResponse({'code':200,'msg':'密码重置成功'},status=200)
                return JsonResponse({'code':401,'msg':'用户不存在'},status=401)
            return JsonResponse({'code':400,'msg':'参数错误'},status=400)
        except Exception as e:
            self.error_log(e, request)
            return JsonResponse({'code': 500, 'msg': '服务器错误'})