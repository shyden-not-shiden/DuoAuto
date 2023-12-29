import json
import uuid

import requests

import settings

config = settings.Config().load()

USER_EMAIL = config.USER_EMAIL
USER_PASS = config.USER_PASS

login_url = "https://android-api-cf.duolingo.com/2017-06-30/login"


def login():
    parameters = {"fields": "id"}
    headers = {
        "User-Agent": "Duodroid/5.132.4 Dalvik/2.1.0 (Linux; U; Android 13; sdk_gphone64_x86_64 Build/TE1A.220922.010)"
    }
    body = {
        "distinctId": f"{uuid.uuid4()}",
        "identifier": f"{USER_EMAIL}",
        "password": f"{USER_PASS}",
    }
    response = session.post(
        headers=headers, params=parameters, url=login_url, data=json.dumps(body)
    )
    cookies = response.cookies
    print(cookies)
    token = response.headers.get("jwt")
    print(token)
    print(f"User ID: {response.json().get('id')}")


if __name__ == "__main__":
    session = requests.Session()
    login()
