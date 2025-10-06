from lookup import parse

def test_clean_profile_data():
    raw = {
        "username": "test_user",
        "full_name": "Test User",
        "followers": 100,
        "following": 50,
        "posts": 10,
        "email": "t***@gmail.com"
    }
    cleaned = parse.clean_profile_data(raw)
    assert cleaned["username"] == "test_user"
    assert cleaned["followers"] == 100
