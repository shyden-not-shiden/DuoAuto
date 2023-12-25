import json
import os
import uuid
from uuid import UUID

import requests
import dotenv

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
        "distinctId": "36d8a06d-dd23-41fe-8bc0-11cda3fe126e",
        "identifier": f"{USER_EMAIL}",
        "password": f"{USER_PASS}",
    }
    response = requests.post(
        headers=headers, params=parameters, url=login_url, data=json.dumps(body)
    )
    print(f"User ID: {response.json().get('id')}")


if __name__ == "__main__":
    login()
