from django.urls import path,include

urlpatterns=[
    path('user/',include('api.user.url'),name='user'),
    # user接口
]