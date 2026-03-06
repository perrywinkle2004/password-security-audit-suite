"""
hash_handler.py - Hash generation and dictionary-based crack simulation.

Supports MD5, SHA-1, SHA-256, SHA-512.
All operations are purely local and educational.
"""

import hashlib
import time
from dataclasses import dataclass, field
from typing import Optional, Generator
from utils.logger import get_logger

logger = get_logger("HashHandler")


SUPPORTED_ALGORITHMS = {
    "MD5": "md5",
    "SHA-1": "sha1",
    "SHA-256": "sha256",
    "SHA-512": "sha512",
}


@dataclass
class CrackResult:
    found: bool
    password: Optional[str] = None
    algorithm: str = ""
    target_hash: str = ""
    attempts: int = 0
    elapsed_seconds: float = 0.0
    candidates_checked: int = 0

    def summary(self) -> str:
        if self.found:
            return (
                f"✅ CRACKED in {self.elapsed_seconds:.3f}s | "
                f"Password: '{self.password}' | Attempts: {self.attempts}"
            )
        return (
            f"❌ Not found after {self.attempts} attempts "
            f"({self.elapsed_seconds:.3f}s elapsed)"
        )


class HashHandler:
    """Handles hashing and educational dictionary-attack simulation."""

    def __init__(self, algorithm: str = "SHA-256"):
        if algorithm not in SUPPORTED_ALGORITHMS:
            raise ValueError(f"Unsupported algorithm: {algorithm}. Choose from {list(SUPPORTED_ALGORITHMS)}")
        self.algorithm = algorithm
        self._algo_key = SUPPORTED_ALGORITHMS[algorithm]

    def hash_password(self, password: str) -> str:
        """Hash a plaintext password using the selected algorithm."""
        try:
            h = hashlib.new(self._algo_key)
            h.update(password.encode("utf-8"))
            digest = h.hexdigest()
            logger.info(f"Hashed password using {self.algorithm}")
            return digest
        except Exception as e:
            logger.error(f"Hashing failed: {e}")
            raise

    def verify(self, password: str, known_hash: str) -> bool:
        """Check if a password matches a known hash."""
        return self.hash_password(password) == known_hash.lower().strip()

    def dictionary_attack(
        self,
        target_hash: str,
        wordlist: list[str],
        max_attempts: Optional[int] = None,
    ) -> Generator[dict, None, CrackResult]:
        """
        Simulate a dictionary attack by hashing each candidate.
        Yields progress dicts; returns CrackResult at end.

        Usage (generator-style):
            gen = handler.dictionary_attack(hash, words)
            for progress in gen:
                ...  # update UI
        """
        target_hash = target_hash.lower().strip()
        start = time.perf_counter()
        attempts = 0
        total = len(wordlist) if not max_attempts else min(len(wordlist), max_attempts)
        candidates = wordlist[:total]

        logger.info(f"Starting dictionary attack: {total} candidates, algo={self.algorithm}")

        for word in candidates:
            attempts += 1
            candidate_hash = self.hash_password(word)

            progress = {
                "attempts": attempts,
                "total": total,
                "current_word": word,
                "progress_pct": attempts / total,
                "found": False,
            }

            if candidate_hash == target_hash:
                elapsed = time.perf_counter() - start
                result = CrackResult(
                    found=True,
                    password=word,
                    algorithm=self.algorithm,
                    target_hash=target_hash,
                    attempts=attempts,
                    elapsed_seconds=elapsed,
                    candidates_checked=attempts,
                )
                progress["found"] = True
                progress["password"] = word
                yield progress
                return result

            yield progress

        elapsed = time.perf_counter() - start
        return CrackResult(
            found=False,
            algorithm=self.algorithm,
            target_hash=target_hash,
            attempts=attempts,
            elapsed_seconds=elapsed,
            candidates_checked=attempts,
        )

    def identify_algorithm_hint(self, hash_str: str) -> str:
        """Guess likely algorithm from hash length."""
        length = len(hash_str.strip())
        hints = {
            32: "Likely MD5",
            40: "Likely SHA-1",
            64: "Likely SHA-256",
            128: "Likely SHA-512",
        }
        return hints.get(length, "Unknown algorithm (check hash length)")
