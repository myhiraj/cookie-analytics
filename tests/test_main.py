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
