from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

from djangoProject import settings

urlpatterns = [
    # path("admin/", admin.site.urls),
   path('api/',include('api.url'),name='api')
    # api模块
] + static('static/', document_root=settings.STATICFILES_DIRS)
# 静态资源文件夹配置

