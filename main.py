import sys
import argparse
import logging
from src.cookie_log import CookieLog
from datetime import date

def main():
    parser = argparse.ArgumentParser(description="Find the most active cookie for a given date.")
    parser.add_argument("log_file_path", help="Path to the log file")
    parser.add_argument("-d", required=True, help="Target date (YYYY-MM-DD)")
    
    args = parser.parse_args()

    try:
        target_date = date.fromisoformat(args.d.strip('" '))
    except ValueError:
        print(f"Invalid date format: {args.d}. Expected format: YYYY-MM-DD")
        sys.exit(1)

    try:
        cookie_log = CookieLog(args.log_file_path.strip('" '))
    except (FileNotFoundError, ValueError) as e:
        print(e)
        sys.exit(1)

    most_active_cookies = cookie_log.most_active_cookie_for_date(target_date)

    if not most_active_cookies:
        print(f"No cookies found for date: {target_date}")
        sys.exit(0)

    for cookie in most_active_cookies:
        print(cookie)

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    main()
