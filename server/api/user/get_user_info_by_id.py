from django.http import JsonResponse

from base_api import BaseApi


class GetUserInfoByID(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        data=self.format_request(request)
        target_id=data.get('target_id')
        if target_id:
            sql = "select users.user_id,username,avatar,signature,sex,background,status from users where user_id=%s"
            results = self.execute_sql(sql, [target_id])
            if results:
                results = results[0]
                if results.get('status')!=1:
                    return JsonResponse({'code':200,'msg':'用户账户异常'},status=200)
                return JsonResponse({'code':200,'msg':'获取成功','data':results},status=200)
            return JsonResponse({'code':200,'msg':'用户不存在'},status=200)
        return JsonResponse({'code':400,'msg':'缺少参数'},status=400)
