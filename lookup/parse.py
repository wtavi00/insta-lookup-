def clean_profile_data(raw_data):
    """Normalize and clean profile dictionary."""
    if not raw_data:
        return {}
    
    # Example cleanup
    return {
        "username": raw_data.get("username"),
        "full_name": raw_data.get("full_name"),
        "followers": raw_data.get("followers", 0),
        "following": raw_data.get("following", 0),
        "posts": raw_data.get("posts", 0),
        "email": raw_data.get("email", None)
    }
