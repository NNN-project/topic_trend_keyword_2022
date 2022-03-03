# Topic Keyword Trend Analytics

검색 키워드 기준의 데이터가 아닌 발행된 키워드 데이터를 분석하기 위한 프로젝트
국내 메인 뉴스의 일별 뉴스 토픽에서 많이 발생하는 키워드들의 데이터와 해당 키워드가 소셜 미디어에서 언급된 데이터를 확인합니다.


> 수행기간: 2022.02.17 ~ 2022.03.02

## Data Collection
* 뉴스의 일별 토픽을 수집하는 기준: 각 종합 편성 채널의 저녁 메인 뉴스 헤드라인   
* 소셜 미디어 데이터: API를 제공하는 트위터, 유튜브   
* 데이터 수집 시간: 매일 오후 11시 30분   

## Getting Started
### Dependencies

* Python3.9
* Django == 3.5.0
* django-chartjs == 2.3.0
* mysqlclient == 2.1.0

## Usage
1. Project download
2. 명령프롬프트(CMD) 열기
3. 가상환경 생성 및 접속   
ex) https://wikidocs.net/70588
5. Dependencies 설치
```
Python3.9
Django == 3.5.0
django-chartjs == 2.3.0
mysqlclient == 2.1.0
```
5. Project 폴더에서 프로젝트 실행
```
python manage.py runserver
```
6. 명령프롬프트에 뜨는 로컬 주소로 접속 가능   
localhost:8000 or http://127.0.0.1:8000

## Demo
![chrome_GPmGUesEXb](https://user-images.githubusercontent.com/89976847/156387736-9b80ca81-55e5-4db7-99e8-65c3bdc4ef7c.gif)

## About
NNN Lab. 은 AI를 공부하다 만난 사람들이 업무가 아닌 취미로 프로젝트를 진행하기 위해 모인 팀입니다.

사람들: 최우진, 이재은, 김찬

##### Topic Keyword Trend Analytics by NNN lab.
