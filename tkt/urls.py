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

    # 키워드 탑10
    path('json-keyword-top10-day/', views.data_keyword_top10_day, name='json-keyword-top10-day'),
    path('json-keyword-top10-week/', views.data_keyword_top10_week, name='json-keyword-top10-week'),
    path('json-keyword-top10-month/', views.data_keyword_top10_month, name='json-keyword-top10-month'),


    path('json-twitter-dy-data/', views.twitter_dy_data, name='json-twitter-dy-data'),
    path('json-twitter-wk-data/', views.twitter_wk_data, name='json-twitter-wk-data'),
    path('json-twitter-mt-data/', views.twitter_mt_data, name='json-twitter-mt-data'),
    path('json-youtube-dy-data/', views.youtube_dy_data, name='json-youtube-dy-data'),
    path('json-youtube-wk-data/', views.youtube_wk_data, name='json-youtube-wk-data'),
    path('json-youtube-mt-data/', views.youtube_mt_data, name='json-youtube-mt-data'),

    path('json-daily-chart/', views.data_daily_chart, name='json-daily-chart'),
    path('json-stacked-wk-data/', views.stacked_wk_data, name='json-stacked-wk-data'),
    path('json-stacked-mt-data/', views.stacked_mt_data, name='json-stacked-mt-data'),
]