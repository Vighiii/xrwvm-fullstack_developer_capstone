import requests
import os
from dotenv import load_dotenv

load_dotenv()

# تم تثبيت الرابط المحلي هنا مباشرة لضمان الاتصال السريع وتخطي مشاكل
# البروكسي الخارجي
backend_url = "http://localhost:3030"
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url', default="http://localhost:5000/")


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params = params + key + "=" + str(value) + "&"
        # نضع علامة الاستفهام فقط في حال وجود متغيرات فعلية مرسلة
        request_url = backend_url + endpoint + "?" + params.rstrip('&')
    else:
        # إذا لم تكن هناك وسائط، نرسل الرابط نظيفاً تماماً بدون علامات زائدة
        request_url = backend_url + endpoint

    print("GET from {} ".format(request_url))
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Network exception occurred: {err}")


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as err:
        print(f"Network exception occurred: {err}")
