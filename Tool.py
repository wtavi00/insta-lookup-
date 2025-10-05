import argparse
import logging
from lookup import auth, fetch, parse, export

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def main():
    parser = argparse.ArgumentParser(description="Instagram Lookup Tool")
    parser.add_argument("--username", help="Instagram username")
    parser.add_argument("--id", help="Instagram user ID")
    parser.add_argument("--session", help="Session token or file path", default=None)
    parser.add_argument("--output", help="Save results to file (JSON/CSV)", default=None)
    args = parser.parse_args()

    # Auth
    session = auth.load_session(args.session)

    # Fetch
    if args.username:
        logging.info(f"Fetching profile for username: {args.username}")
        raw_data = fetch.get_profile_by_username(session, args.username)
    elif args.id:
        logging.info(f"Fetching profile for user ID: {args.id}")
        raw_data = fetch.get_profile_by_id(session, args.id)
    else:
        logging.error("Provide either --username or --id")
        return

    # Parse
    parsed = parse.clean_profile_data(raw_data)
    logging.info("Profile data fetched successfully")

    # Output
    if args.output:
        export.save_results(parsed, args.output)
        logging.info(f"Results saved to {args.output}")
    else:
        print(parsed)

if __name__ == "__main__":
    main()
