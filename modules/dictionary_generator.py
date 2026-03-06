"""
dictionary_generator.py - Wordlist generation engine.

Generates candidate passwords from:
  - Name + Date-of-Birth patterns
  - Common password lists
  - Keyboard walk patterns

Applies mutation rules:
  - Leetspeak substitutions
  - Case variations
  - Number/symbol suffixes
"""

import os
import itertools
from typing import Generator
from utils.logger import get_logger

logger = get_logger("DictionaryGenerator")


# ─── Mutation Rules ────────────────────────────────────────────────────────────

LEET_MAP = {
    "a": ["a", "4", "@"],
    "e": ["e", "3"],
    "i": ["i", "1", "!"],
    "o": ["o", "0"],
    "s": ["s", "5", "$"],
    "t": ["t", "7"],
    "g": ["g", "9"],
    "l": ["l", "1"],
    "b": ["b", "8"],
}

COMMON_SUFFIXES = [
    "", "1", "12", "123", "1234", "12345", "!", "@", "#",
    "2024", "2023", "2022", "2025", "!", "!!", "123!", "@123"
]

KEYBOARD_PATTERNS = [
    "qwerty", "qwertyuiop", "asdfgh", "asdfghjkl",
    "zxcvbn", "1234567890", "qazwsx", "1qaz2wsx",
    "password", "letmein", "iloveyou", "dragon",
    "!@#$%^&*", "qweasdzxc", "mnbvcxz"
]


class DictionaryGenerator:
    """Generates and mutates password wordlists."""

    def __init__(self, common_passwords_path: str = "data/common_passwords.txt"):
        self.common_passwords_path = common_passwords_path
        self._wordlist: list[str] = []

    # ─── Generators ───────────────────────────────────────────────────────────

    def from_name_dob(self, name: str, dob: str) -> list[str]:
        """
        Generate candidates from a person's name and date of birth.
        dob format: DDMMYYYY or any date string
        """
        words = []
        name = name.strip().lower()
        parts = name.split()

        dob_variants = [dob, dob[:4], dob[4:], dob[:2], dob[2:4], dob[-4:], dob[-2:]]
        dob_variants = [d for d in dob_variants if d]

        base_words = parts + [name.replace(" ", ""), name.replace(" ", "_")]

        for base in base_words:
            for dob_part in dob_variants:
                words.append(f"{base}{dob_part}")
                words.append(f"{base.capitalize()}{dob_part}")
                words.append(f"{dob_part}{base}")

        logger.info(f"Generated {len(words)} name+DOB candidates.")
        return list(set(words))

    def from_common_passwords(self) -> list[str]:
        """Load words from the common_passwords.txt file."""
        words = []
        try:
            with open(self.common_passwords_path, "r") as f:
                words = [line.strip() for line in f if line.strip()]
            logger.info(f"Loaded {len(words)} common passwords.")
        except FileNotFoundError:
            logger.error(f"Common passwords file not found: {self.common_passwords_path}")
        return words

    def from_keyboard_patterns(self) -> list[str]:
        """Return built-in keyboard walk patterns."""
        logger.info(f"Loaded {len(KEYBOARD_PATTERNS)} keyboard patterns.")
        return list(KEYBOARD_PATTERNS)

    # ─── Mutations ────────────────────────────────────────────────────────────

    def apply_leet(self, word: str, max_variants: int = 20) -> list[str]:
        """Apply leetspeak substitutions to a word (limited to avoid explosion)."""
        variants = {word}
        for orig, replacements in LEET_MAP.items():
            new_variants = set()
            for v in variants:
                for rep in replacements:
                    new_variants.add(v.replace(orig, rep))
                    if len(new_variants) > max_variants:
                        break
                if len(new_variants) > max_variants:
                    break
            variants.update(new_variants)
        return list(variants)[:max_variants]

    def apply_case_variations(self, word: str) -> list[str]:
        """Generate lowercase, uppercase, title, and mixed case variants."""
        return list({
            word.lower(),
            word.upper(),
            word.capitalize(),
            word.title(),
            word.swapcase(),
        })

    def apply_suffixes(self, word: str) -> list[str]:
        """Append common number/symbol suffixes to a word."""
        return [f"{word}{suffix}" for suffix in COMMON_SUFFIXES]

    def mutate(self, words: list[str], leet: bool = True,
               case: bool = True, suffixes: bool = True) -> list[str]:
        """
        Apply selected mutation rules to a word list.
        Returns deduplicated list of all mutations.
        """
        mutated = set(words)
        for word in words:
            if case:
                mutated.update(self.apply_case_variations(word))
            if leet:
                mutated.update(self.apply_leet(word))
            if suffixes:
                mutated.update(self.apply_suffixes(word))

        logger.info(f"Mutation complete: {len(words)} → {len(mutated)} candidates.")
        return list(mutated)

    # ─── Build & Save ─────────────────────────────────────────────────────────

    def build(self, name: str = "", dob: str = "",
              use_common: bool = True, use_keyboard: bool = True,
              leet: bool = True, case: bool = True, suffixes: bool = True) -> list[str]:
        """Combine all sources and apply mutations into a final wordlist."""
        base: list[str] = []

        if name and dob:
            base.extend(self.from_name_dob(name, dob))
        if use_common:
            base.extend(self.from_common_passwords())
        if use_keyboard:
            base.extend(self.from_keyboard_patterns())

        self._wordlist = self.mutate(list(set(base)), leet=leet, case=case, suffixes=suffixes)
        logger.info(f"Final wordlist size: {len(self._wordlist)}")
        return self._wordlist

    def save(self, filepath: str = "data/generated_wordlist.txt") -> str:
        """Save the current wordlist to a text file."""
        if not self._wordlist:
            raise ValueError("Wordlist is empty. Run build() first.")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            f.write("\n".join(self._wordlist))
        logger.info(f"Wordlist saved to {filepath}")
        return filepath

    @property
    def wordlist(self) -> list[str]:
        return self._wordlist
