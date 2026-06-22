# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
The game's purpose is to guess a mystery number.
- [ ] Detail which bugs you found.
1) The secret number is outside the range
2) New Game does not work after the game is over
3) The History appends the previous number guessed, not the most recent
4) New Game does not restart history or score but resets attemps and makes a new secret number
5) The Range of Numbers appear to be 1 to 100 for every difficulty
- [ ] Explain what fixes you applied.
Fixed the bug that new game would not start a new game. 
Fixed the bug where new game would not clear the history
## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Enter a guess of 50
2. Game returns a guess of too low 
3. Enters a guess of 57 
4. Game returns You won! The secret was 54. Final score: 20
5. Click new game button 
6. Game resets, score resets and history is cleared 
**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```
================================================= test session starts ==================================================
platform darwin -- Python 3.13.1, pytest-9.0.3, pluggy-1.6.0 -- /Users/tuandinh/Documents/code/CodePath/projects/ai110-module1show-gameglitchinvestigator-starter/.venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/tuandinh/Documents/code/CodePath/projects/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.13.0
collected 20 items                                                                                                     
tests/test_restart_bug.py::TestRestartResetsStatus::test_status_reset_after_loss PASSED                          [  5%]
tests/test_restart_bug.py::TestRestartResetsStatus::test_status_reset_after_win PASSED                           [ 10%]
tests/test_restart_bug.py::TestRestartClearsHistory::test_history_cleared_after_loss PASSED                      [ 15%]
tests/test_restart_bug.py::TestRestartClearsHistory::test_history_cleared_after_win PASSED                       [ 20%]
tests/test_restart_bug.py::TestRestartResetsAttempts::test_attempts_reset PASSED                                 [ 25%]
tests/test_restart_bug.py::TestRestartUsesCorrectRange::test_range_matches_difficulty[Easy-1-20] PASSED          [ 30%]
tests/test_restart_bug.py::TestRestartUsesCorrectRange::test_range_matches_difficulty[Normal-1-100] PASSED       [ 35%]
tests/test_restart_bug.py::TestRestartUsesCorrectRange::test_range_matches_difficulty[Hard-1-50] PASSED          [ 40%]
tests/test_restart_bug.py::TestRestartUsesCorrectRange::test_hard_range_is_not_normal_range PASSED               [ 45%]
tests/test_restart_bug.py::TestCheckGuess::test_exact_match_is_win PASSED                                        [ 50%]
tests/test_restart_bug.py::TestCheckGuess::test_higher_guess PASSED                                              [ 55%]
tests/test_restart_bug.py::TestCheckGuess::test_lower_guess PASSED                                               [ 60%]
tests/test_restart_bug.py::TestParseGuess::test_valid_integer PASSED                                             [ 65%]
tests/test_restart_bug.py::TestParseGuess::test_float_string_truncated PASSED                                    [ 70%]
tests/test_restart_bug.py::TestParseGuess::test_empty_string_is_invalid PASSED                                   [ 75%]
tests/test_restart_bug.py::TestParseGuess::test_none_is_invalid PASSED                                           [ 80%]
tests/test_restart_bug.py::TestParseGuess::test_non_numeric_is_invalid PASSED                                    [ 85%]
tests/test_restart_bug.py::TestUpdateScore::test_win_early_gives_high_points PASSED                              [ 90%]
tests/test_restart_bug.py::TestUpdateScore::test_too_low_deducts_points PASSED                                   [ 95%]
tests/test_restart_bug.py::TestUpdateScore::test_score_never_below_minimum_on_win PASSED                         [100%]


## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
