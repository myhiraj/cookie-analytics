from datetime import datetime, date
import logging
from src.cookie import Cookie
from csv import DictReader

logger = logging.getLogger(__name__)

class CookieLog:
    def __init__(self, log_file_path: str):
        self._cookie_registry : dict[str, Cookie] = {}
        self._date_log : dict[date, set[Cookie]] = {}

        self._load_cookies_from_log(log_file_path)

    def most_active_cookie_for_date(self, target_date: date):
        if target_date not in self._date_log:
            return []
        
        cookies_for_date = self._date_log[target_date]
        frequency_map : dict[str, int] = {}

        for cookie in cookies_for_date:
            frequency_map[cookie.name] = cookie.get_activity_frequency_by_date(target_date)
        
        max_frequency = max(frequency_map.values())
        most_active_cookies = [cookie_name for cookie_name, freq in frequency_map.items() if freq == max_frequency]
        
        return most_active_cookies


    def _load_cookies_from_log(self, log_file_path: str):
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
