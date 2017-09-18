# -*- coding: utf-8 -*-
import json

from flask import request, g
from flask_cors import *

import kuas_api.kuas.ap as ap
import kuas_api.kuas.user as user
import kuas_api.kuas.cache as cache

from kuas_api.modules.json import jsonify
from kuas_api.modules.stateless_auth import auth
import kuas_api.modules.stateless_auth as stateless_auth
import kuas_api.modules.const as const
import kuas_api.modules.error as error
from .doc import auto

# Nestable blueprints problem
# not sure isn't this a best practice now.
# https://github.com/mitsuhiko/flask/issues/593
routes = []


def route(rule, **options):
    def decorator(f):
        url_rule = {
            "rule": rule,
            "view_func": f,
            "options": options if options else {}
        }

        routes.append(url_rule)
        return f

    return decorator


@route('/ap/users/info')
@auth.login_required
def ap_user_info():
    """Get user's information.

    :reqheader Authorization: Using Basic Auth
    :resjson string class: User's class name
    :resjson string education_system: User's scheme
    :resjson string department: User's department
    :resjson string student_id: User's student identifier
    :resjson string student_name_cht: User's name in Chinese
    :resjson string student_name_eng: User's name in English
    :statuscode 200: Query successful
    :statuscode 401: Login failed or auth_token has been expired

    **Request**

    .. sourcecode:: http

        GET /latest/ap/users/info HTTP/1.1
        Host: kuas.grd.idv.tw:14769
        Authorization: Basic xxxxxxxxxxxxx=

    .. sourcecode:: shell

        curl -X GET -u username:password https://kuas.grd.idv.tw:14769/latest/ap/users/info


    **Response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: text/html; charset=utf-8

        {
            "class":"四資工三甲",
            "education_system":"日間部四技",
            "department":"資訊工程系",
            "student_id":"1104137***",
            "student_name_cht":"顏**",
            "student_name_eng":""
        }
    """
    # Restore cookies
    s = stateless_auth.get_requests_session_with_cookies()

    return json.dumps(user.get_user_info(s), ensure_ascii=False)


@route('/ap/users/picture')
@auth.login_required
def ap_user_picture():
    """Get user's picture URL.

    :reqheader Authorization: Using Basic Auth
    :statuscode 200: Query successful
    :statuscode 401: Login failed or auth_token has been expired

    **Request**

    .. sourcecode:: http

        GET /latest/ap/users/info HTTP/1.1
        Host: kuas.grd.idv.tw:14769
        Authorization: Basic xxxxxxxxxxxxx=

    .. sourcecode:: shell

        curl -X GET -u username:password https://kuas.grd.idv.tw:14769/latest/ap/users/picture


    **Response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: text/html; charset=utf-8

        http://140.127.113.231/kuas/stdpics/1104137***_20170803213***.jpg
    """
   # Restore cookies
    s = stateless_auth.get_requests_session_with_cookies()

    return user.get_user_picture(s)


@route('/ap/users/coursetables/<int:year>/<int:semester>')
@auth.login_required
def get_coursetables(year, semester):
    """Get user's class schedule.

    :reqheader Authorization: Using Basic Auth
    :query int year: Specific year to query class schedule. format: yyy (see below)
    :query int semester: Given a semester
    :statuscode 200: Query successful
    :statuscode 401: Login failed or auth_token has been expired

    **Request**

    .. sourcecode:: http

        GET /latest/ap/users/info HTTP/1.1
        Host: kuas.grd.idv.tw:14769
        Authorization: Basic xxxxxxxxxxxxx=

    .. sourcecode:: shell

        curl -X GET -u username:password https://kuas.grd.idv.tw:14769/\\
        latest/ap/users/coursetables/106/1


    **Response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json
    
        {
           "status":200,
           "coursetables":{
              "Tuesday":[
                 {
                    "instructors":[
                       "張雲龍"
                    ],
                    "date":{
                       "weekday":"T",
                       "start_time":"09:10",
                       "end_time":"10:00",
                       "section":"第 2 節"
                    },
                    "title":"生物資訊概論",
                    "location":{
                       "building":"",
                       "room":"資002"
                    }
                 },
                 {
                    "instructors":[
                       "張雲龍"
                    ],
                    "date":{
                       "weekday":"T",
                       "start_time":"10:10",
                       "end_time":"11:00",
                       "section":"第 3 節"
                    },
                    "title":"生物資訊概論",
                    "location":{
                       "building":"",
                       "room":"資002"
                    }
                 },
                 {
                    "instructors":[
                       "張雲龍"
                    ],
                    "date":{
                       "weekday":"T",
                       "start_time":"11:10",
                       "end_time":"12:00",
                       "section":"第 4 節"
                    },
                    "title":"生物資訊概論",
                    "location":{
                       "building":"",
                       "room":"資002"
                    }
                 },
                 {
                    "instructors":[
                       "呂明秀"
                    ],
                    "date":{
                       "weekday":"T",
                       "start_time":"",
                       "end_time":"",
                       "section":"A"
                    },
                    "title":"體育－體適能加強班NTC",
                    "location":{
                       "building":"",
                       "room":""
                    }
                 },
                 {
                    "instructors":[
                       "羅孟彥"
                    ],
                    "date":{
                       "weekday":"T",
                       "start_time":"13:30",
                       "end_time":"14:20",
                       "section":"第 5 節"
                    },
                    "title":"物件導向程式設計",
                    "location":{
                       "building":"",
                       "room":"資201"
                    }
                 },
                 {
                    "instructors":[
                       "羅孟彥"
                    ],
                    "date":{
                       "weekday":"T",
                       "start_time":"14:30",
                       "end_time":"15:20",
                       "section":"第 6 節"
                    },
                    "title":"物件導向程式設計",
                    "location":{
                       "building":"",
                       "room":"資201"
                    }
                 },
                 {
                    "instructors":[
                       "羅孟彥"
                    ],
                    "date":{
                       "weekday":"T",
                       "start_time":"15:30",
                       "end_time":"16:20",
                       "section":"第 7 節"
                    },
                    "title":"物件導向程式設計",
                    "location":{
                       "building":"",
                       "room":"資201"
                    }
                 }
              ],
              "Wednesday":[
                 {
                    "instructors":[
                       "洪靖婷"
                    ],
                    "date":{
                       "weekday":"W",
                       "start_time":"08:10",
                       "end_time":"09:00",
                       "section":"第 1 節"
                    },
                    "title":"應用文與習作",
                    "location":{
                       "building":"",
                       "room":"育302"
                    }
                 },
                 {
                    "instructors":[
                       "洪靖婷"
                    ],
                    "date":{
                       "weekday":"W",
                       "start_time":"09:10",
                       "end_time":"10:00",
                       "section":"第 2 節"
                    },
                    "title":"應用文與習作",
                    "location":{
                       "building":"",
                       "room":"育302"
                    }
                 },
                 {
                    "instructors":[
                       "陳正山"
                    ],
                    "date":{
                       "weekday":"W",
                       "start_time":"10:10",
                       "end_time":"11:00",
                       "section":"第 3 節"
                    },
                    "title":"英語聽講訓練(一)",
                    "location":{
                       "building":"",
                       "room":"育303"
                    }
                 },
                 {
                    "instructors":[
                       "陳正山"
                    ],
                    "date":{
                       "weekday":"W",
                       "start_time":"11:10",
                       "end_time":"12:00",
                       "section":"第 4 節"
                    },
                    "title":"英語聽講訓練(一)",
                    "location":{
                       "building":"",
                       "room":"育303"
                    }
                 },
                 {
                    "instructors":[
                       "魏文欽"
                    ],
                    "date":{
                       "weekday":"W",
                       "start_time":"13:30",
                       "end_time":"14:20",
                       "section":"第 5 節"
                    },
                    "title":"延伸通識(社會)-法律與生活",
                    "location":{
                       "building":"",
                       "room":"HS316"
                    }
                 },
                 {
                    "instructors":[
                       "魏文欽"
                    ],
                    "date":{
                       "weekday":"W",
                       "start_time":"14:30",
                       "end_time":"15:20",
                       "section":"第 6 節"
                    },
                    "title":"延伸通識(社會)-法律與生活",
                    "location":{
                       "building":"",
                       "room":"HS316"
                    }
                 }
              ],
              "Monday":[
                 {
                    "instructors":[
                       "張道行"
                    ],
                    "date":{
                       "weekday":"M",
                       "start_time":"13:30",
                       "end_time":"14:20",
                       "section":"第 5 節"
                    },
                    "title":"計算機結構",
                    "location":{
                       "building":"",
                       "room":"南101"
                    }
                 },
                 {
                    "instructors":[
                       "張道行"
                    ],
                    "date":{
                       "weekday":"M",
                       "start_time":"14:30",
                       "end_time":"15:20",
                       "section":"第 6 節"
                    },
                    "title":"計算機結構",
                    "location":{
                       "building":"",
                       "room":"南101"
                    }
                 },
                 {
                    "instructors":[
                       "張道行"
                    ],
                    "date":{
                       "weekday":"M",
                       "start_time":"15:30",
                       "end_time":"16:20",
                       "section":"第 7 節"
                    },
                    "title":"計算機結構",
                    "location":{
                       "building":"",
                       "room":"南101"
                    }
                 }
              ],
              "Thursday":[
                 {
                    "instructors":[
                       "蕭淳元"
                    ],
                    "date":{
                       "weekday":"R",
                       "start_time":"09:10",
                       "end_time":"10:00",
                       "section":"第 2 節"
                    },
                    "title":"資料結構",
                    "location":{
                       "building":"",
                       "room":"育302"
                    }
                 },
                 {
                    "instructors":[
                       "蕭淳元"
                    ],
                    "date":{
                       "weekday":"R",
                       "start_time":"10:10",
                       "end_time":"11:00",
                       "section":"第 3 節"
                    },
                    "title":"資料結構",
                    "location":{
                       "building":"",
                       "room":"育302"
                    }
                 },
                 {
                    "instructors":[
                       "蕭淳元"
                    ],
                    "date":{
                       "weekday":"R",
                       "start_time":"11:10",
                       "end_time":"12:00",
                       "section":"第 4 節"
                    },
                    "title":"資料結構",
                    "location":{
                       "building":"",
                       "room":"育302"
                    }
                 },
                 {
                    "instructors":[
                       "呂明秀"
                    ],
                    "date":{
                       "weekday":"R",
                       "start_time":"",
                       "end_time":"",
                       "section":"A"
                    },
                    "title":"體育－體適能加強班NTC",
                    "location":{
                       "building":"",
                       "room":""
                    }
                 }
              ]
           },
           "messages":""
        }
    """
    # See Gist for more infomation.
    # https://gist.github.com/hearsilent/a2570371cc6aa7db97bb

    weekdays = {"M": "Monday", "T": "Tuesday", "W": "Wednesday",
                "R": "Thursday", "F": "Friday", "S": "Saturday",
                "H": "Sunday"
                }

    # Restore cookies
    s = stateless_auth.get_requests_session_with_cookies()

    classes = cache.ap_query(
        s, "ag222", {"arg01": year, "arg02": semester}, g.username)

    # No Content
    if not classes:
        return jsonify(status=const.no_content, messages="學生目前無選課資料", coursetables=classes)

    coursetables = {}
    for c in classes:
        weekday = weekdays[c["date"]["weekday"]]
        if not weekday in coursetables:
            coursetables[weekday] = []

        coursetables[weekday].append(c)

    return jsonify(status=const.ok, messages="", coursetables=coursetables)


@route('/ap/users/scores/<int:year>/<int:semester>')
@auth.login_required
def get_score(year, semester):
    """Get user's scores.

    :reqheader Authorization: Using Basic Auth
    :query int year: Specific year to query class schedule. format: yyy (see below)
    :query int semester: Set semester to query class schedule. value: 1~4 (see below)
    :statuscode 200: Query successful
    :statuscode 401: Login failed or auth_token has been expired

    **Request**

    .. sourcecode:: http

        GET /latest/ap/users/info HTTP/1.1
        Host: kuas.grd.idv.tw:14769
        Authorization: Basic xxxxxxxxxxxxx=

    .. sourcecode:: shell

        curl -X GET -u username:password https://kuas.grd.idv.tw:14769/\\
        latest/ap/users/scores/105/2


    **Response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: application/json
       

        {
          "status":200,
          "messages":"",
          "scores":{
            "detail":{
              "conduct":82.0,
              "class_rank":"44/56",
              "average":70.33,
              "class_percentage":78.57
            },
            "scores":[
              {
                "required":"【選修】",
                "hours":"3.0",
                "title":"系統程式",
                "remark":"",
                "middle_score":"*",
                "units":"3.0",
                "final_score":"60.00",
                "at":"【學期】"
              },
              {
                "required":"【必修】",
                "hours":"3.0",
                "title":"物理(二)",
                "remark":"停修",
                "middle_score":"*",
                "units":"3.0",
                "final_score":"0.00",
                "at":"【學期】"
              },
              {
                "required":"【必修】",
                "hours":"2.0",
                "title":"英語聽講訓練(二)",
                "remark":"",
                "middle_score":"85.00",
                "units":"1.0",
                "final_score":"75.00",
                "at":"【學期】"
              },
              {
                "required":"【必修】",
                "hours":"3.0",
                "title":"計算機網路",
                "remark":"",
                "middle_score":"*",
                "units":"3.0",
                "final_score":"63.00",
                "at":"【學期】"
              },
              {
                "required":"【選修】",
                "hours":"3.0",
                "title":"視窗程式設計",
                "remark":"",
                "middle_score":"76.00",
                "units":"3.0",
                "final_score":"76.00",
                "at":"【學期】"
              },
              {
                "required":"【必修】",
                "hours":"3.0",
                "title":"微處理機",
                "remark":"",
                "middle_score":"*",
                "units":"3.0",
                "final_score":"79.00",
                "at":"【學期】"
              },
              {
                "required":"【必修】",
                "hours":"3.0",
                "title":"線性代數",
                "remark":"",
                "middle_score":"*",
                "units":"3.0",
                "final_score":"59.00",
                "at":"【學期】"
              },
              {
                "required":"【必修】",
                "hours":"3.0",
                "title":"機率與統計",
                "remark":"",
                "middle_score":"80.00",
                "units":"3.0",
                "final_score":"67.00",
                "at":"【學期】"
              },
              {
                "required":"【必修】",
                "hours":"2.0",
                "title":"延伸通識(科技)-近代科技概論",
                "remark":"",
                "middle_score":"*",
                "units":"2.0",
                "final_score":"95.00",
                "at":"【學期】"
              },
              {
                "required":"【必修】",
                "hours":"2.0",
                "title":"體育－體適能加強班NTC",
                "remark":"",
                "middle_score":"*",
                "units":"0",
                "final_score":"0.00",
                "at":"【學期】"
              }
            ]
          }
        }
    """
    # Restore cookies
    s = stateless_auth.get_requests_session_with_cookies()

    scores = cache.ap_query(
        s, "ag008", {"arg01": year, "arg02": semester, "arg03": g.username}, g.username)

    if not scores:
        return jsonify(status=const.no_content, messages="目前無學生個人成績資料", scores={})

    return jsonify(status=const.ok, messages="", scores=scores)


@route('/ap/samples/coursetables/normal')
@route('/ap/samples/coursetables/all')
@route('/ap/samples/coursetables/aftereight')
@route('/ap/samples/coursetables/weekends')
@route('/ap/samples/coursetables/multiinstructors')
@route('/ap/samples/coursetables/wtf')
def get_sample_coursetables():
    sample_data = {
        "normal": {'Wednesday': [{'date': {'weekday': 'W', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '南101', 'building': ''}, 'instructors': ['張道行'], 'title': '演算法'}, {'date': {'weekday': 'W', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '南101', 'building': ''}, 'instructors': ['張道行'], 'title': '演算法'}, {'date': {'weekday': 'W', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': '南101', 'building': ''}, 'instructors': ['張道行'], 'title': '演算法'}], 'Thursday': [{'date': {'weekday': 'R', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '資201', 'building': ''}, 'instructors': ['楊孟翰'], 'title': '資料庫'}, {'date': {'weekday': 'R', 'end_time': '11:00', 'start_time': '10:10', 'section': '第 3 節'}, 'location': {'room': '資201', 'building': ''}, 'instructors': ['楊孟翰'], 'title': '資料庫'}, {'date': {'weekday': 'R', 'end_time': '12:00', 'start_time': '11:10', 'section': '第 4 節'}, 'location': {'room': '資201', 'building': ''}, 'instructors': ['楊孟翰'], 'title': '資料庫'}, {'date': {'weekday': 'R', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': 'HS210', 'building': ''}, 'instructors': ['詹喆君'], 'title': '延伸通識(人文)-音樂賞析'}, {'date': {'weekday': 'R', 'end_time': '17:20', 'start_time': '16:30', 'section': '第 8 節'}, 'location': {'room': 'HS210', 'building': ''}, 'instructors': ['詹喆君'], 'title': '延伸通識(人文)-音樂賞析'}], 'Tuesday': [{'date': {'weekday': 'T', 'end_time': '09:00', 'start_time': '08:10', 'section': '第 1 節'}, 'location': {'room': '', 'building': ''}, 'instructors': ['陳忠信'], 'title': '體育－羽球'}, {'date': {'weekday': 'T', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '', 'building': ''}, 'instructors': ['陳忠信'], 'title': '體育－羽球'}, {'date': {'weekday': 'T', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '南108', 'building': ''}, 'instructors': ['林威成'], 'title': '離散數學'}, {'date': {'weekday': 'T', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '南108', 'building': ''}, 'instructors': ['林威成'], 'title': '離散數學'}, {'date': {'weekday': 'T', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': '南108', 'building': ''}, 'instructors': ['林威成'], 'title': '離散數學'}], 'Monday': [{'date': {'weekday': 'M', 'end_time': '09:00', 'start_time': '08:10', 'section': '第 1 節'}, 'location': {'room': '育302', 'building': ''}, 'instructors': ['林良志'], 'title': '核心通識(五)-民主與法治'}, {'date': {'weekday': 'M', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '育302', 'building': ''}, 'instructors': ['林良志'], 'title': '核心通識(五)-民主與法治'}, {'date': {'weekday': 'M', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '育302', 'building': ''}, 'instructors': ['鐘文鈺'], 'title': '資料壓縮'}, {'date': {'weekday': 'M', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '育302', 'building': ''}, 'instructors': ['鐘文鈺'], 'title': '資料壓縮'}, {'date': {'weekday': 'M', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': '育302', 'building': ''}, 'instructors': ['鐘文鈺'], 'title': '資料壓縮'}], 'Friday': [{'date': {'weekday': 'F', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '資201', 'building': ''}, 'instructors': ['王志強'], 'title': '作業系統'}, {'date': {'weekday': 'F', 'end_time': '11:00', 'start_time': '10:10', 'section': '第 3 節'}, 'location': {'room': '資201', 'building': ''}, 'instructors': ['王志強'], 'title': '作業系統'}, {'date': {'weekday': 'F', 'end_time': '12:00', 'start_time': '11:10', 'section': '第 4 節'}, 'location': {'room': '資201', 'building': ''}, 'instructors': ['王志強'], 'title': '作業系統'}]},
        "weekends": {'Monday': [{'date': {'weekday': 'M', 'end_time': '09:00', 'start_time': '08:10', 'section': '第 1 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '核心通識(五)-民主與法治', 'instructors': ['林良志']}, {'date': {'weekday': 'M', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '核心通識(五)-民主與法治', 'instructors': ['林良志']}, {'date': {'weekday': 'M', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '資料壓縮', 'instructors': ['鐘文鈺']}, {'date': {'weekday': 'M', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '資料壓縮', 'instructors': ['鐘文鈺']}, {'date': {'weekday': 'M', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '資料壓縮', 'instructors': ['鐘文鈺']}], 'Sunday': [{'date': {'weekday': 'H', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '', 'building': ''}, 'title': '實務專題(一)', 'instructors': ['羅孟彥']}, {'date': {'weekday': 'H', 'end_time': '11:00', 'start_time': '10:10', 'section': '第 3 節'}, 'location': {'room': '', 'building': ''}, 'title': '實務專題(一)', 'instructors': ['羅孟彥']}, {'date': {'weekday': 'H', 'end_time': '12:00', 'start_time': '11:10', 'section': '第 4 節'}, 'location': {'room': '', 'building': ''}, 'title': '實務專題(一)', 'instructors': ['羅孟彥']}, {'date': {'weekday': 'H', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '', 'building': ''}, 'title': '英語能力訓練', 'instructors': ['秦月貞']}, {'date': {'weekday': 'H', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '', 'building': ''}, 'title': '英語能力訓練', 'instructors': ['秦月貞']}], 'Thursday': [{'date': {'weekday': 'R', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '資料庫', 'instructors': ['楊孟翰']}, {'date': {'weekday': 'R', 'end_time': '11:00', 'start_time': '10:10', 'section': '第 3 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '資料庫', 'instructors': ['楊孟翰']}, {'date': {'weekday': 'R', 'end_time': '12:00', 'start_time': '11:10', 'section': '第 4 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '資料庫', 'instructors': ['楊孟翰']}, {'date': {'weekday': 'R', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': 'HS210', 'building': ''}, 'title': '延伸通識(人文)-音樂賞析', 'instructors': ['詹喆君']}, {'date': {'weekday': 'R', 'end_time': '17:20', 'start_time': '16:30', 'section': '第 8 節'}, 'location': {'room': 'HS210', 'building': ''}, 'title': '延伸通識(人文)-音樂賞析', 'instructors': ['詹喆君']}], 'Tuesday': [{'date': {'weekday': 'T', 'end_time': '09:00', 'start_time': '08:10', 'section': '第 1 節'}, 'location': {'room': '', 'building': ''}, 'title': '體育－羽球', 'instructors': ['陳忠信']}, {'date': {'weekday': 'T', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '', 'building': ''}, 'title': '體育－羽球', 'instructors': ['陳忠信']}, {'date': {'weekday': 'T', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '南108', 'building': ''}, 'title': '離散數學', 'instructors': ['林威成']}, {'date': {'weekday': 'T', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '南108', 'building': ''}, 'title': '離散數學', 'instructors': ['林威成']}, {'date': {'weekday': 'T', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': '南108', 'building': ''}, 'title': '離散數學', 'instructors': ['林威成']}], 'Wednesday': [{'date': {'weekday': 'W', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '南101', 'building': ''}, 'title': '演算法', 'instructors': ['張道行']}, {'date': {'weekday': 'W', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '南101', 'building': ''}, 'title': '演算法', 'instructors': ['張道行']}, {'date': {'weekday': 'W', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': '南101', 'building': ''}, 'title': '演算法', 'instructors': ['張道行']}], 'Friday': [{'date': {'weekday': 'F', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '作業系統', 'instructors': ['王志強']}, {'date': {'weekday': 'F', 'end_time': '11:00', 'start_time': '10:10', 'section': '第 3 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '作業系統', 'instructors': ['王志強']}, {'date': {'weekday': 'F', 'end_time': '12:00', 'start_time': '11:10', 'section': '第 4 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '作業系統', 'instructors': ['王志強']}]},
        "aftereight": {'Monday': [{'date': {'weekday': 'M', 'end_time': '09:00', 'start_time': '08:10', 'section': '第 1 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '核心通識(五)-民主與法治', 'instructors': ['林良志']}, {'date': {'weekday': 'M', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '核心通識(五)-民主與法治', 'instructors': ['林良志']}, {'date': {'weekday': 'M', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '資料壓縮', 'instructors': ['鐘文鈺']}, {'date': {'weekday': 'M', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '資料壓縮', 'instructors': ['鐘文鈺']}, {'date': {'weekday': 'M', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '資料壓縮', 'instructors': ['鐘文鈺']}], 'Thursday': [{'date': {'weekday': 'R', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '資料庫', 'instructors': ['楊孟翰']}, {'date': {'weekday': 'R', 'end_time': '11:00', 'start_time': '10:10', 'section': '第 3 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '資料庫', 'instructors': ['楊孟翰']}, {'date': {'weekday': 'R', 'end_time': '12:00', 'start_time': '11:10', 'section': '第 4 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '資料庫', 'instructors': ['楊孟翰']}, {'date': {'weekday': 'R', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': 'HS210', 'building': ''}, 'title': '延伸通識(人文)-音樂賞析', 'instructors': ['詹喆君']}, {'date': {'weekday': 'R', 'end_time': '17:20', 'start_time': '16:30', 'section': '第 8 節'}, 'location': {'room': 'HS210', 'building': ''}, 'title': '延伸通識(人文)-音樂賞析', 'instructors': ['詹喆君']}], 'Tuesday': [{'date': {'weekday': 'T', 'end_time': '09:00', 'start_time': '08:10', 'section': '第 1 節'}, 'location': {'room': '', 'building': ''}, 'title': '體育－羽球', 'instructors': ['陳忠信']}, {'date': {'weekday': 'T', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '', 'building': ''}, 'title': '體育－羽球', 'instructors': ['陳忠信']}, {'date': {'weekday': 'T', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '南108', 'building': ''}, 'title': '離散數學', 'instructors': ['林威成']}, {'date': {'weekday': 'T', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '南108', 'building': ''}, 'title': '離散數學', 'instructors': ['林威成']}, {'date': {'weekday': 'T', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': '南108', 'building': ''}, 'title': '離散數學', 'instructors': ['林威成']}], 'Wednesday': [{'date': {'weekday': 'W', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '南101', 'building': ''}, 'title': '演算法', 'instructors': ['張道行']}, {'date': {'weekday': 'W', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '南101', 'building': ''}, 'title': '演算法', 'instructors': ['張道行']}, {'date': {'weekday': 'W', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': '南101', 'building': ''}, 'title': '演算法', 'instructors': ['張道行']}, {'date': {'weekday': 'W', 'end_time': '20:15', 'start_time': '19:25', 'section': '第 12 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['Awei'], 'title': '實用網路安全技術'}, {'date': {'weekday': 'W', 'end_time': '21:00', 'start_time': '20:20', 'section': '第 13 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['Awei'], 'title': '實用網路安全技術'}, {'date': {'weekday': 'W', 'end_time': '21:15', 'start_time': '22:05', 'section': '第 14 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['Awei'], 'title': '實用網路安全技術'}], 'Friday': [{'date': {'weekday': 'F', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '作業系統', 'instructors': ['王志強']}, {'date': {'weekday': 'F', 'end_time': '11:00', 'start_time': '10:10', 'section': '第 3 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '作業系統', 'instructors': ['王志強']}, {'date': {'weekday': 'F', 'end_time': '12:00', 'start_time': '11:10', 'section': '第 4 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '作業系統', 'instructors': ['王志強']}, {'date': {'weekday': 'F', 'end_time': '', 'start_time': '', 'section': 'B'}, 'location': {'room': '資201', 'building': ''}, 'instructors': ['John Thunder'], 'title': '黑客技巧'}, {'date': {'weekday': 'F', 'end_time': '19:20', 'start_time': '18:30', 'section': '第 11 節'}, 'location': {'room': '資201', 'building': ''}, 'instructors': ['John Thunder'], 'title': '黑客技巧'}, {'date': {'weekday': 'F', 'end_time': '20:15', 'start_time': '19:25', 'section': '第 12 節'}, 'location': {'room': '資201', 'building': ''}, 'instructors': ['John Thunder'], 'title': '黑客技巧'}]},
        "all": {'Monday': [{'date': {'weekday': 'M', 'end_time': '09:00', 'start_time': '08:10', 'section': '第 1 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '核心通識(五)-民主與法治', 'instructors': ['林良志']}, {'date': {'weekday': 'M', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '核心通識(五)-民主與法治', 'instructors': ['林良志']}, {'date': {'weekday': 'M', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '資料壓縮', 'instructors': ['鐘文鈺']}, {'date': {'weekday': 'M', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '資料壓縮', 'instructors': ['鐘文鈺']}, {'date': {'weekday': 'M', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '資料壓縮', 'instructors': ['鐘文鈺']}], 'Sunday': [{'date': {'weekday': 'H', 'end_time': '21:15', 'start_time': '22:05', 'section': '第 14 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['Awei'], 'title': '實用網路安全技術'}, {'date': {'weekday': 'H', 'end_time': '21:15', 'start_time': '22:05', 'section': '第 14 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['Awei'], 'title': '實用網路安全技術'}, {'date': {'weekday': 'H', 'end_time': '11:00', 'start_time': '10:10', 'section': '第 3 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['RegisterAutumn'], 'title': '5倍紅寶石'}, {'date': {'weekday': 'H', 'end_time': '12:00', 'start_time': '11:10', 'section': '第 4 節'}, 'location': {'room': 'HS202', 'building': ''}, 'instructors': ['RegisterAutumn'], 'title': '5倍紅寶石'}], 'Thursday': [{'date': {'weekday': 'R', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '資料庫', 'instructors': ['楊孟翰']}, {'date': {'weekday': 'R', 'end_time': '11:00', 'start_time': '10:10', 'section': '第 3 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '資料庫', 'instructors': ['楊孟翰']}, {'date': {'weekday': 'R', 'end_time': '12:00', 'start_time': '11:10', 'section': '第 4 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '資料庫', 'instructors': ['楊孟翰']}, {'date': {'weekday': 'R', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': 'HS210', 'building': ''}, 'title': '延伸通識(人文)-音樂賞析', 'instructors': ['詹喆君']}, {'date': {'weekday': 'R', 'end_time': '17:20', 'start_time': '16:30', 'section': '第 8 節'}, 'location': {'room': 'HS210', 'building': ''}, 'title': '延伸通識(人文)-音樂賞析', 'instructors': ['詹喆君']}], 'Tuesday': [{'date': {'weekday': 'T', 'end_time': '09:00', 'start_time': '08:10', 'section': '第 1 節'}, 'location': {'room': '', 'building': ''}, 'title': '體育－羽球', 'instructors': ['陳忠信']}, {'date': {'weekday': 'T', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '', 'building': ''}, 'title': '體育－羽球', 'instructors': ['陳忠信']}, {'date': {'weekday': 'T', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '南108', 'building': ''}, 'title': '離散數學', 'instructors': ['林威成']}, {'date': {'weekday': 'T', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '南108', 'building': ''}, 'title': '離散數學', 'instructors': ['林威成']}, {'date': {'weekday': 'T', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': '南108', 'building': ''}, 'title': '離散數學', 'instructors': ['林威成']}], 'Wednesday': [{'date': {'weekday': 'W', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '南101', 'building': ''}, 'title': '演算法', 'instructors': ['張道行']}, {'date': {'weekday': 'W', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '南101', 'building': ''}, 'title': '演算法', 'instructors': ['張道行']}, {'date': {'weekday': 'W', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': '南101', 'building': ''}, 'title': '演算法', 'instructors': ['張道行']}, {'date': {'weekday': 'W', 'end_time': '20:15', 'start_time': '19:25', 'section': '第 12 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['Awei'], 'title': '實用網路安全技術'}, {'date': {'weekday': 'W', 'end_time': '21:00', 'start_time': '20:20', 'section': '第 13 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['Awei'], 'title': '實用網路安全技術'}, {'date': {'weekday': 'W', 'end_time': '21:15', 'start_time': '22:05', 'section': '第 14 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['Awei'], 'title': '實用網路安全技術'}], 'Friday': [{'date': {'weekday': 'F', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '作業系統', 'instructors': ['王志強']}, {'date': {'weekday': 'F', 'end_time': '11:00', 'start_time': '10:10', 'section': '第 3 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '作業系統', 'instructors': ['王志強']}, {'date': {'weekday': 'F', 'end_time': '12:00', 'start_time': '11:10', 'section': '第 4 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '作業系統', 'instructors': ['王志強']}, {'date': {'weekday': 'F', 'end_time': '', 'start_time': '', 'section': 'B'}, 'location': {'room': '資201', 'building': ''}, 'instructors': ['John Thunder'], 'title': '黑客技巧'}, {'date': {'weekday': 'F', 'end_time': '19:20', 'start_time': '18:30', 'section': '第 11 節'}, 'location': {'room': '資201', 'building': ''}, 'instructors': ['John Thunder'], 'title': '黑客技巧'}, {'date': {'weekday': 'F', 'end_time': '20:15', 'start_time': '19:25', 'section': '第 12 節'}, 'location': {'room': '資201', 'building': ''}, 'instructors': ['John Thunder'], 'title': '黑客技巧'}]},
        "multiinstructors": {'Monday': [{'date': {'weekday': 'M', 'end_time': '09:00', 'start_time': '08:10', 'section': '第 1 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '核心通識(五)-民主與法治', 'instructors': ['林良志']}, {'date': {'weekday': 'M', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '核心通識(五)-民主與法治', 'instructors': ['林良志']}, {'date': {'weekday': 'M', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '資料壓縮', 'instructors': ['鐘文鈺']}, {'date': {'weekday': 'M', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '資料壓縮', 'instructors': ['鐘文鈺']}, {'date': {'weekday': 'M', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '資料壓縮', 'instructors': ['鐘文鈺']}], 'Sunday': [{'date': {'weekday': 'H', 'end_time': '21:15', 'start_time': '22:05', 'section': '第 14 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['Awei'], 'title': '實用網路安全技術'}, {'date': {'weekday': 'H', 'end_time': '21:15', 'start_time': '22:05', 'section': '第 14 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['Awei'], 'title': '實用網路安全技術'}, {'date': {'weekday': 'H', 'end_time': '11:00', 'start_time': '10:10', 'section': '第 3 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['RegisterAutumn'], 'title': '5倍紅寶石'}, {'date': {'weekday': 'H', 'end_time': '12:00', 'start_time': '11:10', 'section': '第 4 節'}, 'location': {'room': 'HS202', 'building': ''}, 'instructors': ['RegisterAutumn'], 'title': '5倍紅寶石'}, {'date': {'weekday': 'H', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': 'HS202', 'building': ''}, 'instructors': ['RegisterAutumn', '紅寶石', '藍寶石'], 'title': '5倍紅寶石'}], 'Thursday': [{'date': {'weekday': 'R', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '資料庫', 'instructors': ['楊孟翰']}, {'date': {'weekday': 'R', 'end_time': '11:00', 'start_time': '10:10', 'section': '第 3 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '資料庫', 'instructors': ['楊孟翰']}, {'date': {'weekday': 'R', 'end_time': '12:00', 'start_time': '11:10', 'section': '第 4 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '資料庫', 'instructors': ['楊孟翰']}, {'date': {'weekday': 'R', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': 'HS210', 'building': ''}, 'title': '延伸通識(人文)-音樂賞析', 'instructors': ['詹喆君']}, {'date': {'weekday': 'R', 'end_time': '17:20', 'start_time': '16:30', 'section': '第 8 節'}, 'location': {'room': 'HS210', 'building': ''}, 'title': '延伸通識(人文)-音樂賞析', 'instructors': ['詹喆君']}], 'Tuesday': [{'date': {'weekday': 'T', 'end_time': '09:00', 'start_time': '08:10', 'section': '第 1 節'}, 'location': {'room': '', 'building': ''}, 'title': '體育－羽球', 'instructors': ['陳忠信']}, {'date': {'weekday': 'T', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '', 'building': ''}, 'title': '體育－羽球', 'instructors': ['陳忠信']}, {'date': {'weekday': 'T', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '南108', 'building': ''}, 'title': '離散數學', 'instructors': ['林威成']}, {'date': {'weekday': 'T', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '南108', 'building': ''}, 'title': '離散數學', 'instructors': ['林威成']}, {'date': {'weekday': 'T', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': '南108', 'building': ''}, 'title': '離散數學', 'instructors': ['林威成']}], 'Wednesday': [{'date': {'weekday': 'W', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '南101', 'building': ''}, 'title': '演算法', 'instructors': ['張道行']}, {'date': {'weekday': 'W', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '南101', 'building': ''}, 'title': '演算法', 'instructors': ['張道行']}, {'date': {'weekday': 'W', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': '南101', 'building': ''}, 'title': '演算法', 'instructors': ['張道行']}, {'date': {'weekday': 'W', 'end_time': '20:15', 'start_time': '19:25', 'section': '第 12 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['Awei'], 'title': '實用網路安全技術'}, {'date': {'weekday': 'W', 'end_time': '21:00', 'start_time': '20:20', 'section': '第 13 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['Awei'], 'title': '實用網路安全技術'}, {'date': {'weekday': 'W', 'end_time': '21:15', 'start_time': '22:05', 'section': '第 14 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['Awei'], 'title': '實用網路安全技術'}], 'Friday': [{'date': {'weekday': 'F', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '作業系統', 'instructors': ['王志強']}, {'date': {'weekday': 'F', 'end_time': '11:00', 'start_time': '10:10', 'section': '第 3 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '作業系統', 'instructors': ['王志強']}, {'date': {'weekday': 'F', 'end_time': '12:00', 'start_time': '11:10', 'section': '第 4 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '作業系統', 'instructors': ['王志強']}, {'date': {'weekday': 'F', 'end_time': '', 'start_time': '', 'section': 'B'}, 'location': {'room': '資201', 'building': ''}, 'instructors': ['John Thunder'], 'title': '黑客技巧'}, {'date': {'weekday': 'F', 'end_time': '19:20', 'start_time': '18:30', 'section': '第 11 節'}, 'location': {'room': '資201', 'building': ''}, 'instructors': ['John Thunder'], 'title': '黑客技巧'}, {'date': {'weekday': 'F', 'end_time': '20:15', 'start_time': '19:25', 'section': '第 12 節'}, 'location': {'room': '資201', 'building': ''}, 'instructors': ['John Thunder'], 'title': '黑客技巧'}]},
        "wtf": {'Monday': [{'date': {'weekday': 'M', 'end_time': '09:00', 'start_time': '08:10', 'section': '第 1 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '核心通識(五)-民主與法治', 'instructors': ['林良志']}, {'date': {'weekday': 'M', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '核心通識(五)-民主與法治', 'instructors': ['林良志']}, {'date': {'weekday': 'M', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '資料壓縮', 'instructors': ['鐘文鈺']}, {'date': {'weekday': 'M', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '資料壓縮', 'instructors': ['鐘文鈺']}, {'date': {'weekday': 'M', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': '育302', 'building': ''}, 'title': '資料壓縮', 'instructors': ['鐘文鈺']}], 'Sunday': [{'date': {'weekday': 'T', 'end_time': '09:00', 'start_time': '08:10', 'section': '第 1 節'}, 'location': {'room': '', 'building': ''}, 'title': '體育－羽球', 'instructors': ['陳忠信']}, {'date': {'weekday': 'T', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '', 'building': ''}, 'title': '體育－羽球', 'instructors': ['陳忠信']}, {'date': {'weekday': 'T', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '南108', 'building': ''}, 'weekday': 'F', 'title': '離散數學', 'instructors': ['林威成']}, {'date': {'weekday': 'T', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '南108', 'building': ''}, 'title': '離散數學', 'instructors': ['林威成']}, {'date': {'weekday': 'T', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': '南108', 'building': ''}, 'title': '離散數學', 'instructors': ['林威成']}], 'Thursday': [{'date': {'weekday': 'R', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '資料庫', 'instructors': ['楊孟翰']}, {'date': {'weekday': 'R', 'end_time': '11:00', 'start_time': '10:10', 'section': '第 3 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '資料庫', 'instructors': ['楊孟翰']}, {'date': {'weekday': 'R', 'end_time': '12:00', 'start_time': '11:10', 'section': '第 4 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '資料庫', 'instructors': ['楊孟翰']}, {'date': {'weekday': 'R', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': 'HS210', 'building': ''}, 'title': '延伸通識(人文)-音樂賞析', 'instructors': ['詹喆君']}, {'date': {'weekday': 'R', 'end_time': '17:20', 'start_time': '16:30', 'section': '第 8 節'}, 'location': {'room': 'HS210', 'building': ''}, 'title': '延伸通識(人文)-音樂賞析', 'instructors': ['詹喆君']}], 'Tuesday': [{'date': {'weekday': 'H', 'end_time': '21:15', 'start_time': '22:05', 'section': '第 14 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['Awei'], 'title': '實用網路安全技術'}, {'date': {'weekday': 'H', 'end_time': '21:15', 'start_time': '22:05', 'section': '第 14 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['Awei'], 'title': '實用網路安全技術'}, {'date': {'weekday': 'H', 'end_time': '11:00', 'start_time': '10:10', 'section': '第 3 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['RegisterAutumn'], 'title': '5倍紅寶石'}, {'date': {'weekday': 'H', 'end_time': '12:00', 'start_time': '11:10', 'section': '第 4 節'}, 'location': {'room': 'HS202', 'building': ''}, 'instructors': ['RegisterAutumn'], 'title': '5倍紅寶石'}, {'date': {'weekday': 'H', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': 'HS202', 'building': ''}, 'instructors': ['RegisterAutumn', '紅寶石', '藍寶石'], 'title': '5倍紅寶石'}], 'Wednesday': [{'date': {'weekday': 'W', 'end_time': '14:20', 'start_time': '13:30', 'section': '第 5 節'}, 'location': {'room': '南101', 'building': ''}, 'title': '演算法', 'instructors': ['張道行']}, {'date': {'weekday': 'W', 'end_time': '15:20', 'start_time': '14:30', 'section': '第 6 節'}, 'location': {'room': '南101', 'building': ''}, 'title': '演算法', 'instructors': ['張道行']}, {'date': {'weekday': 'W', 'end_time': '16:20', 'start_time': '15:30', 'section': '第 7 節'}, 'location': {'room': '南101', 'building': ''}, 'title': '演算法', 'instructors': ['張道行']}, {'date': {'weekday': 'W', 'end_time': '20:15', 'start_time': '19:25', 'section': '第 12 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['Awei'], 'title': '實用網路安全技術'}, {'date': {'weekday': 'W', 'end_time': '21:00', 'start_time': '20:20', 'section': '第 13 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['Awei'], 'title': '實用網路安全技術'}, {'date': {'weekday': 'W', 'end_time': '21:15', 'start_time': '22:05', 'section': '第 14 節'}, 'location': {'room': '資202', 'building': ''}, 'instructors': ['Awei'], 'title': '實用網路安全技術'}], 'Friday': [{'date': {'weekday': 'F', 'end_time': '10:00', 'start_time': '09:10', 'section': '第 2 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '作業系統', 'instructors': ['王志強']}, {'date': {'weekday': 'F', 'end_time': '11:00', 'start_time': '10:10', 'section': '第 3 節'}, 'location': {'room': '資201', 'building': ''}, 'title': '作業系統', 'instructors': ['王志強']}, {'location': {'room': '資201', 'building': ''}, 'campus': 'Yanchao', 'building': '資', 'room': '201', 'date': {'weekday': 'F', 'end_time': '12:00', 'start_time': '11:10', 'section': '第 4 節'}, 'instructors': ['王志強'], 'title': '作業系統'}, {'date': {'weekday': 'F', 'end_time': '', 'start_time': '', 'section': 'B'}, 'location': {'room': '資201', 'building': ''}, 'instructors': ['John Thunder'], 'title': '黑客技巧'}, {'date': {'weekday': 'F', 'end_time': '19:20', 'start_time': '18:30', 'section': '第 11 節'}, 'location': {'room': '資201', 'building': ''}, 'instructors': ['John Thunder'], 'title': '黑客技巧'}, {'date': {'weekday': 'F', 'end_time': '20:15', 'start_time': '19:25', 'section': '第 12 節'}, 'location': {'room': '資201', 'building': ''}, 'instructors': ['John Thunder'], 'title': '黑客技巧'}]},
    }

    return jsonify(sample_data[request.path[request.path.rfind("/") + 1:]])


@route('/ap/semester')
def ap_semester():
    """Get user's information.

    :reqheader Authorization: Using Basic Auth
    :resjson string value: Every semester value. format: (year,semester)
    :resjson string text: Every semester description text.
    :resjson int selected: If the value is 1, means the semester is default value on KUAS AP Website.
    :statuscode 200: Query successful
    :statuscode 401: Login failed or auth_token has been expired

    **Request**

    .. sourcecode:: http

        GET /latest/ap/users/info HTTP/1.1
        Host: kuas.grd.idv.tw:14769
        Authorization: Basic xxxxxxxxxxxxx=

    .. sourcecode:: shell

        curl -X GET -u username:password https://kuas.grd.idv.tw:14769/latest/ap/semester


    **Response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Content-Type: text/html; charset=utf-8

        {
          "default":{
            "value":"106,1",
            "text":"106學年度第1學期",
            "selected":1
          },
          "semester":[
            {
              "value":"106,1",
              "text":"106學年度第1學期",
              "selected":1
            },
            {
              "value":"105,1",
              "text":"105學年度第1學期",
              "selected":0
            },
            {
              "value":"105,2",
              "text":"105學年度第2學期",
              "selected":0
            },
            {
              "value":"105,4",
              "text":"105學年度暑修",
              "selected":0
            },
            {
              "value":"104,1",
              "text":"104學年度第1學期",
              "selected":0
            },
            {
              "value":"104,2",
              "text":"104學年度第2學期",
              "selected":0
            },
            {
              "value":"104,3",
              "text":"104學年度寒修",
              "selected":0
            },
            {
              "value":"104,4",
              "text":"104學年度暑修",
              "selected":0
            },
            {
              "value":"103,1",
              "text":"103學年度第1學期",
              "selected":0
            },
            {
              "value":"103,2",
              "text":"103學年度第2學期",
              "selected":0
            },
            {
              "value":"103,4",
              "text":"103學年度暑修",
              "selected":0
            },
            {
              "value":"103,5",
              "text":"103學年度先修學期",
              "selected":0
            },
            {
              "value":"102,1",
              "text":"102學年度第1學期",
              "selected":0
            },
            {
              "value":"102,2",
              "text":"102學年度第2學期",
              "selected":0
            },
            {
              "value":"102,4",
              "text":"102學年度暑修",
              "selected":0
            },
            {
              "value":"101,1",
              "text":"101學年度第1學期",
              "selected":0
            },
            {
              "value":"101,2",
              "text":"101學年度第2學期",
              "selected":0
            },
            {
              "value":"101,3",
              "text":"101學年度寒修",
              "selected":0
            },
            {
              "value":"101,4",
              "text":"101學年度暑修",
              "selected":0
            },
            {
              "value":"100,1",
              "text":"100學年度第1學期",
              "selected":0
            },
            {
              "value":"100,2",
              "text":"100學年度第2學期",
              "selected":0
            },
            {
              "value":"100,3",
              "text":"100學年度寒修",
              "selected":0
            },
            {
              "value":"100,4",
              "text":"100學年度暑修",
              "selected":0
            },
            {
              "value":"99,1",
              "text":"99學年度第1學期",
              "selected":0
            },
            {
              "value":"99,2",
              "text":"99學年度第2學期",
              "selected":0
            },
            {
              "value":"99,3",
              "text":"99學年度寒修",
              "selected":0
            },
            {
              "value":"99,4",
              "text":"99學年度暑修",
              "selected":0
            },
            {
              "value":"98,1",
              "text":"98學年度第1學期",
              "selected":0
            },
            {
              "value":"98,2",
              "text":"98學年度第2學期",
              "selected":0
            },
            {
              "value":"98,3",
              "text":"98學年度寒修",
              "selected":0
            },
            {
              "value":"98,4",
              "text":"98學年度暑修",
              "selected":0
            },
            {
              "value":"97,1",
              "text":"97學年度第1學期",
              "selected":0
            },
            {
              "value":"97,2",
              "text":"97學年度第2學期",
              "selected":0
            },
            {
              "value":"97,3",
              "text":"97學年度寒修",
              "selected":0
            },
            {
              "value":"97,4",
              "text":"97學年度暑修",
              "selected":0
            },
            {
              "value":"96,1",
              "text":"96學年度第1學期",
              "selected":0
            },
            {
              "value":"96,2",
              "text":"96學年度第2學期",
              "selected":0
            },
            {
              "value":"96,3",
              "text":"96學年度寒修",
              "selected":0
            },
            {
              "value":"96,4",
              "text":"96學年度暑修",
              "selected":0
            },
            {
              "value":"95,1",
              "text":"95學年度第1學期",
              "selected":0
            },
            {
              "value":"95,2",
              "text":"95學年度第2學期",
              "selected":0
            },
            {
              "value":"94,1",
              "text":"94學年度第1學期",
              "selected":0
            },
            {
              "value":"94,2",
              "text":"94學年度第2學期",
              "selected":0
            },
            {
              "value":"93,1",
              "text":"93學年度第1學期",
              "selected":0
            },
            {
              "value":"93,2",
              "text":"93學年度第2學期",
              "selected":0
            },
            {
              "value":"92,2",
              "text":"92學年度第2學期",
              "selected":0
            }
          ]
        }
    """
    semester_list = ap.get_semester_list()
    default_yms = list(
        filter(lambda x: x['selected'] == 1, semester_list))[0]

    # Check default args
    if request.args.get("default") == "1":
        return jsonify(default=default_yms)

    # Check limit args
    limit = request.args.get("limit")
    if limit:
        try:
            semester_list = semester_list[: int(limit)]
        except ValueError:
            return error.error_handle(
                status=400,
                developer_message="Error value for limit.",
                user_message="You type a wrong value for limit.")

    return jsonify(
        semester=semester_list,
        default=default_yms
    )


@route('/ap/queries/semester')
@auth.login_required
def query_post():
    fncid = request.form['fncid']
    arg01 = request.form['arg01'] if 'arg01' in request.form else None
    arg02 = request.form['arg02'] if 'arg02' in request.form else None
    arg03 = request.form['arg03'] if 'arg03' in request.form else None
    arg04 = request.form['arg04'] if 'arg04' in request.form else None

    # Restore cookies
    s = stateless_auth.get_requests_session_with_cookies()

    query_content = cache.ap_query(
        s, fncid, {"arg01": arg01, "arg02": arg02,
                   "arg03": arg03, "arg04": arg04}, g.username)

    if fncid == "ag222":
        return json.dumps(query_content)
    elif fncid == "ag008":
        return json.dumps(query_content)
    else:
        return json.dumps(query_content)
