from django.http import JsonResponse
from base_api import BaseApi


class GetNovelCount(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            # 优化后的SQL：通过JOIN和GROUP BY一次性获取所有分类及其数量
            optimized_sql = """
                SELECT 
                    nc.category_id AS id,
                    nc.name,
                    COUNT(n.novel_id) AS count
                FROM novel_categories nc
                LEFT JOIN novels n ON nc.category_id = n.category_id
                GROUP BY nc.category_id, nc.name
            """
            data = self.execute_sql(optimized_sql)

            # 直接返回查询结果（无需循环二次查询）
            return JsonResponse({
                'code': 200,
                'msg': '获取各类小说数量成功',
                'data': data
            }, status=200)

        except Exception as e:
            msg = '获取各类小说数量错误，错误位置：{}，错误信息：{}'.format(
                self.__class__.__name__, e
            )
            self.error_log(msg, request)
            return JsonResponse({
                'code': 500,
                'msg': '服务器错误'
            }, status=500)