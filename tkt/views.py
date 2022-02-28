import json

from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection
from datetime import datetime, timedelta


# Create your views here.


# 인덱스 페이지 실행 함수 ------->
def index(request):
    current_url = r'../'
    context = {
        'current_url': current_url

    }
    return render(request, 'tkt/index.html', context)


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


def data_test_01(request):
    weekly_day = ('월', '화', '수', '목', '금', '토', '일')
    weekly_chart = {}
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT keyword FROM keyword WHERE DATE(c_date) >= ADDDATE(curdate(), - WEEKDAY(curdate())) AND DATE(c_date) <= ADDDATE(curdate(), - WEEKDAY(curdate())+ 6) GROUP BY keyword ORDER BY SUM(weight) DESC LIMIT 5;")
        keywords = cursor.fetchall()
        if len(keywords) != 0:
            for i in range(5):
                cursor.execute(
                    f"SELECT weight FROM keyword WHERE DATE(c_date) >= ADDDATE(curdate(), - WEEKDAY(curdate())) AND DATE(c_date) <= ADDDATE(curdate(), - WEEKDAY(curdate())+ 6) AND keyword = '{keywords[i][0]}' ORDER BY c_date;")
                daily_weight = list(cursor.fetchall())
                weight = [0] * 7
                for n in range(len(daily_weight)):
                    weight[n] = daily_weight[0][0]
                weekly_chart[keywords[i][0]] = weight
        else:
            # 이번주 데이터가 없을 시 지난주 데이터 추출
            cursor.execute(
                "SELECT keyword FROM keyword WHERE DATE(c_date) >= ADDDATE(date_add(curdate(), interval -1 day), - WEEKDAY(date_add(curdate(), interval -1 day))) AND DATE(c_date) <= ADDDATE(date_add(curdate(), interval -1 day), - WEEKDAY(date_add(curdate(), interval -1 day))+ 6) GROUP BY keyword ORDER BY SUM(weight) DESC LIMIT 5;")
            keywords = cursor.fetchall()
            for i in range(5):
                cursor.execute(
                    f"SELECT weight FROM keyword WHERE DATE(c_date) >= ADDDATE(date_add(curdate(), interval -1 day), - WEEKDAY(date_add(curdate(), interval -1 day))) AND DATE(c_date) <= ADDDATE(date_add(curdate(), interval -1 day), - WEEKDAY(date_add(curdate(), interval -1 day))+ 6) AND keyword = '{keywords[i][0]}' ORDER BY c_date;")
                daily_weight = list(cursor.fetchall())
                weight = [0] * 7
                for n in range(len(daily_weight)):
                    weight[n] = daily_weight[0][0]
                weekly_chart[keywords[i][0]] = weight
        connection.commit()
        connection.close()
    except:
        connection.rollback()
        print("Failed Selecting in StockList")




    dic_data = {
        'labels': weekly_day,
        'datasets': [{'label': 'keyword#01', 'backgroundColor': "#3e95cd", 'data': [4,5,6,7,8,9,4]},
                     {'label': 'keyword#02', 'backgroundColor': "#2ecc71", 'data': [1,2,3,4,5,6,1]},
                     {'label': 'keyword#03', 'backgroundColor': "#f1c40f", 'data': [4,3,3,2,3,1,1]},
                     {'label': 'keyword#04', 'backgroundColor': "#9b59b6", 'data': [5,4,3,1,2,9,2]},
                     {'label': 'keyword#05', 'backgroundColor': "#e74c3c", 'data': [2,5,1,1,3,3,6]},]
    }
    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})


def data_test_02(request):

    dic_data = {
        'labels': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                   '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                   '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', ],
        'datasets': [{'label': 'keyword#01', 'backgroundColor': "#3e95cd", 'data': [4,5,6,7,8,9,4,4,5,6,7,8,9,4,4,5,6,7,8,9,4,4,5,6,7,8,9,4]},
                     {'label': 'keyword#02', 'backgroundColor': "#2ecc71", 'data': [1,2,3,4,5,6,1,1,2,3,4,5,6,1,1,2,3,4,5,6,1,1,2,3,4,5,6,1]},
                     {'label': 'keyword#03', 'backgroundColor': "#f1c40f", 'data': [4,3,3,2,3,1,1,4,3,3,2,3,1,1,4,3,3,2,3,1,1,4,3,3,2,3,1,1]},
                     {'label': 'keyword#04', 'backgroundColor': "#9b59b6", 'data': [5,4,3,1,2,9,2,5,4,3,1,2,9,2,5,4,3,1,2,9,2,5,4,3,1,2,9,2]},
                     {'label': 'keyword#05', 'backgroundColor': "#e74c3c", 'data': [2,5,1,1,3,3,6,2,5,1,1,3,3,6,2,5,1,1,3,3,6,2,5,1,1,3,3,6]},]
    }
    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})