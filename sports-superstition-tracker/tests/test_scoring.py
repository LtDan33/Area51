import math

from app.main import compute_correlation_score


def test_zero_gap_positive_peaks_at_ten():
    assert compute_correlation_score(0.0, positive=True) == 10.0


def test_half_second_gap_still_peaks():
    assert compute_correlation_score(0.5, positive=True) == 10.0


def test_mid_range_gap_decays_linearly():
    # 5.25s is exactly halfway through the decay window (0.5s -> 10s)
    result = compute_correlation_score(5.25, positive=True)
    assert math.isclose(result, 5.0, abs_tol=0.1)


def test_ten_second_gap_is_zero():
    assert compute_correlation_score(10.0, positive=True) == 0.0


def test_over_window_returns_zero():
    assert compute_correlation_score(10.1, positive=True) == 0.0


def test_negative_gap_returns_zero():
    assert compute_correlation_score(-0.1, positive=True) == 0.0


def test_opposing_team_scoring_is_negative():
    result = compute_correlation_score(2.0, positive=False)
    assert result < 0
    # Same magnitude as positive case
    assert result == -compute_correlation_score(2.0, positive=True)
