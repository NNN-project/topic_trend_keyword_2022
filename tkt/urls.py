from django.urls import path
from tkt import views


# 앱 이름 정의
app_name = 'tkt'

# url 패턴 정의
urlpatterns = [
    path('', views.index, name='index'),
    path('ajax_test/', views.ajax_test, name='ajax_test'),
    path('a_test/', views.a_test, name='a_test'),

    path('chart_bar/', views.chart_bar, name='chart_bar'),

    path('json_daily_chart/', views.data_daily_chart, name='json_daily_chart'),
    path('json_keyword_top10/', views.data_keyword_top10, name='json_keyword_top10'),

    path('json_twitter_data/', views.data_twitter, name='json_twitter_data'),
    path('json_youtube_data/', views.data_youtube, name='json_youtube_data'),

]