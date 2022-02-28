import json

from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection
from datetime import datetime, timedelta


# Create your views here.


# 인덱스 페이지 실행 함수 ------->
def index(request):
    return render(request, 'tkt/index.html')


def ajax_test(request):
    return render(request, 'tkt/ajax_test.html')


def chart_bar(request):
    return render(request, 'tkt/chart_bar.html')


def a_test(request):
    jsonObject = json.loads(request.body)
    print(jsonObject.get('title'))
    return JsonResponse(jsonObject)


def data_keyword_top10(request):
    today_datetime = (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")
    # MySQL 에서 오늘 기준 keyword 테이블에서 weight 기준 상위 10개 키워드 데이터 추출
    global data_keyword_top10
    labels = []
    data = []

    try:
        cursor = connection.cursor()
        query = "SELECT keyword, weight FROM keyword WHERE c_date = '%s' ORDER BY weight DESC LIMIT 10;" % today_datetime
        cursor.execute(query)
        data_keyword_top10 = cursor.fetchall()
        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed Selecting in StockList")

    for entry in data_keyword_top10:
        labels.append(entry[0])
        data.append(entry[1])

    dic_data = {
        'labels': labels,
        'data': data,
        'time': today_datetime,
        'query': query,
    }

    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})


def data_twitter(request):
    today_datetime = (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")
    # MySQL 에서 오늘 기준 keyword 테이블에서 weight 기준 상위 10개 키워드 데이터 추출
    labels = []
    data = []

    try:
        cursor = connection.cursor()
        query_01 = "SELECT keyword FROM keyword WHERE c_date = '%s' ORDER BY weight DESC LIMIT 10;" % today_datetime
        query_02 = "SELECT keyword_id, CAST(SUM(like_count) AS SIGNED), COUNT(keyword_id) tweet, CAST(SUM(retweet) AS SIGNED), group_concat(DISTINCT(nullif(tags, 'empty'))) FROM twitter GROUP BY keyword_id ORDER BY keyword_id DESC;"
        cursor.execute(query_01)
        keywords = list(cursor.fetchall())
        cursor.execute(query_02)
        twitter = cursor.fetchall()
        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed Selecting in StockList")

    result = []
    no = 1
    while len(keywords) > 0:
        word = keywords.pop(0)
        for key in twitter:
            if word[0] in key[0]:
                result.append([no, list(key)])
        no += 1

    for entry in result:
        labels.append(entry[0])
        data.append(entry[1])

    dic_data = {
        'labels': labels,
        'data': data
    }

    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})


def data_youtube(request):
    today_datetime = (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")
    # MySQL 에서 오늘 기준 keyword 테이블에서 weight 기준 상위 10개 키워드 데이터 추출
    labels = []
    data = []

    try:
        cursor = connection.cursor()
        query_01 = "SELECT keyword FROM keyword WHERE c_date = '%s' ORDER BY weight DESC LIMIT 10;" % today_datetime
        query_02 = "SELECT keyword_id, CAST(SUM(like_count) AS SIGNED), CAST(SUM(comment_count) AS SIGNED), CAST(SUM(view_count) AS SIGNED), group_concat(DISTINCT(nullif(tags, 'empty'))) FROM youtube GROUP BY keyword_id ORDER BY keyword_id DESC;"
        cursor.execute(query_01)
        keywords = list(cursor.fetchall())
        cursor.execute(query_02)
        youtube = cursor.fetchall()
        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed Selecting in StockList")

    result = []
    no = 1
    while len(keywords) > 0:
        word = keywords.pop(0)
        for key in youtube:
            if word[0] in key[0]:
                result.append([no, list(key)])
        no += 1

    for entry in result:
        labels.append(entry[0])
        data.append(entry[1])

    dic_data = {
        'labels': labels,
        'data': data
    }

    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})


def data_daily_chart(request):
    # MySQL 에서 오늘 기준 keyword 테이블에서 weight 기준 상위 10개 키워드 데이터 추출
    today_datetime = (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")
    yesterday_datetime = (datetime.today() - timedelta(2)).strftime("%Y-%m-%d")
    try:
        cursor = connection.cursor()
        query_01 = "SELECT keyword, weight FROM keyword WHERE c_date = '%s' ORDER BY weight DESC LIMIT 25;" % yesterday_datetime
        query_02 = "SELECT keyword, weight FROM keyword WHERE c_date = '%s' ORDER BY weight DESC LIMIT 25;" % today_datetime
        cursor.execute(query_01)
        today = dict(cursor.fetchall())
        cursor.execute(query_02)
        yesterday = dict(cursor.fetchall())
        connection.commit()
        connection.close()
    except:
        connection.rollback()
        print("Failed Selecting in StockList")

    daily_chart = []

    for i in today.keys():
        if i in yesterday.keys():
            if (today[i] - yesterday[i]) > yesterday[i]:
                daily_chart.append([i, today[i], "up"])
            elif (today[i] - yesterday[i]) == yesterday[i]:
                daily_chart.append([i, today[i], "same"])
            else:
                daily_chart.append([i, today[i], "down"])
        else:
            daily_chart.append([i, today[i], "new"])

    dic_data = {
        'data': daily_chart
    }

    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})
