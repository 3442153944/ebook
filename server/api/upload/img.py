import os.path
import uuid

from django.http import JsonResponse
from base_api import BaseApi
from djangoProject.settings import STATICFILES_DIRS
from djangoProject.model.format_img import ReWriteImg


class Img(BaseApi):
    def create_uuid(self):
        return str(uuid.uuid4())

    def post(self, request, *args, **kwargs) -> JsonResponse:
        try:
            file=request.FILES.get('image')
            file_name = self.create_uuid() + '.png'
            if file:
                re_img = ReWriteImg(file=file)
                format_img_file = re_img.copy_paste()
                dir=STATICFILES_DIRS[0]
                print(dir)
                path = os.path.join(dir, 'img', file_name)
                if self.save_file(path, format_img_file):
                    return JsonResponse({'code': 200, 'msg': 'ok',
                                         'data': {'url': 'http://localhost:8000/static/img/{}'.format(file_name)}},
                                        status=200)
                return JsonResponse({'code': 401, 'msg': '图片格式错误'}, status=401)
            return JsonResponse({'code': 400, 'msg': '图像为空'}, status=400)
        except Exception as e:
            msg = '服务器错误,错误接口类：{},错误信息：{}'.format(self.__class__.__name__, e)
            self.error_log(msg, request)
            print(e)
            return JsonResponse({'code': 500, 'msg': '服务器错误'}, status=500)
