import sys
import argparse
import logging
from src.cookie_log import CookieLog
from datetime import date

def handle_most_active_cookie_for_date(
        args: argparse.Namespace | None = None, 
        cookie_log: CookieLog | None = None, 
        sort_top_n: int | None = None
        ):
    if not args.d:
        print("For 'most_active_cookie_for_date', both log_file_path and -d (date) arguments are required.")
        sys.exit(1)
    else:
        try:
            target_date = date.fromisoformat(args.d.strip('" '))
        except ValueError:
            print(f"Invalid date format: {args.d}. Expected format: YYYY-MM-DD")
            sys.exit(1)
    
        if args.sort:
            most_active_cookies = cookie_log.most_active_cookie_for_date(target_date, sort=sort_top_n)
            if sort_top_n == 0:
                for cookie in most_active_cookies:
                    print(cookie)
            else:
                for cookie in most_active_cookies[:abs(sort_top_n)]:
                    print(cookie)
        else:
            most_active_cookies = cookie_log.most_active_cookie_for_date(target_date)

            if not most_active_cookies:
                print(f"No cookies found for date: {target_date}")
                sys.exit(0)
            else:
                for cookie in most_active_cookies:
                    print(cookie)
                sys.exit(0)

def handle_most_active_cookie_for_range(
        args: argparse.Namespace | None = None, 
        cookie_log: CookieLog | None = None, 
        sort_top_n: int | None = None
        ):

    if not args.start_date or not args.end_date:
        print("For 'most_active_cookie_for_range', 'log_file_path', '--start_date', and '--end_date' arguments are required.")
        sys.exit(1)
    else:

        try:
            start_date = date.fromisoformat(args.start_date.strip('" '))
        except ValueError:
            print(f"Invalid date format: {args.start_date}. Expected format: YYYY-MM-DD")
            sys.exit(1)

        try:
            end_date = date.fromisoformat(args.end_date.strip('" '))
        except ValueError:
            print(f"Invalid date format: {args.end_date}. Expected format: YYYY-MM-DD")
            sys.exit(1)
        
        if start_date > end_date:
            print(f"start date cannot be after end date: {start_date} > {end_date}.")
            sys.exit(1)

        if args.sort:
            most_active_cookies = cookie_log.most_active_cookie_for_range(start_date, end_date, sort=sort_top_n)
            if sort_top_n == 0:
                for cookie in most_active_cookies:
                    print(cookie)
            else:
                for cookie in most_active_cookies[:abs(sort_top_n)]:
                    print(cookie)
        else:
            most_active_cookies = cookie_log.most_active_cookie_for_range(start_date, end_date)

            if not most_active_cookies:
                print(f"No cookies found for range: {start_date} to {end_date}")
                sys.exit(0)
            else:
                for cookie in most_active_cookies:
                    print(cookie)
                sys.exit(0)


HANDLERS = {
    "most_active_cookie_for_date": handle_most_active_cookie_for_date,
    "most_active_cookie_for_range": handle_most_active_cookie_for_range,
            }

METHODS_SUPPORTED = list(HANDLERS.keys())

def main():
    parser = argparse.ArgumentParser(description="Run analysis on cookie logs.")

    parser.add_argument("method_selection", help=f"Which analysis to run:{METHODS_SUPPORTED}")
    parser.add_argument("log_file_path", help="Path to the cookie log file (CSV format)")

    # Arguments for most_active_cookie_for_date
    parser.add_argument("-d", required=False, help="Target date (YYYY-MM-DD)")

    # Arguments for most_active_cookie_for_date_range
    parser.add_argument("-from", "--start_date", required=False, help="Start date for range (YYYY-MM-DD)")
    parser.add_argument("-to", "--end_date", required=False, help="End date for range (YYYY-MM-DD)")

    # Optional arguments for sorting top-N results
    parser.add_argument("-s", "--sort", required=False, help="Include this flag to sort results in desc order by frequency.")

    args = parser.parse_args()

    if args.method_selection not in METHODS_SUPPORTED:
        print(f"Invalid method selection: {args.method_selection}. Valid options are: {METHODS_SUPPORTED}")
        sys.exit(1)

    try:
        cookie_log = CookieLog(args.log_file_path.strip('" '))
    except (FileNotFoundError, ValueError) as e:
        print(e)
        sys.exit(1)

    try:
        sort_top_n = int(args.sort) if args.sort else None
    except ValueError as e:
        print(f"Invalid value for sort argument: {args.sort}. Must be an integer. Error: {e}")
        sys.exit(1) 

    HANDLERS[args.method_selection](args=args, cookie_log=cookie_log, sort_top_n=sort_top_n)

if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING)
    main()
