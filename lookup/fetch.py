import logging

def get_profile_by_username(session, username):
    """Stub: Replace with actual Instagram request."""
    logging.info(f"Simulating fetch for username={username}")
    # Replace with real API call
    return {
        "username": username,
        "full_name": "John Doe",
        "followers": 1234,
        "following": 500,
        "posts": 50,
        "email": "john***@gmail.com"
    }

def get_profile_by_id(session, user_id):
    """Stub: Replace with actual Instagram request."""
    logging.info(f"Simulating fetch for user_id={user_id}")
    return {
        "id": user_id,
        "username": "example_user",
        "full_name": "Jane Smith",
        "followers": 2048,
        "following": 320,
        "posts": 75,
        "email": "jane***@outlook.com"
    }

