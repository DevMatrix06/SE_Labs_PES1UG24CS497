# Tic-Tac-Toe Lab

This project is a single-topic two-player Tic-Tac-Toe game using
**Pygame**. It introduces students to win-condition logic, turn/move
validation, and persistent state across rounds, using a small,
readable object-oriented codebase.

---

## What's Provided

A working Tic-Tac-Toe game with:

- A 3x3 board you click on to place X
- You always play X; the computer automatically plays O right after
  you, using a simple random-move opponent - this lab is designed for
  one person to play solo against the computer, not for two people
  sharing a keyboard
- Basic win and draw detection, and a "Press R for a new round"
  restart

It has **one deliberate bug** (with several related symptoms) and
**three features** left for you to build. You are expected to
**analyze**, **interact with an AI assistant**, and **complete/fix**
the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the game:

```bash
python main.py
```

**Controls:** You play X - click a cell to place it. The computer
automatically plays O right after you. Press R for a new round.

---

## Tasks to Complete

Each task must be completed using an iterative process involving LLM
suggestions and your critical code review.

### Task 1: Fix win and draw detection

> **What you'll see, problem 1:** win three-in-a-row diagonally (top
> corner to bottom corner, either direction) and the game doesn't
> notice at all - no winner is announced, even though the board
> clearly shows one.

> **What you'll see, problem 2:** if the winning move also happens to
> be the move that fills the very last empty cell, the game announces
> "Draw!" instead of announcing the actual winner.
>

> **What you'll see, problem 3:** once a round has ended, you can keep
> clicking empty cells and new symbols keep appearing on the board.
>

> **Fix all three:** diagonals should count as wins, a genuine win
> should always be reported as a win even if the board is also full,
> and no further moves should be accepted once a round has ended.

### Task 2: Implement a persistent scoreboard

> Track how many rounds X has won, how many O has won, and how many
> have ended in a draw. This should stay visible and unchanged when
> starting a new round, and should only be cleared when the player
> explicitly resets the whole match (not just the round).

### Task 3: Implement turn and move validation

> **What you'll see:** click on a cell that already has a symbol in
> it, and your click overwrites it with your own symbol instead of
> being rejected.
>

> **Fix it:** a click on an already-occupied cell should be rejected
> entirely - the board and whose turn it is should both stay exactly
> as they were.

### Task 4: Add first-player choice and separate restart controls

> Let the player choose whether X or O goes first (since the computer
> always plays O, choosing "O starts" means the computer takes the
> first move of the round automatically). Provide two separate
> controls: one to restart just the current round (keeping the
> scoreboard), and one to reset the whole match (clearing the
> scoreboard too).

---

## Expected Behavior

- All 8 winning lines - 3 rows, 3 columns, and both diagonals - are
  detected correctly.
- A move that both wins the game and fills the last empty cell is
  always scored as a win, never as a draw.
- Once a round has ended, clicking anywhere on the board does nothing.
- Clicking an already-occupied cell is rejected outright - the board
  and current turn stay unchanged.
- The scoreboard survives a round restart but resets to zero on a full
  match reset.
- Choosing which symbol starts takes effect on the next round.

---

## Folder Structure

```
tic-tac-toe/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── rules.py
│   ├── ai.py
│   └── renderer.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history
