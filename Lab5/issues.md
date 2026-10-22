# Issues found in `theater_system.py`

Reports from before the fixes are in `reports/before/` and from after in `reports/after/`.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Weak MD5 hash (Bandit B324, **High**) | Security | 25 | `ticket_code` used `hashlib.md5`, which is not safe to rely on, so ticket codes could be forged. | Switched to `hashlib.sha256`. |
| Over-permissive file mode (Bandit B103, **High**) | Security | 55 | `os.chmod("seats.json", 0o777)` gave every user read, write and execute access to the bookings file. | Removed the `chmod` call and the `os` import it left unused. The file now has normal default permissions. |
| Try/except/pass (Bandit B110, Low) | Security / Bug | 19-22 | `release_seat` used a bare `except: pass`, so any failure (even a mistyped show id) was ignored silently. | Catch only `(KeyError, ValueError)` and return `False` on failure, `True` on success. |
| No seat validation | Bug (no tool flags it) | 9-16 | Seats `-1`, `"A7"` and `25` (the show only has 20 seats) were accepted and counted as booked, which also threw off the "seats free" number. | `reserve_seat` now checks that the show exists and the seat is an `int` between 1 and the seat count. Rejected bookings are logged. |
| Seat type mismatch | Bug (no tool flags it) | 50-51 | `input()` returns a string, so `"4"` was saved instead of `4`, and both `"4"` and `4` could be booked for the same seat. | `main` converts the input to `int` and reports non-numeric input instead of booking it. |
| Mutable default argument (Pylint W0102) | Bug | 9 | `system_logs=[]` is created once and shared across every call. | Default is `None`; a fresh list is created inside the function. |
| Bare except (Pylint W0702 / Flake8 E722) | Bug / Style | 21 | Catches everything, even `KeyboardInterrupt`. | Same fix as B110 above (specific exceptions). |
| Files opened without `with` (Pylint R1732) | Bug | 28, 33 | `dump_reservations` and `load_reservations` never closed their files, so data might not get written to disk. | Use `with open(...)` and `json.dump` / `json.load`. |
| No explicit encoding (Pylint W1514) | Bug | 28, 33 | The encoding depends on the machine's locale. | Pass `encoding="utf-8"`. |
| Global statement (Pylint W0603) | Design | 32 | `global shows` replaces the module-level dict. | Use `shows.clear()` then `shows.update(data)` to change the dict in place. |
| Naming (Pylint C0103) | Style | 37 | `printSeatingSummary` is not snake_case. | Renamed to `print_seating_summary`. |
| Old-style `%` formatting (Pylint C0209) | Style | 12, 15 | Strings built with `%`. | Converted to f-strings (also in the summary and the log messages). |
| Missing docstrings (Pylint C0114 / C0116) | Style | 1, 9, 18, 24, 27, 31, 37, 42 | The module and every function had no docstring. | Added a docstring to the module and each function. |
| Line too long (Pylint C0301 / Flake8 E501) | Style | 12, 40 | Lines of 83 and 104 characters. | Wrapped to 79 characters or fewer. |
| Blank lines (Flake8 E302 / E305) | Style | 9, 18, 24, 27, 31, 37, 42, 57 | Only one blank line between top-level definitions. | Two blank lines between top-level definitions. |
| Script runs on import | Design (no tool flags it) | 57 | `main()` was called at module level, so just importing the file ran the program and asked for input. | Added `if __name__ == "__main__":`. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.87/10 (19 messages) | **10.00/10** |
| Bandit | 2 High, 1 Low | **No issues** |
| Flake8 | 11 findings | **0 findings** |
