from datetime import datetime, date
from src.cookie import Cookie
from csv import DictReader

class CookieLog:
    def __init__(self, log_file_path: str):
        self._cookie_registry : dict[str, Cookie] = {}
        self._date_log : dict[date, list[Cookie]] = {}

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
        with open(log_file_path, 'r') as f:
            reader = DictReader(f)
            for row in reader:
                cookie_name = row['cookie']
                datetime_str = row['timestamp']
                datetime_obj = datetime.fromisoformat(datetime_str)

                if cookie_name not in self._cookie_registry:
                    self._cookie_registry[cookie_name] = Cookie(cookie_name)
                
                cookie_obj = self._cookie_registry[cookie_name]

                cookie_obj.insert_timestamps([datetime_obj])

                if datetime_obj.date() not in self._date_log:
                    self._date_log[datetime_obj.date()] = []

                if cookie_obj not in self._date_log[datetime_obj.date()]:
                    self._date_log[datetime_obj.date()].append(cookie_obj)
