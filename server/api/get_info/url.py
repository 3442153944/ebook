from django.urls import path

from api.get_info.get_novel_count import GetNovelCount
from api.get_info.get_recommend_novel import GetRecommendNovel
from api.get_info.get_work_qualification import GetWorkQualification

urlpatterns = [
    path('get_work_qualification', GetWorkQualification.as_view(), name='GetWorkQualification'),
    # 获取作品资质
    path('get_novel_count', GetNovelCount.as_view(), name='GetNovelCount'),
    # 获取各类小说数量
    path('get_recommend_novel', GetRecommendNovel.as_view(), name='GetRecommendNovel'),
    # 获取推荐小说
]
