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


def advanced_lookup(username):
    body = "signed_body=SIGNATURE." + quote_plus(
        dumps({"q": username, "skip_recovery": "1"}, separators=(",", ":"))
    )
    headers = {
        "Accept-Language": "en-US",
        "User-Agent": "Instagram 101.0.0.15.120",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-IG-App-ID": "124024574287414",
        "Accept-Encoding": "gzip, deflate",
        "Host": "i.instagram.com",
        "Connection": "keep-alive",
        "Content-Length": str(len(body))
    }
    try:
        response = requests.post(
            'https://i.instagram.com/api/v1/users/lookup/',
            headers=headers,
            data=body
        )
        return {"user": response.json(), "error": None}
    except decoder.JSONDecodeError:
        return {"user": None, "error": "Rate limit on lookup"}


def enrich_phone(number, country_code):
    try:
        full_number = f"+{country_code}{number}"
        parsed = phonenumbers.parse(full_number)
        country = pycountry.countries.get(alpha_2=region_code_for_country_code(parsed.country_code))
        return f"{full_number} ({country.name})" if country else full_number
    except Exception:
        return f"+{country_code}{number} (Unknown)"


def print_info(info, extra_info=None):
    print("\n" + "-" * 40)
    print(f"Username               : {info.get('username', 'N/A')}")
    print(f"User ID                : {info.get('userID')}")
    print(f"Full Name              : {info.get('full_name', 'N/A')}")
    print(f"Verified               : {info.get('is_verified')} | Business Account: {info.get('is_business')}")
    print(f"Private Account        : {info.get('is_private')}")
    print(f"Followers              : {info.get('follower_count')}")
    print(f"Following              : {info.get('following_count')}")
    print(f"Posts                  : {info.get('media_count')}")
    print(f"IGTV Posts             : {info.get('total_igtv_videos')}")
    print(f"Biography              :\n  {'  '.join(info.get('biography', '').splitlines())}")
    print(f"External URL           : {info.get('external_url', 'None')}")
    print(f"Linked WhatsApp        : {info.get('is_whatsapp_linked')}")
    print(f"Memorial Account       : {info.get('is_memorialized')}")
    print(f"New to Instagram       : {info.get('is_new_to_instagram')}")

    if info.get("public_email"):
        print(f"Public Email           : {info['public_email']}")
    if info.get("public_phone_number"):
        enriched = enrich_phone(info['public_phone_number'], info['public_phone_country_code'])
        print(f"Public Phone           : {enriched}")
    if 'hd_profile_pic_url_info' in info:
        print(f"Profile Picture        : {info['hd_profile_pic_url_info'].get('url')}")

    if extra_info:
        if extra_info.get("obfuscated_email"):
            print(f"Obfuscated Email       : {extra_info['obfuscated_email']}")
        if extra_info.get("obfuscated_phone"):
            print(f"Obfuscated Phone       : {extra_info['obfuscated_phone']}")
    print("-" * 40)


def process_user(search, sessionid, search_type):
    info_result = get_info(search, sessionid, search_type)
    if info_result["error"]:
        print(f"❌ {search} - {info_result['error']}")
        return {"username": search, "error": info_result["error"]}

    user_info = info_result["user"]
    extra_lookup = advanced_lookup(user_info["username"])
    extra_data = extra_lookup["user"] if not extra_lookup["error"] else {}

    print_info(user_info, extra_data)
    return user_info



def main():
    parser = argparse.ArgumentParser(description="Instagram user info lookup tool with batch support.")
    parser.add_argument('-s', '--sessionid', required=True, help="Instagram session ID")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--username', help="Instagram username")
    group.add_argument('-i', '--id', help="Instagram user ID")
    group.add_argument('-f', '--file', help="File with usernames or IDs (one per line)")

    parser.add_argument('-o', '--output', help="Optional output file for JSON results")

    args = parser.parse_args()
    sessionid = args.sessionid

    results = []

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        for entry in lines:
            if entry.isdigit():
                search_type = "id"
            else:
                search_type = "username"
            user_data = process_user(entry, sessionid, search_type)
            results.append(user_data)
            time.sleep(1.5)  # to avoid hitting rate limits too quickly
    else:
        search_type = "id" if args.id else "username"
        search = args.id or args.username
        user_data = process_user(search, sessionid, search_type)
        results.append(user_data)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2)
            print(f"\n✅ Results saved to {args.output}")
        except IOError:
            print(f"❌ Could not write to {args.output}")


