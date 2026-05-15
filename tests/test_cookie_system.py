import pytest
import subprocess
from datetime import date
from src.cookie import Cookie
from src.cookie_log import CookieLog

class TestCookieLog:
    def test_simple_case_single_most_active_cookie(self):
        log = CookieLog('tests/log_file_fixtures/simple_case.csv')
        most_active = log.most_active_cookie_for_date(date(2018, 12, 9))
        assert most_active == ['AtY0laUfhglK31C7']
    
    def test_simple_case_multiple_most_active_cookies(self):
        log = CookieLog('tests/log_file_fixtures/simple_case.csv')
        most_active = log.most_active_cookie_for_date(date(2018, 12, 8))
        assert set(most_active) == {'SAZuXPGUrfbcn5UA', 'fbcn5UAVanZf6UtG'}

    def test_empty_file_raises(self):
        with pytest.raises(ValueError):
            CookieLog("tests/log_file_fixtures/empty_case.csv")

    def test_malformed_row_missing_data(self):
        # fixture: valid row plus rows with a missing cookie or timestamp value
        log = CookieLog("tests/log_file_fixtures/missing_values.csv")
        result = log.most_active_cookie_for_date(date(2018, 12, 9))
        assert result == ["AtY0laUfhglK31C7"]

    def test_extra_columns_still_works(self):
        # fixture: csv with extra columns beyond cookie and timestamp
        log = CookieLog("tests/log_file_fixtures/extra_columns.csv")
        result = log.most_active_cookie_for_date(date(2018, 12, 9))
        assert result == ["AtY0laUfhglK31C7"]

    def test_missing_headers_raises(self):
        with pytest.raises(ValueError):
            CookieLog("tests/log_file_fixtures/missing_headers.csv")

    def test_wrong_datetime_format_skips_row(self):
        # fixture: one valid row, one row with bad timestamp
        log = CookieLog("tests/log_file_fixtures/bad_timestamp.csv")
        result = log.most_active_cookie_for_date(date(2018, 12, 9))
        assert result == ["AtY0laUfhglK31C7"]  # only valid row counted

    def test_no_cookies_for_date(self):
        log = CookieLog("tests/log_file_fixtures/simple_case.csv")
        result = log.most_active_cookie_for_date(date(2018, 12, 1))
        assert result == []
    
    def test_header_only_file(self):
        log = CookieLog("tests/log_file_fixtures/header_only.csv")
        result = log.most_active_cookie_for_date(date(2018, 12, 9))
        assert result == []


class TestCookie:
    def test_same_cookie_object_across_dates(self):
        # Verifies that _cookie_registry and _date_log reference the same object,
        # not separate Cookie instances with the same name
        log = CookieLog("tests/log_file_fixtures/simple_case.csv")

        cookie_from_registry = log._cookie_registry["AtY0laUfhglK31C7"]
        cookie_from_date_log = next(
            c for c in log._date_log[date(2018, 12, 9)]
            if c.name == "AtY0laUfhglK31C7"
        )

        assert cookie_from_registry is cookie_from_date_log
    
    def test_insert_timestamps_separates_by_date(self):
        from datetime import datetime
        cookie = Cookie("AtY0laUfhglK31C7")
        cookie.insert_timestamps([
            datetime.fromisoformat("2018-12-09T14:19:00+00:00"),
            datetime.fromisoformat("2018-12-08T10:00:00+00:00"),
        ])
        assert cookie.get_activity_frequency_by_date(date(2018, 12, 9)) == 1
        assert cookie.get_activity_frequency_by_date(date(2018, 12, 8)) == 1

    def test_empty_name_raises(self):
        with pytest.raises(ValueError):
            Cookie("")

    def test_whitespace_name_raises(self):
        with pytest.raises(ValueError):
            Cookie("   ")

class TestMain:
    def test_cli_basic(self):
        result = subprocess.run(
            ["python", "main.py", "tests/log_file_fixtures/simple_case.csv", "-d", "2018-12-09"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "AtY0laUfhglK31C7" in result.stdout

    def test_cli_invalid_date(self):
        result = subprocess.run(
            ["python", "main.py", "tests/log_file_fixtures/simple_case.csv", "-d", "not-a-date"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1

    def test_cli_missing_file(self):
        result = subprocess.run(
            ["python", "main.py", "nonexistent.csv", "-d", "2018-12-09"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1