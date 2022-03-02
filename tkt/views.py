import json

from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection
from datetime import datetime, timedelta


# Create your views here.


# 인덱스 페이지 실행 함수 ------->
def index(request):
    import datetime
    today = datetime.date.today()
    last_day = today - datetime.timedelta(1)
    last_monday = today - datetime.timedelta(days=today.weekday())  # 지난 월요일 날짜
    last_firstday = today.replace(day=1)  # 지난 월요일 날짜
    p_week = str(last_monday) + " ~ " + str(last_day)
    p_month = str(last_firstday) + " ~ " + str(last_day)

    current_url = r'../'
    context = {
        'current_url': current_url,
        'p_day': str(last_day),
        'p_week': p_week,
        'p_month': p_month

    }
    return render(request, 'tkt/index.html', context)


def data_period_day(request):
    import datetime
    today = datetime.date.today()
    last_day = today - datetime.timedelta(1)
    last_monday = today - datetime.timedelta(days=today.weekday())  # 지난 월요일 날짜
    last_firstday = today.replace(day=1)  # 지난 월요일 날짜
    print(today, last_day, last_monday, last_firstday)

    p_week = str(last_monday) + " ~ " + str(last_day)
    p_month = str(last_firstday) + " ~ " + str(last_day)
    print(p_week)
    print(p_month)

    dic_data = {
        'p_day': last_day,
        'p_week': p_week,
        'p_month': p_month
    }

    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})


def data_keyword_top10_day(request):
    # MySQL 에서 오늘 기준 keyword 테이블에서 weight 기준 상위 10개 키워드 데이터 추출
    labels = []
    data = []

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT keyword, weight FROM keyword WHERE c_date = curdate() ORDER BY weight DESC LIMIT 10;")
        result = cursor.fetchall()
        # 오늘에 대한 정보 없을 시 어제 날짜로 출력
        if len(result) == 0:
            cursor.execute("SELECT keyword, weight FROM keyword WHERE c_date = date_add(curdate(), interval -1 day) ORDER BY weight DESC LIMIT 10;")
            result = cursor.fetchall()
        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed Selecting in StockList")

    for entry in result:
        labels.append(entry[0])
        data.append(entry[1])

    dic_data = {
        'labels': labels,
        'data': data
    }

    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})


def data_keyword_top10_week(request):
    labels = []
    data = []

    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT keyword, CAST(SUM(weight) AS SIGNED) FROM keyword WHERE DATE(c_date) >= ADDDATE(curdate(), - WEEKDAY(curdate())) AND DATE(c_date) <= ADDDATE(curdate(), - WEEKDAY(curdate())+ 6) GROUP BY keyword ORDER BY SUM(weight) DESC LIMIT 10;")
        result = cursor.fetchall()
        # 이번주에 대한 정보가 없을시 지난주에 대한 정보 출력
        if len(result) == 0:
            cursor.execute(
                "SELECT keyword, CAST(SUM(weight) AS SIGNED) FROM keyword WHERE DATE(c_date) >= ADDDATE(date_add(curdate(), interval -1 day), - WEEKDAY(date_add(curdate(), interval -1 day))) AND DATE(c_date) <= ADDDATE(date_add(curdate(), interval -1 day), - WEEKDAY(date_add(curdate(), interval -1 day))+ 6) GROUP BY keyword ORDER BY SUM(weight) DESC LIMIT 10;")
            result = cursor.fetchall()
        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed Selecting in StockList")

    for entry in result:
        labels.append(entry[0])
        data.append(entry[1])

    dic_data = {
        'labels': labels,
        'data': data
    }

    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})


def data_keyword_top10_month(request):
    labels = []
    data = []

    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT keyword, CAST(SUM(weight) AS SIGNED) FROM keyword WHERE date_format(c_date, '%Y-%m') = date_format(curdate(), '%Y-%m') GROUP BY keyword ORDER BY SUM(weight) DESC LIMIT 10;")
        result = cursor.fetchall()
        # 이번달에 대한 정보가 없을시 지난달에 대한 정보 출력
        if len(result) == 0:
            cursor.execute(
                "SELECT keyword, CAST(SUM(weight) AS SIGNED) FROM keyword WHERE date_format(c_date, '%Y-%m') = date_format((curdate() - INTERVAL 1 MONTH), '%Y-%m') GROUP BY keyword ORDER BY SUM(weight) DESC LIMIT 10;")
            result = cursor.fetchall()
        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed Selecting in StockList")

    for entry in result:
        labels.append(entry[0])
        data.append(entry[1])

    dic_data = {
        'labels': labels,
        'data': data
    }

    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})


def twitter_dy_data(request):
    today_datetime = (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")
    # MySQL 에서 오늘 기준 keyword 테이블에서 weight 기준 상위 10개 키워드 데이터 추출
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT keyword FROM keyword WHERE c_date = date(now()) ORDER BY weight DESC LIMIT 5;")
        keywords = list(cursor.fetchall())
        if len(keywords) != 0:
            cursor.execute(
                "SELECT keyword_id, CAST(SUM(retweet) AS SIGNED), CAST(SUM(like_count) AS SIGNED), group_concat(DISTINCT(nullif(tags, 'empty'))) FROM twitter WHERE SUBSTR(keyword_id, 1, 8) = date(now()) GROUP BY keyword_id ORDER BY COUNT(keyword_id) DESC;")
            twitter = cursor.fetchall()
        else:
            # 오늘 정보 없을 시 어제 정보출력
            cursor.execute(
                "SELECT keyword FROM keyword WHERE c_date = date_add(curdate(), interval -1 day) ORDER BY weight DESC LIMIT 5;")
            keywords = list(cursor.fetchall())
            cursor.execute(
                "SELECT keyword_id, CAST(SUM(retweet) AS SIGNED), CAST(SUM(like_count) AS SIGNED), group_concat(DISTINCT(nullif(tags, 'empty'))) FROM twitter WHERE SUBSTR(keyword_id, 1, 8) = date_add(curdate(), interval -1 day) GROUP BY keyword_id ORDER BY COUNT(keyword_id) DESC;")
            twitter = cursor.fetchall()
        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed Selecting in StockList")

    daily_twitter = {}
    no = 1
    while len(keywords) > 0:
        word = keywords.pop(0)
        for tweet in twitter:
            if word[0] in tweet[0]:
                daily_twitter[word[0]] = tweet[1:]
        no += 1

    labels = []
    data = []

    for i in range(len(daily_twitter.keys())):
        key = list(daily_twitter.keys())[i]
        value = list(daily_twitter.values())[i]
        value = list(value)
        value.insert(0, key)
        labels.append(i + 1)
        data.append(value)

    dic_data = {
        'labels': labels,
        'data': data
    }

    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})


def twitter_wk_data(request):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT keyword FROM keyword WHERE DATE(c_date) >= ADDDATE(curdate(), - WEEKDAY(curdate())) AND DATE(c_date) <= ADDDATE(curdate(), - WEEKDAY(curdate())+ 6) GROUP BY keyword ORDER BY SUM(weight) DESC LIMIT 5;")
        keywords = list(cursor.fetchall())
        if len(keywords) != 0:
            cursor.execute(
                "SELECT keyword_id, CAST(SUM(retweet) AS SIGNED), CAST(SUM(like_count) AS SIGNED), group_concat(DISTINCT(nullif(tags, 'empty'))) FROM twitter WHERE SUBSTR(keyword_id, 1, 8) >= ADDDATE(curdate(), - WEEKDAY(curdate())) AND SUBSTR(keyword_id, 1, 8) <= ADDDATE(curdate(), - WEEKDAY(curdate())+ 6) GROUP BY keyword_id ORDER BY COUNT(keyword_id) DESC;")
            twitter = cursor.fetchall()
        else:
            cursor.execute(
                "SELECT keyword FROM keyword WHERE DATE(c_date) >= ADDDATE(date_add(curdate(), interval -1 day), - WEEKDAY(date_add(curdate(), interval -1 day))) AND DATE(c_date) <= ADDDATE(date_add(curdate(), interval -1 day), - WEEKDAY(date_add(curdate(), interval -1 day))+ 6) GROUP BY keyword ORDER BY SUM(weight) DESC LIMIT 5;")
            keywords = list(cursor.fetchall())
            cursor.execute(
                "SELECT keyword_id, CAST(SUM(retweet) AS SIGNED), CAST(SUM(like_count) AS SIGNED), group_concat(DISTINCT(nullif(tags, 'empty'))) FROM twitter WHERE SUBSTR(keyword_id, 1, 8) >= ADDDATE(date_add(curdate(), interval -1 day), - WEEKDAY(date_add(curdate(), interval -1 day))) AND SUBSTR(keyword_id, 1, 8) <= ADDDATE(date_add(curdate(), interval -1 day), - WEEKDAY(date_add(curdate(), interval -1 day))+ 6) GROUP BY keyword_id ORDER BY COUNT(keyword_id) DESC;")
            twitter = cursor.fetchall()
        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed Selecting in StockList")

    weekly_twitter = {}
    for i in keywords:
        weekly_twitter[i[0]] = [0, 0, '']
    no = 1
    while len(keywords) > 0:
        word = keywords.pop(0)
        for tweet in twitter:
            if word[0] in tweet[0]:
                weekly_twitter[word[0]][0] += tweet[1]
                weekly_twitter[word[0]][1] += tweet[2]
                weekly_twitter[word[0]][2] += tweet[3]
        no += 1

    labels = []
    data = []

    for i in range(len(weekly_twitter.keys())):
        key = list(weekly_twitter.keys())[i]
        value = list(weekly_twitter.values())[i]
        value.insert(0, key)
        labels.append(i + 1)
        data.append(value)

    dic_data = {
        'labels': labels,
        'data': data
    }

    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})


def twitter_mt_data(request):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT keyword FROM keyword WHERE DATE(c_date) >= DATE_SUB(curdate(), INTERVAL (DAY(curdate())-1) DAY) AND DATE(c_date) <= LAST_DAY(NOW()) GROUP BY keyword ORDER BY SUM(weight) DESC LIMIT 5;")
        keywords = list(cursor.fetchall())
        if len(keywords) != 0:
            cursor.execute(
                "SELECT keyword_id, CAST(SUM(retweet) AS SIGNED), CAST(SUM(like_count) AS SIGNED), group_concat(DISTINCT(nullif(tags, 'empty'))) FROM twitter WHERE SUBSTR(keyword_id, 1, 8) >= DATE_SUB(curdate(), INTERVAL (DAY(curdate())-1) DAY) AND SUBSTR(keyword_id, 1, 8) <= LAST_DAY(NOW()) GROUP BY keyword_id ORDER BY COUNT(keyword_id) DESC;")
            twitter = cursor.fetchall()
        else:
            # 이번달 정보 없을 시 지난달 정보 출력
            cursor.execute(
                "SELECT keyword FROM keyword WHERE date_format(c_date, '%Y-%m') = date_format((curdate() - INTERVAL 1 MONTH), '%Y-%m') GROUP BY keyword ORDER BY SUM(weight) DESC LIMIT 5;")
            keywords = list(cursor.fetchall())
            cursor.execute(
                "SELECT keyword_id, CAST(SUM(retweet) AS SIGNED), CAST(SUM(like_count) AS SIGNED), group_concat(DISTINCT(nullif(tags, 'empty'))) FROM twitter WHERE SUBSTR(keyword_id, 1, 8) = date_format((curdate() - INTERVAL 1 MONTH), '%Y-%m') GROUP BY keyword_id ORDER BY COUNT(keyword_id) DESC;")
            twitter = cursor.fetchall()
        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed Selecting in StockList")

    monthly_twitter = {}
    for i in keywords:
        monthly_twitter[i[0]] = [0, 0, '']

    no = 1
    while len(keywords) > 0:
        word = keywords.pop(0)
        for tweet in twitter:
            if word[0] in tweet[0]:
                monthly_twitter[word[0]][0] += tweet[1]
                monthly_twitter[word[0]][1] += tweet[2]
                monthly_twitter[word[0]][2] += tweet[3]
        no += 1

    labels = []
    data = []

    for i in range(len(monthly_twitter.keys())):
        key = list(monthly_twitter.keys())[i]
        value = list(monthly_twitter.values())[i]
        value.insert(0, key)
        labels.append(i + 1)
        data.append(value)

    dic_data = {
        'labels': labels,
        'data': data
    }

    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})


def youtube_dy_data(request):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT keyword FROM keyword WHERE c_date = date(now()) ORDER BY weight DESC LIMIT 5;")
        keywords = list(cursor.fetchall())
        if len(keywords) != 0:
            cursor.execute(
                "SELECT keyword_id, CAST(SUM(view_count) AS SIGNED), CAST(SUM(like_count) AS SIGNED), CAST(SUM(comment_count) AS SIGNED), group_concat(tags) FROM youtube WHERE SUBSTR(keyword_id, 1, 8) = curdate() GROUP BY keyword_id ORDER BY COUNT(keyword_id) DESC;")
            youtube = cursor.fetchall()
        else:
            # 오늘 정보 없을 시 어제 정보 출력
            cursor.execute(
                "SELECT keyword FROM keyword WHERE c_date = date_add(curdate(), interval -1 day) ORDER BY weight DESC LIMIT 5;")
            keywords = list(cursor.fetchall())
            cursor.execute(
                "SELECT keyword_id, CAST(SUM(view_count) AS SIGNED), CAST(SUM(like_count) AS SIGNED), CAST(SUM(comment_count) AS SIGNED), group_concat(tags) FROM youtube WHERE SUBSTR(keyword_id, 1, 8) = date_add(curdate(), interval -1 day) GROUP BY keyword_id ORDER BY COUNT(keyword_id) DESC;")
            youtube = cursor.fetchall()
        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed Selecting in StockList")

    daily_youtube = {}
    no = 1
    while len(keywords) > 0:
        word = keywords.pop(0)
        for data in youtube:
            if word[0] in data[0]:
                daily_youtube[word[0]] = data[1:]
        no += 1

    labels = []
    data = []

    for i in range(len(daily_youtube.keys())):
        key = list(daily_youtube.keys())[i]
        value = list(daily_youtube.values())[i]
        value = list(value)
        value.insert(0, key)
        labels.append(i + 1)
        data.append(value)

    dic_data = {
        'labels': labels,
        'data': data
    }

    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})


def youtube_wk_data(request):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT keyword FROM keyword WHERE DATE(c_date) >= ADDDATE(curdate(), - WEEKDAY(curdate())) AND DATE(c_date) <= ADDDATE(curdate(), - WEEKDAY(curdate())+ 6) GROUP BY keyword ORDER BY SUM(weight) DESC LIMIT 5;")
        keywords = list(cursor.fetchall())
        if len(keywords) != 0:
            cursor.execute(
                "SELECT keyword_id, CAST(SUM(view_count) AS SIGNED), CAST(SUM(like_count) AS SIGNED), CAST(SUM(comment_count) AS SIGNED), group_concat(tags) FROM youtube WHERE SUBSTR(keyword_id, 1, 8) >= ADDDATE(curdate(), - WEEKDAY(curdate())) AND SUBSTR(keyword_id, 1, 8) <= ADDDATE(curdate(), - WEEKDAY(curdate())+ 6) GROUP BY keyword_id ORDER BY COUNT(keyword_id) DESC;")
            youtube = cursor.fetchall()
        else:
            # 이번주 정보 없을 시 지난주 정보 출력
            cursor.execute(
                "SELECT keyword FROM keyword WHERE DATE(c_date) >= ADDDATE(date_add(curdate(), interval -1 day), - WEEKDAY(date_add(curdate(), interval -1 day))) AND DATE(c_date) <= ADDDATE(date_add(curdate(), interval -1 day), - WEEKDAY(date_add(curdate(), interval -1 day))+ 6) ORDER BY weight DESC LIMIT 5;")
            keywords = list(cursor.fetchall())
            cursor.execute(
                "SELECT keyword_id, CAST(SUM(view_count) AS SIGNED), CAST(SUM(like_count) AS SIGNED), CAST(SUM(comment_count) AS SIGNED), group_concat(tags) FROM youtube WHERE SUBSTR(keyword_id, 1, 8) >= ADDDATE(date_add(curdate(), interval -1 day), - WEEKDAY(date_add(curdate(), interval -1 day))) AND SUBSTR(keyword_id, 1, 8) <= ADDDATE(date_add(curdate(), interval -1 day), - WEEKDAY(date_add(curdate(), interval -1 day))+ 6) GROUP BY keyword_id ORDER BY COUNT(keyword_id) DESC;")
            youtube = cursor.fetchall()
        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed Selecting in StockList")

    weekly_youtube = {}
    for i in keywords:
        weekly_youtube[i[0]] = [0, 0, 0, '']
    no = 1
    while len(keywords) > 0:
        word = keywords.pop(0)
        for data in youtube:
            if word[0] in data[0]:
                weekly_youtube[word[0]][0] += data[1]
                weekly_youtube[word[0]][1] += data[2]
                weekly_youtube[word[0]][2] += data[3]
                weekly_youtube[word[0]][3] += data[4]
        no += 1

    labels = []
    data = []

    for i in range(len(weekly_youtube.keys())):
        key = list(weekly_youtube.keys())[i]
        value = list(weekly_youtube.values())[i]
        value.insert(0, key)
        labels.append(i + 1)
        data.append(value)

    dic_data = {
        'labels': labels,
        'data': data
    }

    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})


def youtube_mt_data(request):
    try:
        cursor = connection.cursor()
        # DB keyword테이블에서 이번달 keyword별 언급량 합계 상위 5개의 keyword 추출
        cursor.execute(
            "SELECT keyword FROM keyword WHERE DATE(c_date) >= DATE_SUB(curdate(), INTERVAL (DAY(curdate())-1) DAY) AND DATE(c_date) <= LAST_DAY(NOW()) GROUP BY keyword ORDER BY SUM(weight) DESC LIMIT 5;")
        keywords = list(cursor.fetchall())
        if len(keywords) != 0:
            # DB youtube테이블에서 추출한 keywords의 키워드, 조회수, 좋아요 수, 댓글 수, 해시태그 모두 추출
            cursor.execute(
                "SELECT keyword_id, CAST(SUM(view_count) AS SIGNED), CAST(SUM(like_count) AS SIGNED), CAST(SUM(comment_count) AS SIGNED), group_concat(tags) FROM youtube  WHERE SUBSTR(keyword_id, 1, 8) >= DATE_SUB(curdate(), INTERVAL (DAY(curdate())-1) DAY) AND SUBSTR(keyword_id, 1, 8) <= LAST_DAY(NOW()) GROUP BY keyword_id ORDER BY COUNT(keyword_id) DESC;")
            youtube = cursor.fetchall()
        else:
            # 이번달 정보 없을 시 지난주 정보 출력
            cursor.execute(
                "SELECT keyword FROM keyword WHERE date_format(c_date, '%Y-%m') = date_format((curdate() - INTERVAL 1 MONTH), '%Y-%m') GROUP BY keyword ORDER BY SUM(weight) DESC LIMIT 5;")
            keywords = list(cursor.fetchall())
            cursor.execute(
                "SELECT keyword_id, CAST(SUM(view_count) AS SIGNED), CAST(SUM(like_count) AS SIGNED), CAST(SUM(comment_count) AS SIGNED), group_concat(tags) FROM youtube  WHERE SUBSTR(keyword_id, 1, 5) = date_format((curdate() - INTERVAL 1 MONTH), '%y-%m') GROUP BY keyword_id ORDER BY COUNT(keyword_id) DESC;")
            youtube = cursor.fetchall()
        connection.commit()
        connection.close()

    except:
        connection.rollback()
        print("Failed Selecting in StockList")

    # youtube테이블에서 추출한 정보 keyword별로 합치기
    monthly_youtube = {}
    for i in keywords:
        monthly_youtube[i[0]] = [0, 0, 0, '']
    no = 1
    while len(keywords) > 0:
        word = keywords.pop(0)
        for data in youtube:
            if word[0] in data[0]:
                monthly_youtube[word[0]][0] += data[1]
                monthly_youtube[word[0]][1] += data[2]
                monthly_youtube[word[0]][2] += data[3]
                monthly_youtube[word[0]][3] += data[4]
        no += 1

    labels = []
    data = []

    for i in range(len(monthly_youtube.keys())):
        key = list(monthly_youtube.keys())[i]
        value = list(monthly_youtube.values())[i]
        value.insert(0, key)
        labels.append(i + 1)
        data.append(value)

    dic_data = {
        'labels': labels,
        'data': data
    }

    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})


def data_daily_chart(request):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT keyword, weight FROM keyword WHERE c_date = curdate() ORDER BY weight DESC LIMIT 25;")
        today = dict(cursor.fetchall())
        if len(today) != 0:
            # 전날 top1~25출력
            cursor.execute(
                "SELECT keyword, weight FROM keyword WHERE c_date = date_add(curdate(), interval -1 day) ORDER BY weight DESC LIMIT 25;")
            yesterday = dict(cursor.fetchall())
        else:
            # 오늘 정보가 없을 시 어제,그저께 정보로 데이터 출력
            # 어제 top1~25출력
            cursor.execute(
                "SELECT keyword, weight FROM keyword WHERE c_date = date_add(curdate(), interval -1 day) ORDER BY weight DESC LIMIT 25;")
            today = dict(cursor.fetchall())
            # 그저께 top1~25출력
            cursor.execute(
                "SELECT keyword, weight FROM keyword WHERE c_date = date_add(curdate(), interval -2 day) ORDER BY weight DESC LIMIT 25;")
            yesterday = dict(cursor.fetchall())
        connection.commit()
        connection.close()
    except:
        connection.rollback()
        print("Failed Selecting in StockList")

    daily_chart = []

    for i in today.keys():
        if i in yesterday.keys():
            if today[i] > yesterday[i]:
                daily_chart.append([i, today[i], "up"])
            elif today[i] == yesterday[i]:
                daily_chart.append([i, today[i], "same"])
            else:
                daily_chart.append([i, today[i], "down"])
        else:
            daily_chart.append([i, today[i], "new"])

    dic_data = {
        'data': daily_chart
    }

    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})


def stacked_wk_data(request):
    from datetime import datetime
    date = datetime.today().strftime("%Y-%m-%d")

    weekly_chart = {}
    trans_dic = []
    try:
        cursor = connection.cursor()
        # DB keyword테이블에서 이번주 keyword별 언급량 합계 상위 5개의 keyword 추출
        cursor.execute(
            "SELECT keyword FROM keyword WHERE DATE(c_date) >= ADDDATE(curdate(), - WEEKDAY(curdate())) AND DATE(c_date) <= ADDDATE(curdate(), - WEEKDAY(curdate())+ 6) GROUP BY keyword ORDER BY SUM(weight) DESC LIMIT 5;")
        keywords = cursor.fetchall()
        # 이번주(월~일) 날짜 추출
        cursor.execute(
            "WITH RECURSIVE day AS (SELECT ADDDATE(curdate(), - WEEKDAY(curdate())) AS DAY UNION ALL SELECT DATE_ADD(DAY, INTERVAL 1 DAY) FROM day WHERE DAY < ADDDATE(curdate(), - WEEKDAY(curdate())+ 6)) SELECT date_format(DAY, '%Y-%m-%d') FROM day;")
        day = cursor.fetchall()

        # 이번주 데이터가 없을 시 지난주 데이터 추출
        if len(keywords) == 0:
            # DB keyword테이블에서 지난주 keyword별 언급량 합계 상위 5개의 keyword 추출
            cursor.execute(
                "SELECT keyword FROM keyword WHERE DATE(c_date) >= date_format(curdate() - INTERVAL 1 WEEK - WEEKDAY(curdate()), '%Y-%m-%d') AND DATE(c_date) <= date_format(curdate() - INTERVAL 1 WEEK + (6 - WEEKDAY(curdate())), '%Y-%m-%d') GROUP BY keyword ORDER BY SUM(weight) DESC LIMIT 5;")
            keywords = cursor.fetchall()
            # 지난주(월~일) 날짜 추출
            cursor.execute(
                "WITH RECURSIVE day AS (SELECT DATE(curdate() - INTERVAL 1 WEEK - WEEKDAY(curdate())) AS DAY UNION ALL SELECT DATE_ADD(DAY, INTERVAL 1 DAY) FROM day WHERE DAY < DATE(curdate() - INTERVAL 1 WEEK + (6 - WEEKDAY(curdate())))) SELECT date_format(DAY, '%Y-%m-%d') FROM day;")
            day = cursor.fetchall()

        # DB keyword테이블에서 추출한 keywords의 일별 weight 추출
        for i in range(5):
            weight = [0] * 7
            no = 0
            for d in day:
                if d[0] == date:
                    break
                else:
                    # 일별 추출한 keywords의 weight 추출
                    cursor.execute(
                        f"SELECT weight FROM keyword WHERE DATE(c_date) = '{d[0]}' AND keyword = '{keywords[i][0]}'")
                    daily_weight = list(cursor.fetchall())
                    if daily_weight != []:
                        weight[no] = daily_weight[0][0]
                    no += 1
            weekly_chart[keywords[i][0]] = weight
        connection.commit()
        connection.close()
    except:
        connection.rollback()
        print("Failed Selecting in StockList")



    for i in range(len(weekly_chart.keys())):
        key = list(weekly_chart.keys())[i]
        value = list(weekly_chart.values())[i]
        color = ["#3e95cd", "#2ecc71", "#f1c40f", "#9b59b6", "#e74c3c"]
        dic_kdc = {'label': key , 'data': value, "backgroundColor" : color[i]}
        trans_dic.append(dic_kdc)

    dic_data = {
        'labels': ["월", "화", "수", "목", "금", "토", "일"],
        'datasets': trans_dic
    }

    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})


def stacked_mt_data(request):
    import calendar
    from datetime import datetime
    date = datetime.today().strftime("%Y%m%d")
    last_day = calendar.monthrange(int(date[:4]), int(date[4:6]))[1]

    monthly_chart = {}
    trans_dic = []
    list_m_day = []

    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT keyword FROM keyword WHERE DATE(c_date) >= DATE_SUB(curdate(), INTERVAL (DAY(curdate())-1) DAY) AND DATE(c_date) <= LAST_DAY(NOW()) GROUP BY keyword ORDER BY SUM(weight) DESC LIMIT 5;")
        keywords = cursor.fetchall()
        if len(keywords) != 0:
            for i in range(5):
                cursor.execute(
                    f"SELECT weight FROM keyword WHERE DATE(c_date) >= DATE_SUB(curdate(), INTERVAL (DAY(curdate())-1) DAY) AND DATE(c_date) <= LAST_DAY(NOW()) AND keyword = '{keywords[i][0]}' ORDER BY c_date;")
                daily_weight = list(cursor.fetchall())
                weight = [0] * last_day
                for n in range(len(daily_weight)):
                    weight[n] = daily_weight[0][0]
                    monthly_chart[keywords[i][0]] = weight
        else:
            cursor.execute(
                "SELECT keyword FROM keyword WHERE date_format(c_date, '%Y-%m') = date_format((curdate() - INTERVAL 1 MONTH), '%Y-%m') GROUP BY keyword ORDER BY SUM(weight) DESC LIMIT 5;")
            keywords = cursor.fetchall()
            for i in range(5):
                cursor.execute(
                    f"SELECT weight FROM keyword WHERE date_format(c_date, '%Y-%m') = date_format((curdate() - INTERVAL 1 MONTH), '%Y-%m') AND keyword = '{keywords[i][0]}' ORDER BY c_date;")
                daily_weight = list(cursor.fetchall())
                weight = [0] * last_day
                for n in range(len(daily_weight)):
                    weight[n] = daily_weight[0][0]
                    monthly_chart[keywords[i][0]] = weight
        connection.commit()
        connection.close()
    except:
        connection.rollback()
        print("Failed Selecting in StockList")


    for i in range(len(monthly_chart.keys())):
        key = list(monthly_chart.keys())[i]
        value = list(monthly_chart.values())[i]
        color = ["#3e95cd", "#2ecc71", "#f1c40f", "#9b59b6", "#e74c3c"]
        dic_kdc = {'label': key, 'data': value, "backgroundColor": color[i]}
        trans_dic.append(dic_kdc)

    for i in range(last_day):
        i += 1
        list_m_day.append(i)

    dic_data = {
        'labels': list_m_day,
        'datasets': trans_dic
    }

    return JsonResponse(dic_data, json_dumps_params={'ensure_ascii': False})

