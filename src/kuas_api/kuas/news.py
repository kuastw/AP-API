# -*- coding: utf-8 -*-

import random

ENABLE = 1
NEWS_ID = 31
NEWS_DEBUG = False

DEFAULT_WEIGHT = 10


def random_by_weight(p):
    choice_id = []
    for i in range(len(p)):
        choice_id += [i for _ in range(DEFAULT_WEIGHT + p[i]["news_weight"])]

    return p[random.choice(choice_id)]


def random_news():
    news_list = [
        {
            "news_title": "iRunner高應大路跑",
            "news_image": "http://i.imgur.com/Wdwa1W0.jpg",
            "news_url": "https://www.facebook.com/KUASiRunner",
            "news_content": "",
            "news_weight": 0
        },
        {
            "news_title": "104級排球社期初社員大會",
            "news_image": "http://i.imgur.com/Kjl1iZe.jpg",
            "news_url": "https://www.facebook.com/events/970003029729702/970003066396365/",
            "news_content": "",
            "news_weight": 0
        },
        {
            "news_title": "學生會實習幹部甄選 同雁翱翔",
            "news_image": "http://i.imgur.com/G2hbmrL.jpg",
            "news_url": "https://docs.google.com/forms/d/1Q45XyafbKGSavFUn_R_uQpV918V5uanqw7ggOmp7p2c/viewform?c=0&w=1",
            "news_content": "",
            "news_weight": 5
        },
        {
            "news_title": "第八屆志工營-王者之劍",
            "news_image": "http://i.imgur.com/Bp6JFCh.jpg",
            "news_url": "https://www.facebook.com/KUAS.Soc",
            "news_content": "",
            "news_weight": 5
        },
        {
            "news_title": "韻箏社  期初社員大會",
            "news_image": "http://i.imgur.com/6OblQiR.jpg",
            "news_url": "https://www.facebook.com/kuaszither",
            "news_content": "",
            "news_weight": 5
        },
    ]

    if NEWS_DEBUG:
        return news_list[0]
    else:
        return random_by_weight(news_list)


def news_status():
    return [ENABLE, NEWS_ID]


def news():
    """
    News for kuas.

    return [enable, news_id, news_title, news_template, news_url]
        enable: bool
        news_id: int
        news_title: string
        news_tempalte: string
        news_url: string
    """

    # Get news from random news
    news = random_news()

    news_title = news["news_title"]
    news_template = (
            "<div style='text-align:center;'>"
            "<div><img style='display:block;margin-left:auto;margin-right:auto;max-width:80%;min-height:150px;height:auto;' src='"
            + news["news_image"] + "'></img>" + news["news_content"] + "</div>" +
            "</div>"

        )
    news_url = news["news_url"]

    return [ENABLE, NEWS_ID, news_title, news_template, news_url]
