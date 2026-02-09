"""
Syllable encoding system for converting entropy to pronounceable strings.

Uses 256 distinct, pronounceable syllables (8 bits per syllable).
A 128-bit seed phrase entropy = 16 syllables.
"""
from __future__ import annotations

from typing import List

# Consonants that work well at the start of syllables
ONSETS = [
    '', 'b', 'bl', 'br', 'ch', 'd', 'dr', 'f', 'fl', 'fr', 'g', 'gl', 'gr',
    'h', 'j', 'k', 'kl', 'kr', 'l', 'm', 'n', 'p', 'pl', 'pr', 'r', 's',
    'sh', 'sk', 'sl', 'sm', 'sn', 'sp', 'st', 'str', 'sw', 't', 'tr', 'th',
    'v', 'w', 'z'
]

# Vowel sounds
VOWELS = ['a', 'e', 'i', 'o', 'u', 'ai', 'au', 'ei', 'ou', 'oo']

# Consonants that work well at the end of syllables
CODAS = [
    '', 'b', 'd', 'f', 'g', 'k', 'l', 'ld', 'lk', 'lm', 'lp', 'lt',
    'm', 'n', 'nd', 'ng', 'nk', 'nt', 'p', 'r', 'rb', 'rd', 'rk', 'rm',
    'rn', 'rp', 'rt', 's', 'sh', 'sk', 'sp', 'st', 't', 'th', 'x', 'z'
]


def generate_syllable_table() -> List[str]:
    """
    Generate exactly 256 unique, pronounceable syllables.
    Each syllable maps to a byte value (0-255).
    """
    syllables = []
    seen = set()

    # Generate CV and CVC combinations, prioritizing shorter ones
    for onset in ONSETS:
        for vowel in VOWELS:
            # CV pattern (no coda)
            syl = onset + vowel
            if syl not in seen and len(syllables) < 256:
                syllables.append(syl)
                seen.add(syl)

            # CVC pattern (with coda)
            for coda in CODAS:
                if coda:  # Skip empty coda (already handled above)
                    syl = onset + vowel + coda
                    if syl not in seen and len(syllables) < 256:
                        # Filter out awkward combinations
                        if not _is_awkward(syl):
                            syllables.append(syl)
                            seen.add(syl)

                if len(syllables) >= 256:
                    break
            if len(syllables) >= 256:
                break
        if len(syllables) >= 256:
            break

    return syllables[:256]


def _is_awkward(syllable: str) -> bool:
    """Filter out syllables that are hard to pronounce or offensive."""
    awkward_patterns = [
        'shsh', 'thth', 'xx', 'zz', 'shth', 'thsh',
    ]
    for pattern in awkward_patterns:
        if pattern in syllable:
            return True
    return False


# Pre-generated syllable table (deterministic, 256 entries)
SYLLABLE_TABLE = generate_syllable_table()

# Reverse lookup: syllable -> byte value
SYLLABLE_TO_BYTE = {syl: i for i, syl in enumerate(SYLLABLE_TABLE)}


def bytes_to_syllables(data: bytes) -> str:
    """Convert bytes to a pronounceable syllable string."""
    return ''.join(SYLLABLE_TABLE[b] for b in data)


def bytes_to_syllable_list(data: bytes) -> List[str]:
    """Convert bytes to a list of syllables."""
    return [SYLLABLE_TABLE[b] for b in data]


def syllables_to_bytes(syllable_string: str) -> bytes:
    """Convert a syllable string back to bytes."""
    result = []
    remaining = syllable_string.lower()

    while remaining:
        # Try to match longest syllable first
        matched = False
        for length in range(6, 0, -1):  # Max syllable length is ~6 chars
            candidate = remaining[:length]
            if candidate in SYLLABLE_TO_BYTE:
                result.append(SYLLABLE_TO_BYTE[candidate])
                remaining = remaining[length:]
                matched = True
                break

        if not matched:
            raise ValueError(f"Cannot parse syllable at: '{remaining[:10]}...'")

    return bytes(result)
