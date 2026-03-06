"""
brute_force.py - Brute-force attack simulation engine.

Simulates iterating over character combinations to find a password.
This is 100% local and educational — no system access whatsoever.
"""

import itertools
import time
import math
from typing import Generator, Optional
from dataclasses import dataclass
from utils.logger import get_logger

logger = get_logger("BruteForce")


# Character set definitions
CHARSETS = {
    "Lowercase (a-z)": "abcdefghijklmnopqrstuvwxyz",
    "Uppercase (A-Z)": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "Digits (0-9)": "0123456789",
    "Symbols (!@#...)": "!@#$%^&*()_+-=[]{}|;:'\",.<>?/`~\\",
}


@dataclass
class BruteForceStats:
    target_length: int
    charset_size: int
    charset_name: str
    total_combinations: int
    estimated_seconds: float  # at simulated speed
    real_world_estimate: str  # at 10B/s GPU speed


class BruteForceEngine:
    """Simulates brute-force password cracking for educational demonstration."""

    GPU_SPEED = 1e10  # 10 billion guesses/sec (modern cracking rig)
    SIM_SPEED = 50_000  # simulated attempts/sec for UI animation

    def __init__(self, selected_charsets: list[str], max_length: int = 6):
        self.selected_charsets = selected_charsets
        self.max_length = max_length
        self.charset = self._build_charset()

    def _build_charset(self) -> str:
        chars = ""
        for name in self.selected_charsets:
            if name in CHARSETS:
                chars += CHARSETS[name]
        return "".join(sorted(set(chars))) if chars else "abcdefghijklmnopqrstuvwxyz"

    def compute_stats(self, target_length: int) -> BruteForceStats:
        """Compute combination counts and time estimates."""
        n = len(self.charset)
        # Total combinations for lengths 1..target_length
        total = sum(n ** l for l in range(1, target_length + 1))
        sim_seconds = total / self.SIM_SPEED
        gpu_seconds = total / (2 * self.GPU_SPEED)  # avg = half keyspace

        return BruteForceStats(
            target_length=target_length,
            charset_size=n,
            charset_name="+".join(self.selected_charsets),
            total_combinations=total,
            estimated_seconds=sim_seconds,
            real_world_estimate=self._format_time(gpu_seconds),
        )

    def _format_time(self, seconds: float) -> str:
        if seconds < 1:
            return "< 1 second"
        elif seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.1f} minutes"
        elif seconds < 86400:
            return f"{seconds/3600:.1f} hours"
        elif seconds < 31536000:
            return f"{seconds/86400:.1f} days"
        elif seconds < 3.154e9:
            return f"{seconds/31536000:.1f} years"
        else:
            return "centuries"

    def simulate(
        self,
        target_password: str,
        max_attempts: int = 100_000,
    ) -> Generator[dict, None, None]:
        """
        Simulate brute-force search. Yields progress dicts.
        Stops early if target found or max_attempts reached.
        """
        target = target_password
        target_len = len(target)
        charset = self.charset
        attempts = 0
        start = time.perf_counter()
        found = False

        logger.info(f"Starting brute-force sim: target_len={target_len}, charset_size={len(charset)}")

        # Iterate increasing lengths up to target length
        for length in range(1, min(target_len, self.max_length) + 1):
            for combo in itertools.product(charset, repeat=length):
                attempts += 1
                candidate = "".join(combo)

                is_match = candidate == target
                elapsed = time.perf_counter() - start

                yield {
                    "attempts": attempts,
                    "candidate": candidate,
                    "length": length,
                    "found": is_match,
                    "elapsed": elapsed,
                    "speed": attempts / max(elapsed, 0.001),
                }

                if is_match:
                    found = True
                    logger.info(f"Found '{target}' after {attempts} attempts in {elapsed:.3f}s")
                    return

                if attempts >= max_attempts:
                    logger.info(f"Max attempts ({max_attempts}) reached without match.")
                    return

        if not found:
            logger.info("Brute-force simulation ended without match (target too long or not in charset).")

    def estimate_only(self, password_length: int) -> dict:
        """Return stats without running simulation."""
        stats = self.compute_stats(password_length)
        return {
            "charset_size": stats.charset_size,
            "total_combinations": stats.total_combinations,
            "real_world_estimate": stats.real_world_estimate,
            "charset": self.charset[:40] + ("..." if len(self.charset) > 40 else ""),
        }
