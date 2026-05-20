import subprocess


class TestMain:
    def test_cli_basic(self):
        result = subprocess.run(
            ["python", "main.py", "most_active_cookie_for_date", "tests/log_file_fixtures/simple_case.csv", "-d", "2018-12-09"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "AtY0laUfhglK31C7" in result.stdout

    def test_cli_invalid_date(self):
        result = subprocess.run(
            ["python", "main.py", "most_active_cookie_for_date", "tests/log_file_fixtures/simple_case.csv", "-d", "not-a-date"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1

    def test_cli_missing_file(self):
        result = subprocess.run(
            ["python", "main.py", "most_active_cookie_for_date", "nonexistent.csv", "-d", "2018-12-09"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1

    def test_cli_sort_date(self):
        result = subprocess.run(
            ["python", "main.py", "most_active_cookie_for_date", "tests/log_file_fixtures/simple_case.csv",
             "-d", "2018-12-09", "-s", "2"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        lines = result.stdout.strip().splitlines()
        assert len(lines) == 2
        assert lines[0] == "AtY0laUfhglK31C7"

    def test_cli_sort_range(self):
        result = subprocess.run(
            ["python", "main.py", "most_active_cookie_for_range", "tests/log_file_fixtures/range_tie.csv",
             "--start_date", "2018-11-01", "--end_date", "2018-11-03", "-s", "1"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        lines = result.stdout.strip().splitlines()
        assert len(lines) == 1
        assert lines[0] == "cookieC"

    def test_cli_sort_invalid(self):
        result = subprocess.run(
            ["python", "main.py", "most_active_cookie_for_date", "tests/log_file_fixtures/simple_case.csv",
             "-d", "2018-12-09", "-s", "notanint"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1

    def test_cli_invalid_method(self):
        result = subprocess.run(
            ["python", "main.py", "not_a_method", "tests/log_file_fixtures/simple_case.csv"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1

    def test_cli_date_method_missing_d_flag(self):
        result = subprocess.run(
            ["python", "main.py", "most_active_cookie_for_date", "tests/log_file_fixtures/simple_case.csv"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1

    def test_cli_range_method_missing_date_flags(self):
        result = subprocess.run(
            ["python", "main.py", "most_active_cookie_for_range", "tests/log_file_fixtures/simple_case.csv"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 1

    def test_cli_range_basic(self):
        result = subprocess.run(
            ["python", "main.py", "most_active_cookie_for_range", "tests/log_file_fixtures/simple_case.csv",
             "--start_date", "2018-12-08", "--end_date", "2018-12-09"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "AtY0laUfhglK31C7" in result.stdout
