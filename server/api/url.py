from django.urls import path, include

urlpatterns = [
    path('user/', include('api.user.url'), name='user'),
    # 用户接口
    path('upload/', include('api.upload.url'), name='upload'),
    # 上传接口
    path('get_info/',include('api.get_info.url'),name='get_info')
    # 获取信息接口
]
