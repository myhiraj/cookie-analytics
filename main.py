import sys
from src.cookie_log import CookieLog
from src.cookie import Cookie

def main():
    
    if len(sys.argv) != 3:
        print("Usage: ./most_active_cookie <log_file_path> -d <target_date>")
        return

if __name__ == "__main__":
    main()