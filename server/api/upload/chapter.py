from datetime import datetime
from django.http import JsonResponse
from base_api import BaseApi


class Chapter(BaseApi):
    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            data = self.format_request(request)
            if request.user.is_login:
                if data:
                    user_id = request.user.id
                    title = data.get('title')
                    # 统计标题字数
                    if len(title) > 30 or len(title) < 1 or title == '' or title is None:
                        return JsonResponse({'code': 400, 'msg': '标题字数不能超过30个字符'}, status=400)
                    content = data.get('content', None)
                    if not content:
                        return JsonResponse({'code': 400, 'msg': '内容不能为空'}, status=400)
                    novel_id = data.get('novel_id', None)
                    if not user_id or not title or not content:
                        return JsonResponse({'code': 400, 'msg': '缺少必要参数'}, status=400)
                    is_vip = int(data.get('is_vip', 0))
                    # 合并查询：一次性获取 category_id、volume_id 以及章节数
                    get_info = '''
                    SELECT n.category_id,
                           nv.volume_id,
                           (SELECT COUNT(*) FROM chapters c WHERE c.novel_id = n.novel_id) AS total,
                           is_vip
                    FROM novels n
                    JOIN novel_volume nv ON nv.novel_id = n.novel_id
                    WHERE n.novel_id = %s
                    '''
                    result = self.execute_sql(get_info, [novel_id])
                    if not result:
                        return JsonResponse({'code': 400, 'msg': '小说信息不存在'}, status=400)

                    row = result[0]
                    work_qualification = row.get('is_vip')
                    if work_qualification != 1 and is_vip == 1:
                        return JsonResponse({'code': 400, 'msg': '作品资质不足，请与审核联系申请VIP书本资格'},
                                            status=400)
                    category_id = row['category_id']
                    volume_id = row['volume_id']
                    index = row['total'] + 1

                    sql = '''
                    INSERT INTO chapters (novel_id, chapter_number, title, content, type, volume, created_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    '''
                    result_len = self.execute_sql(sql, [
                        novel_id,
                        index,
                        title,
                        content,
                        category_id,  # 使用从合并查询得到的类别 ID
                        volume_id,  # 使用从合并查询得到的卷 ID
                        datetime.now()
                    ])

                    if result_len > 0:
                        return JsonResponse({'code': 200, 'msg': '添加成功'}, status=200)
                    return JsonResponse({'code': 400, 'msg': '添加失败'}, status=400)

                else:
                    return JsonResponse({'code': 400, 'msg': '缺少必要参数'}, status=400)
            return JsonResponse({'code': 401, 'msg': '登录状态失效'}, status=401)
        except Exception as es:
            msg = '服务器错误,发生类{}，错误信息：{}'.format(str(self.__class__.__name__), es)
            self.error_log(msg, request)
            return JsonResponse({'code': 500, 'msg': msg}, status=500)
