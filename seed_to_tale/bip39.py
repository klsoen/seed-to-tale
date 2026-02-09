"""
BIP39 mnemonic handling - convert between seed phrases and entropy.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Optional, List


def load_wordlist() -> List[str]:
    """Load the BIP39 English wordlist."""
    wordlist_path = Path(__file__).parent / "wordlist.txt"
    if wordlist_path.exists():
        return wordlist_path.read_text().strip().split('\n')

    # Fallback: fetch from standard source
    raise FileNotFoundError(
        "BIP39 wordlist not found. Please ensure wordlist.txt exists."
    )


def mnemonic_to_entropy(mnemonic: str, wordlist: Optional[List[str]] = None) -> bytes:
    """
    Convert a BIP39 mnemonic phrase to its entropy bytes.

    For 12 words: 128 bits entropy + 4 bits checksum = 132 bits
    We return just the 128-bit (16 byte) entropy.
    """
    if wordlist is None:
        wordlist = load_wordlist()

    word_to_index = {word: i for i, word in enumerate(wordlist)}

    words = mnemonic.lower().strip().split()
    if len(words) not in (12, 15, 18, 21, 24):
        raise ValueError(f"Invalid mnemonic length: {len(words)} words")

    # Convert words to 11-bit indices
    bits = ''
    for word in words:
        if word not in word_to_index:
            raise ValueError(f"Invalid BIP39 word: '{word}'")
        index = word_to_index[word]
        bits += format(index, '011b')

    # Split into entropy and checksum
    checksum_bits = len(words) // 3  # 4 bits for 12 words
    entropy_bits = bits[:-checksum_bits]
    checksum = bits[-checksum_bits:]

    # Convert entropy bits to bytes
    entropy = int(entropy_bits, 2).to_bytes(len(entropy_bits) // 8, 'big')

    # Verify checksum
    expected_checksum = _compute_checksum(entropy, checksum_bits)
    if checksum != expected_checksum:
        raise ValueError("Invalid mnemonic checksum")

    return entropy


def entropy_to_mnemonic(entropy: bytes, wordlist: Optional[List[str]] = None) -> str:
    """
    Convert entropy bytes to a BIP39 mnemonic phrase.

    16 bytes (128 bits) -> 12 words
    """
    if wordlist is None:
        wordlist = load_wordlist()

    if len(entropy) not in (16, 20, 24, 28, 32):
        raise ValueError(f"Invalid entropy length: {len(entropy)} bytes")

    # Compute checksum
    checksum_bits = len(entropy) // 4  # 4 bits per 4 bytes
    checksum = _compute_checksum(entropy, checksum_bits)

    # Combine entropy and checksum
    bits = format(int.from_bytes(entropy, 'big'), f'0{len(entropy) * 8}b') + checksum

    # Split into 11-bit chunks and convert to words
    words = []
    for i in range(0, len(bits), 11):
        index = int(bits[i:i + 11], 2)
        words.append(wordlist[index])

    return ' '.join(words)


def _compute_checksum(entropy: bytes, num_bits: int) -> str:
    """Compute the BIP39 checksum for entropy."""
    h = hashlib.sha256(entropy).digest()
    checksum_byte = h[0]
    checksum_bits = format(checksum_byte, '08b')
    return checksum_bits[:num_bits]
