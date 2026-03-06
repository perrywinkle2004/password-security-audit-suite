"""
strength_analyzer.py - Password strength evaluation engine.

Evaluates:
  - Length score
  - Character diversity
  - Shannon entropy
  - Dictionary match detection
  - Pattern detection (repeats, sequences, keyboard walks)

Returns a structured StrengthReport with score, label, and suggestions.
"""

import re
import math
from dataclasses import dataclass, field
from utils.entropy import calculate_entropy, calculate_charset_size, estimate_crack_time
from utils.logger import get_logger

logger = get_logger("StrengthAnalyzer")


COMMON_PATTERNS = [
    r"(.)\1{2,}",          # Repeated characters (aaa, 111)
    r"(012|123|234|345|456|567|678|789|890|987|876|765|654|543|432|321|210)",  # Sequential digits
    r"(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)",  # Sequential letters
    r"(qwerty|asdfgh|zxcvbn|qazwsx|1qaz|2wsx)",  # Keyboard walks
]

SCORE_WEIGHTS = {
    "length": 30,
    "diversity": 25,
    "entropy": 25,
    "no_common": 10,
    "no_pattern": 10,
}


@dataclass
class StrengthReport:
    password: str
    score: int                     # 0–100
    label: str                     # Weak / Moderate / Strong / Very Strong
    label_color: str               # Hex color
    entropy_bits: float
    charset_size: int
    crack_time: str
    length_score: int
    diversity_score: int
    entropy_score: int
    common_match: bool
    pattern_found: bool
    suggestions: list[str] = field(default_factory=list)
    details: dict = field(default_factory=dict)


class StrengthAnalyzer:
    """Analyzes a password and produces a detailed StrengthReport."""

    def __init__(self, common_passwords_path: str = "data/common_passwords.txt"):
        self._common: set[str] = set()
        self._load_common(common_passwords_path)

    def _load_common(self, path: str) -> None:
        try:
            with open(path) as f:
                self._common = {line.strip().lower() for line in f if line.strip()}
            logger.info(f"Loaded {len(self._common)} common passwords for analysis.")
        except FileNotFoundError:
            logger.warning("Common passwords file not found; skipping dictionary check.")

    # ─── Scoring ──────────────────────────────────────────────────────────────

    def _score_length(self, password: str) -> tuple[int, list[str]]:
        length = len(password)
        suggestions = []
        if length < 8:
            score = 0
            suggestions.append("Use at least 8 characters.")
        elif length < 12:
            score = 50
            suggestions.append("Consider using 12+ characters for better security.")
        elif length < 16:
            score = 80
        else:
            score = 100
        return score, suggestions

    def _score_diversity(self, password: str) -> tuple[int, list[str]]:
        has_lower = bool(re.search(r"[a-z]", password))
        has_upper = bool(re.search(r"[A-Z]", password))
        has_digit = bool(re.search(r"\d", password))
        has_symbol = bool(re.search(r"[^a-zA-Z0-9]", password))

        count = sum([has_lower, has_upper, has_digit, has_symbol])
        score = count * 25  # 25 per category
        suggestions = []

        if not has_upper:
            suggestions.append("Add uppercase letters (A–Z).")
        if not has_lower:
            suggestions.append("Add lowercase letters (a–z).")
        if not has_digit:
            suggestions.append("Include at least one digit (0–9).")
        if not has_symbol:
            suggestions.append("Include special characters (!@#$...).")

        return score, suggestions

    def _score_entropy(self, entropy: float) -> int:
        if entropy < 28:
            return 0
        elif entropy < 36:
            return 25
        elif entropy < 60:
            return 55
        elif entropy < 100:
            return 80
        else:
            return 100

    def _check_common(self, password: str) -> bool:
        return password.lower() in self._common

    def _check_patterns(self, password: str) -> tuple[bool, list[str]]:
        found = []
        for pattern in COMMON_PATTERNS:
            if re.search(pattern, password.lower()):
                found.append(pattern)
        return bool(found), found

    def _compute_label(self, score: int) -> tuple[str, str]:
        if score < 30:
            return "Weak", "#ff4444"
        elif score < 55:
            return "Moderate", "#ff8800"
        elif score < 80:
            return "Strong", "#44dd44"
        else:
            return "Very Strong", "#00ffaa"

    # ─── Public API ───────────────────────────────────────────────────────────

    def analyze(self, password: str) -> StrengthReport:
        """Full password strength analysis. Returns StrengthReport."""
        if not password:
            return StrengthReport(
                password="", score=0, label="Weak", label_color="#ff4444",
                entropy_bits=0, charset_size=0, crack_time="instant",
                length_score=0, diversity_score=0, entropy_score=0,
                common_match=False, pattern_found=False,
                suggestions=["Enter a password to analyze."]
            )

        logger.info(f"Analyzing password of length {len(password)}")

        # Individual scores
        length_score, length_sugg = self._score_length(password)
        diversity_score, diversity_sugg = self._score_diversity(password)

        entropy = calculate_entropy(password)
        charset = calculate_charset_size(password)
        entropy_score = self._score_entropy(entropy)
        crack_time = estimate_crack_time(entropy)

        is_common = self._check_common(password)
        has_pattern, patterns = self._check_patterns(password)

        # Weighted total
        base_score = int(
            length_score * 0.30 +
            diversity_score * 0.25 +
            entropy_score * 0.25
        )

        # Penalties
        if is_common:
            base_score = max(0, base_score - 30)
        if has_pattern:
            base_score = max(0, base_score - 10)

        base_score = min(100, base_score)

        # Suggestions
        suggestions = length_sugg + diversity_sugg
        if is_common:
            suggestions.insert(0, "⚠️ This password is in common password lists — avoid it.")
        if has_pattern:
            suggestions.append("Avoid predictable patterns like 'abc', '123', or keyboard rows.")
        if not suggestions:
            suggestions.append("✅ Great password! Keep it secret and don't reuse it.")

        label, color = self._compute_label(base_score)

        report = StrengthReport(
            password=password,
            score=base_score,
            label=label,
            label_color=color,
            entropy_bits=entropy,
            charset_size=charset,
            crack_time=crack_time,
            length_score=length_score,
            diversity_score=diversity_score,
            entropy_score=entropy_score,
            common_match=is_common,
            pattern_found=has_pattern,
            suggestions=suggestions,
            details={
                "length": len(password),
                "has_lower": bool(re.search(r"[a-z]", password)),
                "has_upper": bool(re.search(r"[A-Z]", password)),
                "has_digit": bool(re.search(r"\d", password)),
                "has_symbol": bool(re.search(r"[^a-zA-Z0-9]", password)),
            }
        )

        logger.info(f"Score={base_score}, Label={label}, Entropy={entropy:.1f} bits")
        return report
