"""
entropy.py - Password entropy calculation utilities.
Provides functions for computing password entropy and estimating crack time.
"""

import math


def calculate_charset_size(password: str) -> int:
    """Determine the effective character set size based on password contents."""
    size = 0
    if any(c.islower() for c in password):
        size += 26
    if any(c.isupper() for c in password):
        size += 26
    if any(c.isdigit() for c in password):
        size += 10
    if any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in password):
        size += 32
    if any(c in " \t`~\\^" for c in password):
        size += 6
    return max(size, 1)


def calculate_entropy(password: str) -> float:
    """
    Compute Shannon entropy bits for a given password.
    Formula: entropy = length * log2(charset_size)
    """
    charset_size = calculate_charset_size(password)
    length = len(password)
    if length == 0:
        return 0.0
    return length * math.log2(charset_size)


def estimate_crack_time(entropy: float, guesses_per_second: float = 1e10) -> str:
    """
    Estimate time to crack based on entropy and assumed attack speed.
    Default: 10 billion guesses/second (modern GPU cluster).
    """
    total_combinations = 2 ** entropy
    seconds = total_combinations / (2 * guesses_per_second)  # avg case = half keyspace

    if seconds < 1:
        return "< 1 second"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{seconds / 60:.1f} minutes"
    elif seconds < 86400:
        return f"{seconds / 3600:.1f} hours"
    elif seconds < 31536000:
        return f"{seconds / 86400:.1f} days"
    elif seconds < 3.154e9:
        return f"{seconds / 31536000:.1f} years"
    elif seconds < 3.154e12:
        return f"{seconds / 3.154e9:.1f} thousand years"
    elif seconds < 3.154e15:
        return f"{seconds / 3.154e12:.1f} million years"
    else:
        return "billions of years"


def get_entropy_label(entropy: float) -> tuple[str, str]:
    """Return (label, color_hex) based on entropy value."""
    if entropy < 28:
        return ("Very Weak", "#ff4444")
    elif entropy < 36:
        return ("Weak", "#ff8800")
    elif entropy < 60:
        return ("Moderate", "#ffcc00")
    elif entropy < 128:
        return ("Strong", "#44dd44")
    else:
        return ("Very Strong", "#00ffaa")
