from django.http import JsonResponse
from base_api import BaseApi

class GetRecommendNovel(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            data=self.format_request(request)
            limit=data.get('limit',20)
            offset=data.get('offset',0)
            sql='''
            select novels.*,user_id,username,avatar,novel_categories.name as novel_type_name from novels
             left join users on users.user_id=novels.author_id
             left join novel_categories on novels.category_id = novel_categories.category_id
             where novels.work_status=0
             order by rating desc limit %s offset %s
            '''
            result=self.execute_sql(sql,[limit,offset])
            return JsonResponse({'code':200,'msg':'获取推荐小说成功','data':result},status=200)

        except Exception as e:
            msg='获取推荐小说发生异常，异常位置：{}，异常信息：{}'.format(self.__class__.__name__,e)
            self.error_log(msg,request)
            return JsonResponse({'code': 500, 'msg': "服务器异常"},status=500)