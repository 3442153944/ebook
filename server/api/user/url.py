from django.urls import path

from api.user.get_notice import GetNotice
from api.user.get_notice_by_id import GetNoticeByID
from api.user.get_user_info import GetUserInfo
from api.user.get_user_info_by_id import GetUserInfoByID
from api.user.register import Register
from api.user.reset_password import ResetPassword

urlpatterns = [
    path('register', Register.as_view(), name='Register'),
    # 注册接口
    path('get_user_info', GetUserInfo.as_view(), name='GetUserInfo'),
    # 获取用户信息
    path('get_user_info_by_id', GetUserInfoByID.as_view(), name='GetUserInfoById'),
    # 根据id获取用户信息
    path('reset_password', ResetPassword.as_view(), name='ResetPassword'),
    # 重置密码
    path('get_notice', GetNotice.as_view(),name='GetNotice'),
    # 获取公告
    path('get_notice_by_id', GetNoticeByID.as_view(),name='GetNoticeById'),
    # 根据id获取公告
]
