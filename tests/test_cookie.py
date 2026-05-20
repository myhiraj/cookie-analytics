import pytest
from datetime import date
from src.cookie import Cookie


class TestCookie:
    
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

    def test_get_activity_frequency_unknown_date_returns_zero(self):
        from datetime import datetime
        cookie = Cookie("AtY0laUfhglK31C7")
        cookie.insert_timestamps([datetime.fromisoformat("2018-12-09T14:19:00+00:00")])
        assert cookie.get_activity_frequency_by_date(date(2018, 12, 1)) == 0
