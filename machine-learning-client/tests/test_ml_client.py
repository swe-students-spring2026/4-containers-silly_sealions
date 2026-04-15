"""Tests for the ML Client"""
from unittest.mock import MagicMock
import pytest
from ml_client import (
    count_filler_words,
    compute_words_per_minute,
    rate_volume,
    rate_pitch,
    rate_pace,
    analyze_audio,
    transcribe_audio,
    app,
)


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Tests for count_filler_words
def test_count_filler_words_regular():
    """Testing regualar filler word counting"""
    assert count_filler_words("um I like uh saw like a tree") == 4


def test_count_filler_words_none():
    """Testing no filler word counting"""
    assert count_filler_words("I saw a tree") == 0


def test_count_filler_words_uppercase():
    """Testing uppercase filler word counting"""
    assert count_filler_words("UM I LIKE UH SAW A TREE") == 3


def test_count_filler_words_punct():
    """Testing punctuated filler word counting"""
    assert count_filler_words("um, I like saw uh a tree") == 3


def test_count_filler_words_empty():
    """Testing empty filler word counting"""
    assert count_filler_words("") == 0


# Tests for compute_words_per_minute
def test_compute_words_per_minute_regular():
    """Testing regular computing words per minutes"""
    assert compute_words_per_minute("hi hi hi hi", 4) == 60.0


def test_compute_words_per_minute_zero():
    """Testing computing words per minutes with no time"""
    assert compute_words_per_minute("hi hi hi hi", 0) == 0.0


def test_compute_words_per_minute_decimal():
    """Testing regular computing words per minutes"""
    assert compute_words_per_minute("hi hi hi hi hi hi", 4.5) == 80.0


# rate_volume tests
def test_rate_volume_too_quiet():
    """Test volume rated as too quiet"""
    assert rate_volume(-50) == "too quiet"


def test_rate_volume_too_loud():
    """Test volume rated as too loud"""
    assert rate_volume(-5) == "too loud"


def test_rate_volume_good():
    """Test volume rated as good"""
    assert rate_volume(-20) == "good"


# rate_pitch tests
def test_rate_pitch_monotone():
    """Test pitch rated as monotone"""
    assert rate_pitch(10) == "monotone"


def test_rate_pitch_too_varied():
    """Test pitch rated as too varied"""
    assert rate_pitch(3000) == "too varied"


def test_rate_pitch_good():
    """Test pitch rated as good"""
    assert rate_pitch(500) == "good"


# rate_pace tests
def test_rate_pace_too_slow():
    """Test pace rated as too slow"""
    assert rate_pace(80) == "too slow"


def test_rate_pace_too_fast():
    """Test pace rated as too fast"""
    assert rate_pace(180) == "too fast"


def test_rate_pace_good():
    """Test pace rated as good"""
    assert rate_pace(130) == "good"


# analyze_audio Tests
def test_analyze_audio():
    """Test analyze audio returns correctly"""
    result = analyze_audio("audio_test.wav")
    assert result["duration_seconds"] == 43.43
    assert result["avg_volume_db"] == -39.84
    assert result["pitch_variance"] == 261.5883


# transcribe_audio Test
def test_transcribe_audio():
    """Test transcribe_audio returns transcript text"""
    mock_model = MagicMock()
    mock_model.transcribe.return_value = {"text": "  hi hi hi  "}
    result = transcribe_audio("fake_path.wav", mock_model)
    assert result == "hi hi hi"
