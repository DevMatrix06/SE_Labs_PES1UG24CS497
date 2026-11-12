# Lab 7: Fuzzing for Input Validation Bugs

Tejas P (PES1UG24CS497)

Fuzz testing `processor.py` with Hypothesis, then fixing what it found.

## Files

| File | What it is |
|------|------------|
| `processor.py` | Fixed module. Bad input returns `None` instead of raising. |
| `test_processor.py` | Hypothesis tests (three no-crash tests from the handout, plus a few extra checks) |
| `buggy/processor.py` | Original starter code, kept for the "before" runs |
| `screenshots/` | Console screenshots used in the PDF |
| `logs/` | Text copies of the terminal output |
| `Lab7_FuzzTesting_PES1UG24CS497.pdf` | Screenshots of each step and a bug summary |
| `make_pdf.py` | Script that builds the PDF from `screenshots/` |

## Running

```
pip install hypothesis pytest
python processor.py
python -m pytest test_processor.py -v
```

To see the failures, copy `test_processor.py` into `buggy/` and run pytest there (6 failed, 3 passed).
