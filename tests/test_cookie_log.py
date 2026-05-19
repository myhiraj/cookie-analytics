import pytest
from datetime import date
from src.cookie_log import CookieLog


class TestMostActiveDate:
    def test_simple_case_single_most_active_cookie(self):
        log = CookieLog('tests/log_file_fixtures/simple_case.csv')
        most_active = log.most_active_cookie_for_date(date(2018, 12, 9))
        assert most_active == ['AtY0laUfhglK31C7']
    
    def test_simple_case_multiple_most_active_cookies(self):
        log = CookieLog('tests/log_file_fixtures/simple_case.csv')
        most_active = log.most_active_cookie_for_date(date(2018, 12, 8))
        assert set(most_active) == {'SAZuXPGUrfbcn5UA', 'fbcn5UAVanZf6UtG'}

    def test_no_cookies_for_date(self):
        log = CookieLog("tests/log_file_fixtures/simple_case.csv")
        result = log.most_active_cookie_for_date(date(2018, 12, 1))
        assert result == []

class TestMostActiveRange:

    def test_single_winner_across_range(self):
        log = CookieLog('tests/log_file_fixtures/simple_case.csv')
        result = log.most_active_cookie_for_range(date(2018, 12, 8), date(2018, 12, 9))
        assert result == ['AtY0laUfhglK31C7']

    def test_tie_returns_all_tied_cookies(self):
        log = CookieLog('tests/log_file_fixtures/range_tie.csv')
        result = log.most_active_cookie_for_range(date(2018, 11, 1), date(2018, 11, 2))
        assert set(result) == {'cookieA', 'cookieB'}

    def test_boundaries_are_inclusive(self):
        # range_tie.csv: Nov 1 cookieA×2, Nov 2 cookieB×2, Nov 3 cookieC×3
        log = CookieLog('tests/log_file_fixtures/range_tie.csv')
        # excluding Nov 3 (end): tie — proves end boundary is included when it changes result
        assert set(log.most_active_cookie_for_range(date(2018, 11, 1), date(2018, 11, 2))) == {'cookieA', 'cookieB'}
        # including Nov 3 (end): cookieC wins — proves end boundary is included
        assert log.most_active_cookie_for_range(date(2018, 11, 1), date(2018, 11, 3)) == ['cookieC']

    def test_frequency_accumulated_across_days(self):
        # AtY0laUfhglK31C7: 1 hit Dec 8 + 3 hits Dec 9 = 4 total; others max out at 3
        log = CookieLog('tests/log_file_fixtures/simple_case.csv')
        result = log.most_active_cookie_for_range(date(2018, 12, 8), date(2018, 12, 9))
        assert result == ['AtY0laUfhglK31C7']

    def test_no_cookies_in_range(self):
        log = CookieLog('tests/log_file_fixtures/simple_case.csv')
        result = log.most_active_cookie_for_range(date(2018, 12, 1), date(2018, 12, 5))
        assert result == []


class TestCookieLogInternals:

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

    def test_wrong_datetime_format_skips_row(self):
        # fixture: one valid row, one row with bad timestamp
        log = CookieLog("tests/log_file_fixtures/bad_timestamp.csv")
        result = log.most_active_cookie_for_date(date(2018, 12, 9))
        assert result == ["AtY0laUfhglK31C7"]  # only valid row counted

    def test_empty_file_raises(self):
        with pytest.raises(ValueError):
            CookieLog("tests/log_file_fixtures/empty_case.csv")

    def test_missing_headers_raises(self):
        with pytest.raises(ValueError):
            CookieLog("tests/log_file_fixtures/missing_headers.csv")

    def test_file_not_found_raises(self):
        with pytest.raises(FileNotFoundError):
            CookieLog("nonexistent.csv")

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
