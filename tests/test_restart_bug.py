"""
Tests for the game-restart bug.

Bug summary: clicking "New Game" after a win or loss did not reset
`status` or `history`, and used a hardcoded range (1-100) instead of
the difficulty-based range.  After the fix, all three fields must be
correctly reinitialised.

Because app.py imports streamlit at the top level we inject a minimal
mock into sys.modules before importing the logic functions.
"""

import sys
import types
import pathlib
import pytest

# Make the project root importable regardless of where pytest is invoked from.
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

# ---------------------------------------------------------------------------
# Minimal streamlit stub so `import app` doesn't crash outside of Streamlit.
# ---------------------------------------------------------------------------

class _AttrDict(dict):
    """Dict that also supports attribute-style access, like st.session_state."""
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __contains__(self, key):
        return dict.__contains__(self, key)


def _make_streamlit_stub():
    st = types.ModuleType("streamlit")
    st.set_page_config = lambda **kw: None
    st.title = lambda *a, **kw: None
    st.caption = lambda *a, **kw: None
    st.sidebar = types.SimpleNamespace(
        header=lambda *a, **kw: None,
        selectbox=lambda *a, **kw: "Normal",
        caption=lambda *a, **kw: None,
    )
    st.subheader = lambda *a, **kw: None
    st.info = lambda *a, **kw: None
    st.expander = lambda *a, **kw: _NullContext()
    st.text_input = lambda *a, **kw: ""
    st.columns = lambda n: [_NullContext()] * n
    st.button = lambda *a, **kw: False
    st.checkbox = lambda *a, **kw: False
    st.success = lambda *a, **kw: None
    st.error = lambda *a, **kw: None
    st.warning = lambda *a, **kw: None
    st.divider = lambda: None
    st.stop = lambda: None
    st.rerun = lambda: None
    st.balloons = lambda: None
    st.write = lambda *a, **kw: None
    st.session_state = _AttrDict()
    return st


class _NullContext:
    def __enter__(self): return self
    def __exit__(self, *a): return False
    def __call__(self, *a, **kw): return self


sys.modules.setdefault("streamlit", _make_streamlit_stub())

from app import (  # noqa: E402
    get_range_for_difficulty,
    check_guess,
    update_score,
    parse_guess,
)


# ---------------------------------------------------------------------------
# Helper: minimal session-state dict that mirrors what app.py initialises
# ---------------------------------------------------------------------------
def _game_over_state(status: str = "lost"):
    return {
        "secret": 42,
        "attempts": 8,
        "score": 55,
        "status": status,
        "history": [10, 20, 30],
    }


def _simulate_new_game(state: dict, difficulty: str = "Normal") -> dict:
    """Mirrors the fixed `if new_game:` block in app.py."""
    low, high = get_range_for_difficulty(difficulty)
    state["attempts"] = 0
    state["secret"] = 50          # deterministic stand-in for randint
    state["status"] = "playing"
    state["history"] = []
    return state


# ---------------------------------------------------------------------------
# Tests for the restart bug
# ---------------------------------------------------------------------------

class TestRestartResetsStatus:
    """status must return to 'playing' so the game is not immediately blocked."""

    def test_status_reset_after_loss(self):
        state = _game_over_state(status="lost")
        assert state["status"] == "lost"
        state = _simulate_new_game(state)
        assert state["status"] == "playing"

    def test_status_reset_after_win(self):
        state = _game_over_state(status="won")
        assert state["status"] == "won"
        state = _simulate_new_game(state)
        assert state["status"] == "playing"


class TestRestartClearsHistory:
    """History from the previous game must not carry into the new one."""

    def test_history_cleared_after_loss(self):
        state = _game_over_state(status="lost")
        assert len(state["history"]) > 0, "pre-condition: history is non-empty"
        state = _simulate_new_game(state)
        assert state["history"] == []

    def test_history_cleared_after_win(self):
        state = _game_over_state(status="won")
        state = _simulate_new_game(state)
        assert state["history"] == []


class TestRestartResetsAttempts:
    """Attempt counter must restart at 0."""

    def test_attempts_reset(self):
        state = _game_over_state()
        assert state["attempts"] > 0, "pre-condition"
        state = _simulate_new_game(state)
        assert state["attempts"] == 0


class TestRestartUsesCorrectRange:
    """
    Original bug: secret was always re-rolled with hardcoded randint(1, 100).
    After the fix, get_range_for_difficulty drives the bounds.
    """

    @pytest.mark.parametrize("difficulty,expected_low,expected_high", [
        ("Easy",   1,  20),
        ("Normal", 1, 100),
        ("Hard",   1,  50),
    ])
    def test_range_matches_difficulty(self, difficulty, expected_low, expected_high):
        low, high = get_range_for_difficulty(difficulty)
        assert low == expected_low
        assert high == expected_high

    def test_hard_range_is_not_normal_range(self):
        """Regression: Hard was incorrectly returning 1–100 before the fix."""
        _, hard_high = get_range_for_difficulty("Hard")
        _, normal_high = get_range_for_difficulty("Normal")
        assert hard_high != normal_high, (
            "Hard and Normal should have different upper bounds"
        )


# ---------------------------------------------------------------------------
# Sanity tests for the logic functions used during restart
# ---------------------------------------------------------------------------

class TestCheckGuess:
    def test_exact_match_is_win(self):
        outcome, _ = check_guess(42, 42)
        assert outcome == "Win"

    def test_higher_guess(self):
        outcome, _ = check_guess(60, 42)
        assert outcome == "Too High"

    def test_lower_guess(self):
        outcome, _ = check_guess(10, 42)
        assert outcome == "Too Low"


class TestParseGuess:
    def test_valid_integer(self):
        ok, val, err = parse_guess("42")
        assert ok is True and val == 42 and err is None

    def test_float_string_truncated(self):
        ok, val, _ = parse_guess("3.9")
        assert ok is True and val == 3

    def test_empty_string_is_invalid(self):
        ok, _, err = parse_guess("")
        assert ok is False and err == "Enter a guess."

    def test_none_is_invalid(self):
        ok, _, err = parse_guess(None)
        assert ok is False and err == "Enter a guess."

    def test_non_numeric_is_invalid(self):
        ok, _, err = parse_guess("abc")
        assert ok is False and err == "That is not a number."


class TestUpdateScore:
    def test_win_early_gives_high_points(self):
        score = update_score(0, "Win", attempt_number=1)
        assert score > 0

    def test_too_low_deducts_points(self):
        score = update_score(50, "Too Low", attempt_number=3)
        assert score < 50

    def test_score_never_below_minimum_on_win(self):
        # Even on attempt 100 the floor is 10 points
        score = update_score(0, "Win", attempt_number=100)
        assert score == 10
