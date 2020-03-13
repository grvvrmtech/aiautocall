#from django.urls import path
from django.urls import path
from kws.views import Index
from kws.views import Analysis
from kws.views import Keyword
from kws.views import KeywordIndex
from kws.views import SearchKeyword

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('keyword/', Keyword.as_view(), name = 'keyword'),
    path('keyword_index/', KeywordIndex.as_view(), name = 'keyword_index'),
    path('search_keyword/', SearchKeyword.as_view(), name = 'search_keyword'),
    path('analysis/', Analysis.as_view(), name = 'analysis'),
    path('analysis/<str:call_id>/<str:keyword_id>/', Analysis.as_view(), name='listen'),
    ]

