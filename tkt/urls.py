from django.urls import path
from tkt import views


# 앱 이름 정의
app_name = 'tkt'

# url 패턴 정의
urlpatterns = [
    path('', views.index, name='index'),
    path('ajax-test/', views.ajax_test, name='ajax-test'),
    path('a-test/', views.a_test, name='a-test'),

    path('chart-bar/', views.chart_bar, name='chart-bar'),

    path('json-daily-chart/', views.data_daily_chart, name='json-daily-chart'),
    path('json-keyword-top10/', views.data_keyword_top10, name='json-keyword-top10'),

    path('json-twitter-data/', views.data_twitter, name='json-twitter-data'),
    path('json-youtube-data/', views.data_youtube, name='json-youtube-data'),

    path('json-stacked-wk-data/', views.data_test_01, name='json-stacked-wk-data'),
    path('json-stacked-mt-data/', views.data_test_02, name='json-stacked-mt-data'),
]