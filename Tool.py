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


def get_info(search, sessionid, search_type="username"):
    if search_type == "username":
        data = get_user_id(search, sessionid)
        if data["error"]:
            return {"user": None, "error": data["error"]}
        user_id = data["id"]
    else:
        try:
            user_id = str(int(search))
        except ValueError:
            return {"user": None, "error": "Invalid ID"}
    try:
        response = requests.get(
            f'https://i.instagram.com/api/v1/users/{user_id}/info/',
            headers={'User-Agent': 'Instagram 64.0.0.14.96'},
            cookies={'sessionid': sessionid}
        )
        if response.status_code == 429:
            return {"user": None, "error": "Rate limit exceeded"}

        response.raise_for_status()
        user_data = response.json().get("user")
        if not user_data:
            return {"user": None, "error": "User not found"}
        user_data["userID"] = user_id
        return {"user": user_data, "error": None}
    except requests.exceptions.RequestException:
        return {"user": None, "error": "Request failed"}


