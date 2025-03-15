from django.urls import path

from api.upload.chapter import Chapter
from api.upload.img import Img

urlpatterns=[
    path('image',Img.as_view(),name='img'),
    # 图像上传接口
    path('chapter',Chapter.as_view(),name='chapter'),
    # 章节上传接口
]