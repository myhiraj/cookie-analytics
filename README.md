# cookie-analytics

A command-line tool that parses a cookie activity log and returns the most active cookie(s) for a given date or date range.

## Usage

```bash
python main.py <method> <log_file_path> [options]
```

### Methods

#### `most_active_cookie_for_date`

Returns the most active cookie(s) on a specific date.

```bash
python main.py most_active_cookie_for_date <log_file_path> -d <date>
```

Example:

```bash
python main.py most_active_cookie_for_date cookie_log.csv -d 2018-12-09
```

#### `most_active_cookie_for_range`

Returns the most active cookie(s) across an inclusive date range.

```bash
python main.py most_active_cookie_for_range <log_file_path> -from <start_date> -to <end_date>
```

Example:

```bash
python main.py most_active_cookie_for_range cookie_log.csv -from 2018-12-08 -to 2018-12-09
```

The log file must be a CSV with at minimum two columns: `cookie` and `timestamp`. Timestamps must be ISO 8601 format. Extra columns are ignored. Rows with missing values or unparseable timestamps are skipped with a warning.

If multiple cookies share the highest frequency, all are returned, one per line.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
chmod +x most_active_cookie
```

## Data Structures

**`Cookie`** — represents a single cookie and its activity history. Internally stores a `dict[date, list[time]]` mapping each date to the times the cookie was seen. Identity is determined by name.

**`CookieLog`** — parses the CSV and maintains two indexes built in a single pass:

- `_date_log: dict[date, set[Cookie]]` — primary index, maps each date to the set of cookies active that day. Used for date-based queries.
- `_cookie_registry: dict[str, Cookie]` — secondary index, maps cookie name to its Cookie object. Ensures a single Cookie object exists per unique name, and supports future cookie-centric queries.

## Implementation Decisions

**Plain dicts instead of a sorted tree** — my original design used a self-balancing tree keyed on `date` to support range queries. Since only the standard library was used and it has no native sorted tree, plain dicts are used instead. Range queries iterate over all keys and filter by date bounds. If performance becomes a concern, the `bisect` module could provide binary search over a sorted list as a standard library alternative.

**Secondary index** — `_cookie_registry` was added not just for deduplication during parsing, but as a foundation for future cookie-centric queries (e.g. "which days was cookie X most active"). Both indexes are built in a single CSV parse pass at no extra time cost.

**Cookie objects stored by reference** — both indexes hold references to the same Cookie objects. Mutating a cookie's activity via either index affects the same object in memory. This is verified explicitly in the test suite.

**Set for `_date_log` values** — using `set[Cookie]` instead of `list[Cookie]` makes membership checks O(1) on insert rather than O(n). Requires `Cookie` to implement `__hash__`, which is based on name consistent with `__eq__`.

**Per-row error recovery** — malformed rows (missing values, bad timestamps) are skipped with a warning rather than failing the entire load. File-level errors (missing file, missing headers) raise exceptions since the program cannot continue meaningfully.

**Implementation exposure in tests** — `test_same_cookie_object_across_dates` accesses `_cookie_registry` and `_date_log` directly to verify object identity across both indexes. This couples the test to the implementation but tests a correctness property that has no clean public interface equivalent.

## Testing

```bash
pytest
```

Or with verbose output:

```bash
pytest -v
```

Test fixtures are in `tests/log_file_fixtures/`. Tests cover single winners, ties, empty files, missing headers, malformed rows, bad timestamps, range queries, range ties, and CLI behaviour.