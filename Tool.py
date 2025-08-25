import argparse
import requests
from urllib.parse import quote_plus
from json import dumps, decoder
import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_country_code
import pycountry
import json
import sys
import time

def get_user_id(username, sessionid):
    headers = {"User-Agent": "iphone_ua", "x-ig-app-id": "936619743392459"}
    response = requests.get(
        f'https://i.instagram.com/api/v1/users/web_profile_info/?username={username}',
        headers=headers,
        cookies={'sessionid': sessionid}
    )
    if response.status_code == 404:
        return {"id": None, "error": "User not found"}

    try:
        user_id = response.json()["data"]['user']['id']
        return {"id": user_id, "error": None}
    except decoder.JSONDecodeError:
        return {"id": None, "error": "Rate limit or bad response"}


