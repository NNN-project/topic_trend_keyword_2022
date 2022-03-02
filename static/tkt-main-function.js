//    <!-- 키워드 top10 #일간 -->
    $.ajax({
        url: '../tkt/json-keyword-top10-day/',
        dataType: "json",
        success: function (data) {
            var keyword_top10 = "";
            var color = ['primary', 'success','info','warning', 'Danger'];
            var pick_color = "";
            for (var i = 0; i < data.data.length; i++) {
                if (i < 5) {
                    pick_color = color[i]
                }else{
                    pick_color = color[i-5]
                }
                keyword_top10 += '<div class="col-xl-3 col-md-6 mb-4"><div class="card border-left-' + pick_color +' h-100 py-1"><div class="card-body"><div class="row no-gutters align-items-center"><div class="col mr-2">'
                keyword_top10 += '<div class="text-s font-weight-bold text-' + pick_color + ' text-uppercase mb-1">' + data.labels[i] + '</div>'
                keyword_top10 += '<div class="h4 mb-0 font-weight-bold text-gray-800">' + data.data[i] + '<span class="h6 mb-0">회 언급</span></div>'
                keyword_top10 += '</div></div></div></div></div>'
            }
            $('[id="keyword_top10_day"]').html(keyword_top10);
        },
        error: function (request, status, error) {
            console.log('실패');
        }
    });

//    <!-- 키워드 top10 #주간 -->
    $.ajax({
        url: '../tkt/json-keyword-top10-week/',
        dataType: "json",
        success: function (data) {
            var keyword_top10 = "";
            var color = ['primary', 'success','info','warning', 'Danger'];
            var pick_color = "";
            for (var i = 0; i < data.data.length; i++) {
                if (i < 5) {
                    pick_color = color[i]
                }else{
                    pick_color = color[i-5]
                }
                keyword_top10 += '<div class="col-xl-3 col-md-6 mb-4"><div class="card border-left-' + pick_color +' h-100 py-1"><div class="card-body"><div class="row no-gutters align-items-center"><div class="col mr-2">'
                keyword_top10 += '<div class="text-s font-weight-bold text-' + pick_color + ' text-uppercase mb-1">' + data.labels[i] + '</div>'
                keyword_top10 += '<div class="h4 mb-0 font-weight-bold text-gray-800">' + data.data[i] + '<span class="h6 mb-0">회 언급</span></div>'
                keyword_top10 += '</div></div></div></div></div>'
            }
            $('[id="keyword_top10_week"]').html(keyword_top10);
            console.log(data.labels[0]);

        },
        error: function (request, status, error) {
            console.log('실패');
        }
    });

//    <!-- 키워드 top10 #월간 -->
    $.ajax({
        url: '../tkt/json-keyword-top10-month/',
        dataType: "json",
        success: function (data) {
            var keyword_top10 = "";
            var color = ['primary', 'success','info','warning', 'Danger'];
            var pick_color = "";
            for (var i = 0; i < data.data.length; i++) {
                if (i < 5) {
                    pick_color = color[i]
                }else{
                    pick_color = color[i-5]
                }
                keyword_top10 += '<div class="col-xl-3 col-md-6 mb-4"><div class="card border-left-' + pick_color +' h-100 py-1"><div class="card-body"><div class="row no-gutters align-items-center"><div class="col mr-2">'
                keyword_top10 += '<div class="text-s font-weight-bold text-' + pick_color + ' text-uppercase mb-1">' + data.labels[i] + '</div>'
                keyword_top10 += '<div class="h4 mb-0 font-weight-bold text-gray-800">' + data.data[i] + '<span class="h6 mb-0">회 언급</span></div>'
                keyword_top10 += '</div></div></div></div></div>'
            }
            $('[id="keyword_top10_month"]').html(keyword_top10);
            console.log(data.labels[0]);

        },
        error: function (request, status, error) {
            console.log('실패');
        }
    });

//    <!-- Daily Topic Keyword Chart -->
    $.ajax({
        url: '../tkt/json-daily-chart/',
        dataType: "json",
        success: function (data) {
            var daily_top25 = "";
            var color = ['#e74c3c', '#3498db','#7f8c8d','#e67e22']; <!-- 상승, 하락, 동일, 뉴 -->
            for (var i = 0; i < data.data.length; i++) {
                switch (data.data[i][2]){
                    case 'up': status_color = color[0];
                        break;
                    case 'down': status_color = color[1];
                        break;
                    case 'same': status_color = color[2];
                        break;
                    case 'new': status_color = color[3];
                        break;
                }
                daily_top25 += '<tr>'
                daily_top25 += '<td>' + (i + 1) + '</td>'
                daily_top25 += '<td>' + data.data[i][0] + '</td>'
                daily_top25 += '<td>' + data.data[i][1] + '</td>'
                daily_top25 += '<td style = "color:'+ status_color +'">' + data.data[i][2] + '</td>'
                daily_top25 += '</tr>'

            }
            $('[id="daily_top25"]').html(daily_top25);
            console.log(data.labels[0]);

        },
        error: function (request, status, error) {
            console.log('실패');
        }
    });

//    <!-- Weekly Bar Chart -->
    $.ajax({
        url: '../tkt/json-stacked-wk-data/',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            console.log(data["labels"]);
            chart = new Chart(document.getElementById("stackedBarChart-wk"), {
                type: 'bar',
                data: {
                  labels: data.labels,
                  datasets: data.datasets
                },
            });
        },
        error: function (xhr, status, error) {

        },
        complete: function (data) {

        }
    });

//    <!-- Monthly Stacked Bar Chart -->
    $.ajax({
        url: '../tkt/json-stacked-mt-data/',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            console.log(data["labels"]);
            chart = new Chart(document.getElementById("stackedBarChart-mt"), {
                type: 'bar',
                data: {
                  labels: data.labels,
                  datasets: data.datasets
                },
                  options: {
                     scales: {
                        xAxes: [{
                            stacked: true
                        }],
                        yAxes: [{
                            stacked: true
                        }]
                    }
                  }
            });
        },
        error: function (xhr, status, error) {

        },
        complete: function (data) {

        }
    });

//    <!-- 트위터 테이블 -->
//    <!-- 트위터 테이블 일간 -->
    $.ajax({
        url: '../tkt/json-twitter-dy-data/',
        dataType: "json",
        success: function (data) {
            var twitter_retweet = "";
            var twitter_like = "";
            var twitter_tag = "";

            for (var i = 0; i < data.data.length; i++) {
                twitter_retweet += '<tr>'
                twitter_retweet += '<td width="5%">' + data.labels[i] +'.' + '</td>'
                twitter_retweet += '<td width="80%">' + data.data[i][0] + '</td>'
                twitter_retweet += '<td width="15%">' + data.data[i][1] + '</td>'
                twitter_retweet += '</tr>'

                twitter_like += '<tr>'
                twitter_like += '<td width="5">' + data.labels[i] +'.' + '</td>'
                twitter_like += '<td width="80%">' + data.data[i][0] + '</td>'
                twitter_like += '<td width="15%">' + data.data[i][2] + '</td>'
                twitter_like += '</tr>'

                twitter_tag += '<tr>'
                twitter_tag += '<td width="50px">' + data.labels[i] +'.' + '</td>'
                twitter_tag += '<td width="100px">' + data.data[i][0] + '</td>'
                twitter_tag += '<td style="overflow:hidden; white-space:nowrap; text-overflow:ellipsis; max-width:100px; ">' + data.data[i][3] + '</td>'
                twitter_tag += '</tr>'

            }
            $('[id="twitter_retweet_dy"]').html(twitter_retweet);
            $('[id="twitter_like_dy"]').html(twitter_like);
            $('[id="twitter_tag_dy"]').html(twitter_tag);

        },
        error: function (request, status, error) {
            console.log('실패');
        }
    });

//    <!-- 트위터 테이블 주간 -->
    $.ajax({
        url: '../tkt/json-twitter-wk-data/',
        dataType: "json",
        success: function (data) {
            var twitter_retweet = "";
            var twitter_like = "";
            var twitter_tag = "";

            for (var i = 0; i < data.data.length; i++) {
                twitter_retweet += '<tr>'
                twitter_retweet += '<td width="5%">' + data.labels[i] +'.' + '</td>'
                twitter_retweet += '<td width="80%">' + data.data[i][0] + '</td>'
                twitter_retweet += '<td width="15%">' + data.data[i][1] + '</td>'
                twitter_retweet += '</tr>'

                twitter_like += '<tr>'
                twitter_like += '<td width="5">' + data.labels[i] +'.' + '</td>'
                twitter_like += '<td width="80%">' + data.data[i][0] + '</td>'
                twitter_like += '<td width="15%">' + data.data[i][2] + '</td>'
                twitter_like += '</tr>'

                twitter_tag += '<tr>'
                twitter_tag += '<td width="50px">' + data.labels[i] +'.' + '</td>'
                twitter_tag += '<td width="100px">' + data.data[i][0] + '</td>'
                twitter_tag += '<td style="overflow:hidden; white-space:nowrap; text-overflow:ellipsis; max-width:100px; ">' + data.data[i][3] + '</td>'
                twitter_tag += '</tr>'

            }
            $('[id="twitter_retweet_wk"]').html(twitter_retweet);
            $('[id="twitter_like_wk"]').html(twitter_like);
            $('[id="twitter_tag_wk"]').html(twitter_tag);

        },
        error: function (request, status, error) {
            console.log('실패');
        }
    });

//    <!-- 트위터 테이블 월간 -->
    $.ajax({
        url: '../tkt/json-twitter-mt-data/',
        dataType: "json",
        success: function (data) {
            var twitter_retweet = "";
            var twitter_like = "";
            var twitter_tag = "";

            for (var i = 0; i < data.data.length; i++) {
                twitter_retweet += '<tr>'
                twitter_retweet += '<td width="5%">' + data.labels[i] +'.' + '</td>'
                twitter_retweet += '<td width="80%">' + data.data[i][0] + '</td>'
                twitter_retweet += '<td width="15%">' + data.data[i][1] + '</td>'
                twitter_retweet += '</tr>'

                twitter_like += '<tr>'
                twitter_like += '<td width="5%">' + data.labels[i] +'.' + '</td>'
                twitter_like += '<td width="80%">' + data.data[i][0] + '</td>'
                twitter_like += '<td width="15%">' + data.data[i][2] + '</td>'
                twitter_like += '</tr>'

                twitter_tag += '<tr>'
                twitter_tag += '<td width="50px">' + data.labels[i] +'.' + '</td>'
                twitter_tag += '<td width="100px">' + data.data[i][0] + '</td>'
                twitter_tag += '<td style="overflow:hidden; white-space:nowrap; text-overflow:ellipsis; max-width:100px; ">' + data.data[i][3] + '</td>'
                twitter_tag += '</tr>'

            }
            $('[id="twitter_retweet_mt"]').html(twitter_retweet);
            $('[id="twitter_like_mt"]').html(twitter_like);
            $('[id="twitter_tag_mt"]').html(twitter_tag);

        },
        error: function (request, status, error) {
            console.log('실패');
        }
    });

//    <!-- 유튜브 테이블 -->
//    <!-- 유튜브 테이블 일간-->
    $.ajax({
        url: '../tkt/json-youtube-dy-data/',
        dataType: "json",
        success: function (data) {
            var youtube_comment = "";
            var youtube_view = "";
            var youtube_like = "";
            var youtube_tag = "";

            for (var i = 0; i < data.data.length; i++) {
                youtube_comment += '<tr>'
                youtube_comment += '<td>' + data.labels[i] +'.' + '</td>'
                youtube_comment += '<td width="350px">' + data.data[i][0] + '</td>'
                youtube_comment += '<td>' + data.data[i][3] + '</td>'
                youtube_comment += '</tr>'

                youtube_view += '<tr>'
                youtube_view += '<td>' + data.labels[i] +'.' + '</td>'
                youtube_view += '<td width="350px">' + data.data[i][0] + '</td>'
                youtube_view += '<td>' + data.data[i][1] + '</td>'
                youtube_view += '</tr>'

                youtube_like += '<tr>'
                youtube_like += '<td>' + data.labels[i] +'.' + '</td>'
                youtube_like += '<td width="350px">' + data.data[i][0] + '</td>'
                youtube_like += '<td>' + data.data[i][2] + '</td>'
                youtube_like += '</tr>'

                youtube_tag += '<tr>'
                youtube_tag += '<td width="50px">' + data.labels[i] +'.' + '</td>'
                youtube_tag += '<td width="100px">' + data.data[i][0] + '</td>'
                youtube_tag += '<td style="overflow:hidden; white-space:nowrap; text-overflow:ellipsis; max-width:100px; ">' + data.data[i][4] + '</td>'
                youtube_tag += '</tr>'

            }
            $('[id="youtube_comment_dy"]').html(youtube_comment);
            $('[id="youtube_view_dy"]').html(youtube_view);
            $('[id="youtube_like_dy"]').html(youtube_like);
            $('[id="youtube_tag_dy"]').html(youtube_tag);

        },
        error: function (request, status, error) {
            console.log('실패');
        }
    });
//    <!-- 유튜브 테이블 주간-->
    $.ajax({
        url: '../tkt/json-youtube-wk-data/',
        dataType: "json",
        success: function (data) {
            var youtube_comment = "";
            var youtube_view = "";
            var youtube_like = "";
            var youtube_tag = "";

            for (var i = 0; i < data.data.length; i++) {
                youtube_comment += '<tr>'
                youtube_comment += '<td>' + data.labels[i] +'.' + '</td>'
                youtube_comment += '<td width="350px">' + data.data[i][0] + '</td>'
                youtube_comment += '<td>' + data.data[i][3] + '</td>'
                youtube_comment += '</tr>'

                youtube_view += '<tr>'
                youtube_view += '<td>' + data.labels[i] +'.' + '</td>'
                youtube_view += '<td width="350px">' + data.data[i][0] + '</td>'
                youtube_view += '<td>' + data.data[i][1] + '</td>'
                youtube_view += '</tr>'

                youtube_like += '<tr>'
                youtube_like += '<td>' + data.labels[i] +'.' + '</td>'
                youtube_like += '<td width="350px">' + data.data[i][0] + '</td>'
                youtube_like += '<td>' + data.data[i][2] + '</td>'
                youtube_like += '</tr>'

                youtube_tag += '<tr>'
                youtube_tag += '<td width="50px">' + data.labels[i] +'.' + '</td>'
                youtube_tag += '<td width="100px">' + data.data[i][0] + '</td>'
                youtube_tag += '<td style="overflow:hidden; white-space:nowrap; text-overflow:ellipsis; max-width:100px; ">' + data.data[i][4] + '</td>'
                youtube_tag += '</tr>'

            }
            $('[id="youtube_comment_wk"]').html(youtube_comment);
            $('[id="youtube_view_wk"]').html(youtube_view);
            $('[id="youtube_like_wk"]').html(youtube_like);
            $('[id="youtube_tag_wk"]').html(youtube_tag);

        },
        error: function (request, status, error) {
            console.log('실패');
        }
    });
//    <!-- 유튜브 테이블 월간-->
    $.ajax({
        url: '../tkt/json-youtube-mt-data/',
        dataType: "json",
        success: function (data) {
            var youtube_comment = "";
            var youtube_view = "";
            var youtube_like = "";
            var youtube_tag = "";

            for (var i = 0; i < data.data.length; i++) {
                youtube_comment += '<tr>'
                youtube_comment += '<td>' + data.labels[i] +'.' + '</td>'
                youtube_comment += '<td width="350px">' + data.data[i][0] + '</td>'
                youtube_comment += '<td>' + data.data[i][3] + '</td>'
                youtube_comment += '</tr>'

                youtube_view += '<tr>'
                youtube_view += '<td>' + data.labels[i] +'.' + '</td>'
                youtube_view += '<td width="350px">' + data.data[i][0] + '</td>'
                youtube_view += '<td>' + data.data[i][1] + '</td>'
                youtube_view += '</tr>'

                youtube_like += '<tr>'
                youtube_like += '<td>' + data.labels[i] +'.' + '</td>'
                youtube_like += '<td width="350px">' + data.data[i][0] + '</td>'
                youtube_like += '<td>' + data.data[i][2] + '</td>'
                youtube_like += '</tr>'

                youtube_tag += '<tr>'
                youtube_tag += '<td width="50px">' + data.labels[i] +'.' + '</td>'
                youtube_tag += '<td width="100px">' + data.data[i][0] + '</td>'
                youtube_tag += '<td style="overflow:hidden; white-space:nowrap; text-overflow:ellipsis; max-width:100px; ">' + data.data[i][4] + '</td>'
                youtube_tag += '</tr>'

            }
            $('[id="youtube_comment_mt"]').html(youtube_comment);
            $('[id="youtube_view_mt"]').html(youtube_view);
            $('[id="youtube_like_mt"]').html(youtube_like);
            $('[id="youtube_tag_mt"]').html(youtube_tag);

        },
        error: function (request, status, error) {
            console.log('실패');
        }
    });