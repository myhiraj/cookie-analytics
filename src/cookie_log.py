from datetime import datetime, date
import logging
from src.cookie import Cookie
from csv import DictReader

logger = logging.getLogger(__name__)

class CookieLog:

    '''
    Parses a cookie activity log CSV and answers queries against it.

    The CSV must have at minimum two columns: 'cookie' and 'timestamp'.
    Timestamps must be ISO 8601 format (e.g. 2018-12-09T14:19:00+00:00).
    Rows with missing values or unparseable timestamps are skipped with a warning.

    Raises:
        FileNotFoundError: If the log file does not exist.
        ValueError: If the file is empty or missing required columns.
    '''

    def __init__(self, log_file_path: str):
        # primary index for lookup of cookies active on a given date
        self._date_log : dict[date, set[Cookie]] = {}  # date -> set of cookies active on that date

        # secondary index for lookup of cookies by name
        self._cookie_registry : dict[str, Cookie] = {} # string cookie name -> Cookie object

        self._load_cookies_from_log(log_file_path)


    def most_active_cookie_for_date(self, target_date: date) -> list[str]:

        '''
        Returns the name(s) of the most frequently seen cookie(s) on the given date.
        If multiple cookies share the highest frequency, all are returned.
        Returns an empty list if no cookies were seen on that date.
        '''

        if target_date not in self._date_log:
            return []
        
        cookies_for_date = self._date_log[target_date]
        frequency_map : dict[str, int] = {}

        for cookie in cookies_for_date:
            frequency_map[cookie.name] = cookie.get_activity_frequency_by_date(target_date)
        
        max_frequency = max(frequency_map.values())
        most_active_cookies = [cookie_name for cookie_name, freq in frequency_map.items() if freq == max_frequency]
        
        return most_active_cookies
    
    def most_active_cookie_for_range(self, start_date: date, end_date: date) -> list[str]:

        '''
        Returns the name(s) of the most frequently seen cookie(s) across the given date range (inclusive).
        If multiple cookies share the highest frequency, all are returned.
        Returns an empty list if no cookies were seen in that date range.
        '''

        if start_date not in self._date_log and end_date not in self._date_log:
            return []
        
        frequency_map : dict[str, int] = {}

        for date_key in self._date_log:
            if start_date <= date_key <= end_date:
                cookie = self._date_log[date_key]
                frequency_map[cookie.name] = cookie.get_activity_frequency_by_date(date_key)
        
        if not frequency_map:
            return []
        
        max_frequency = max(frequency_map.values())
        most_active_cookies = [cookie_name for cookie_name, freq in frequency_map.items() if freq == max_frequency]

        return most_active_cookies

    def _load_cookies_from_log(self, log_file_path: str):
        '''Reads and indexes the log file into _cookie_registry and _date_log.'''

        try:
            with open(log_file_path, 'r') as f:

                reader = DictReader(f)

                expected = {'cookie', 'timestamp'}

                if not reader.fieldnames:
                    raise ValueError("Log file is empty")

                if not expected.issubset(reader.fieldnames):
                    raise ValueError(f"Log file is missing required fields. Expected: {expected}")

                for row in reader:

                    cookie_name = row['cookie'].strip('" ')
                    datetime_str = row['timestamp'].strip('" ')

                    if not cookie_name or not datetime_str:
                        logger.warning(f"Skipping row with missing values: {row}")
                        continue

                    try:
                        datetime_obj = datetime.fromisoformat(datetime_str)
                    except ValueError:
                        logger.warning(f"Skipping invalid timestamp: {datetime_str}")
                        continue

                    if cookie_name not in self._cookie_registry:
                        self._cookie_registry[cookie_name] = Cookie(cookie_name)
                    
                    cookie = self._cookie_registry[cookie_name]

                    cookie.insert_timestamps([datetime_obj])

                    if datetime_obj.date() not in self._date_log:
                        self._date_log[datetime_obj.date()] = set()

                    self._date_log[datetime_obj.date()].add(cookie)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Log file not found: {log_file_path}") from e
