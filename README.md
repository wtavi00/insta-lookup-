# 📸 Instagram User Info Lookup Tool

This Python tool lets you fetch **detailed profile information** from Instagram using a valid session ID.  
It supports both **single-user** and **batch lookups**, and provides **public and obfuscated contact info** when available.

---

## ⚠️ Disclaimer

> This tool uses **Instagram's private APIs**, which are undocumented and may violate [Instagram’s Terms of Use](https://help.instagram.com/581066165581870). Use at your own risk. Your account may be **rate-limited**, **restricted**, or **banned**.

---
---

### 2. Code Structure
Right now your repo might be just one or two Python files.  

insta-lookup-/
│── insta_lookup.py # CLI entry point
│── lookup/
│ ├── init.py
│ ├── auth.py # session handling
│ ├── fetch.py # core API requests
│ ├── parse.py # parsing/cleaning output
│ └── export.py # save to JSON/CSV
│── requirements.txt
│── README.md


---

## 🚀 Features

- Lookup by **username** or **user ID**
- Batch mode: Read from a file of usernames/IDs
- Fetch public profile stats: followers, bio, posts, links, etc.
- Extract public **email** / **phone number**
- Add support for profile pictures download
- Handle private accounts gracefully
- Obfuscated **email/phone** from advanced recovery endpoint
- Displays **profile picture URL**
- Provide a GUI frontend
- JSON export

---


## 🔑 Getting Your Session ID
Log in to Instagram on your desktop browser.
Open Developer Tools → Application → Cookies.
Copy the value of the sessionid cookie.

## 🧪 Usage
### ▶️ Single User Lookup
```bash
python insta_user_lookup.py -s YOUR_SESSION_ID -u instagram
```
or by userID:
```bash
python insta_user_lookup.py -s YOUR_SESSION_ID -i 1234567890
```

### 📁 Batch Mode (Multiple Users)
Create a file usernames.txt.
Then run
Save to JSON

## ⚡ Usage
### By username:
```bash
python insta_lookup.py --username example_user
```

### By user ID:
```bash
python insta_lookup.py --id 123456789
```

### Save results:
```bash
python insta_lookup.py --username example_user --output results.json
```


## 🖥 Output Example
```bash
Username               : natgeo
User ID                : 787132
Full Name              : National Geographic
Verified               : True | Business Account: True
Private Account        : False
Followers              : 287000000
Following              : 134
Posts                  : 30000
External URL           : https://natgeo.com
Biography              : Taking our understanding of the world further...
Public Email           : contact@natgeo.com
Obfuscated Phone       : +* *** ***90
Profile Picture        : https://instagram.natgo.net/...
```
## 🛡 Notes
Avoid sending too many requests too fast - you might get rate limited.
The tool includes a small delay (1.5s) between users in batch mode to be safe.
Some users may not have public info (private/business accounts).
Obfuscated data is not always available; it depends on the user.


