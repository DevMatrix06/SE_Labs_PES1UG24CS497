# Reflection

**1. Which issues were easiest and which were hardest to fix?**

The easy ones were the tool warnings that have a one-line fix: the blank lines and line lengths from Flake8, the f-string and naming messages from Pylint, and swapping MD5 for SHA-256 and deleting the chmod line for Bandit. The hard part wasn't in any report. When I ran the program, seats like -1, "A7" and 25 (on a 20-seat show) were booked without complaint, so I had to decide what a valid seat actually is and what to do when the input is wrong. I went with a whole number from 1 to the number of seats, and anything else gets rejected with a message.

**2. Did the tools give false positives or miss things?**

I didn't see any real false positives, but some warnings felt minor, like the missing docstrings and the low-severity try/except/pass. What the tools missed were the bugs that matter most for this program. They didn't notice that seats weren't validated, or that the seat typed by the user was saved as the text "4" instead of the number 4, so the same seat could be booked twice. They also didn't mind that the program starts running as soon as you import the file. Those only showed up because I ran it and read the output, so the tools help but don't replace testing.

**3. How could you use static analysis in a real project?**

I'd run all three tools as a pre-commit hook so problems show up before the code is even committed, and again in CI on every pull request. The build should fail on Bandit high or medium findings, on any Flake8 error, and if the Pylint score drops under something like 9.5. That way reviewers can focus on whether the logic is right instead of pointing out style problems.

**4. What improved in this code?**

Security is better: the ticket code uses SHA-256 and the bookings file is no longer open to everyone with 777 permissions. It's also more reliable, because files are closed properly, errors aren't swallowed silently, and the shared default list bug is gone. It's easier to read and reuse, with docstrings, snake_case names and a main guard so importing the file doesn't run it. In numbers: Pylint went from 5.87 to 10.00, Bandit from 3 issues (2 high, 1 low) to none, and Flake8 from 11 warnings to none.
