import sys
from src.cookie_log import CookieLog
from datetime import date

def main():
    
    if len(sys.argv) != 4:
        print("Usage: ./most_active_cookie <log_file_path> -d <target_date>")
        sys.exit(1)
    
    log_file_path = sys.argv[1]
    target_date_str = sys.argv[3]

    try:
        target_date = date.fromisoformat(target_date_str)
    except ValueError:
        print(f"Invalid date format: {target_date_str}. Expected format: YYYY-MM-DD")
        sys.exit(1)

    cookie_log = CookieLog(log_file_path)
    
    most_active_cookies = cookie_log.most_active_cookie_for_date(target_date)

    for cookie in most_active_cookies:
        print(cookie)

if __name__ == "__main__":
    main()
