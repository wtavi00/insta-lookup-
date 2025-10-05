import logging

def load_session(session_file_or_token):
    """Load session from file or token (stub for now)."""
    if session_file_or_token is None:
        logging.warning("No session provided, using public endpoints only")
        return {}
    
    if session_file_or_token.endswith(".txt"):
        try:
            with open(session_file_or_token, "r") as f:
                token = f.read().strip()
            return {"session": token}
        except FileNotFoundError:
            logging.error("Session file not found")
            return {}
    else:
        return {"session": session_file_or_token}
