"""
Library of Babel - Local Implementation

Implements the Library of Babel algorithm locally for fully offline operation.
No internet required.

Algorithm based on: https://github.com/cakenggt/Library-Of-Pybel
"""
from __future__ import annotations

import string
from typing import Tuple

# Character set: a-z, space, comma, period (29 characters)
CHARSET = "abcdefghijklmnopqrstuvwxyz ,."
CHARSET_LEN = 29
PAGE_LENGTH = 3200  # 80 chars × 40 lines
LINES_PER_PAGE = 40
CHARS_PER_LINE = 80

# Base-36 for hex addresses
BASE36 = string.digits + string.ascii_lowercase


def _char_to_val(c: str) -> int:
    """Convert character to value (0-28)."""
    if c.isalpha():
        return ord(c.lower()) - ord('a')
    elif c == ' ':
        return 26
    elif c == ',':
        return 27
    elif c == '.':
        return 28
    return 26  # default to space


def _val_to_char(v: int) -> str:
    """Convert value to character."""
    v = v % CHARSET_LEN
    if v < 26:
        return chr(ord('a') + v)
    elif v == 26:
        return ' '
    elif v == 27:
        return ','
    else:
        return '.'


def _to_base36(num: int) -> str:
    """Convert integer to base-36 string."""
    if num == 0:
        return '0'
    result = []
    while num:
        result.append(BASE36[num % 36])
        num //= 36
    return ''.join(reversed(result))


def _from_base36(s: str) -> int:
    """Convert base-36 string to integer."""
    return int(s.lower(), 36)


def _normalize_text(text: str) -> str:
    """Normalize text: lowercase, valid chars only, pad to 3200."""
    result = []
    for c in text.lower():
        if c in CHARSET:
            result.append(c)
        else:
            result.append(' ')

    text = ''.join(result).rstrip()

    # Pad to PAGE_LENGTH
    if len(text) < PAGE_LENGTH:
        text = text.ljust(PAGE_LENGTH)
    else:
        text = text[:PAGE_LENGTH]

    return text


def _text_to_number(text: str) -> int:
    """Convert text to base-29 number."""
    text = _normalize_text(text)
    result = 0
    for i, c in enumerate(reversed(text)):
        result += _char_to_val(c) * (CHARSET_LEN ** i)
    return result


def _number_to_text(num: int) -> str:
    """Convert base-29 number to text."""
    chars = []
    for _ in range(PAGE_LENGTH):
        chars.append(_val_to_char(num % CHARSET_LEN))
        num //= CHARSET_LEN
    return ''.join(reversed(chars))


def _make_coordinate(wall: int, shelf: int, volume: int, page: int) -> int:
    """Create library coordinate from location."""
    # Format: PPPVVSW (page 3 digits, volume 2 digits, shelf 1 digit, wall 1 digit)
    return int(f"{page:03d}{volume:02d}{shelf}{wall}")


def search_text_local(text: str, wall: int = 1, shelf: int = 1, volume: int = 1, page: int = 1) -> Tuple[str, int, int, int, int]:
    """
    Find Library of Babel coordinates for text (LOCAL - no internet).

    Returns: (hex_name, wall, shelf, volume, page)
    """
    coord = _make_coordinate(wall, shelf, volume, page)
    text_num = _text_to_number(text)

    # Combine: coordinate * 29^3200 + text_number
    combined = coord * (CHARSET_LEN ** PAGE_LENGTH) + text_num
    hex_name = _to_base36(combined)

    return hex_name, wall, shelf, volume, page


def get_page_content(hex_name: str, wall: int, shelf: int, volume: int, page: int) -> str:
    """
    Get the text content of a Library of Babel page (LOCAL - no internet).

    Returns the 3200-character page content.
    """
    coord = _make_coordinate(wall, shelf, volume, page)
    combined = _from_base36(hex_name)

    # Extract text number
    text_num = combined - coord * (CHARSET_LEN ** PAGE_LENGTH)

    return _number_to_text(text_num)


def format_page(content: str) -> str:
    """Format page content with line breaks (80 chars per line, 40 lines)."""
    lines = []
    for i in range(0, len(content), CHARS_PER_LINE):
        lines.append(content[i:i + CHARS_PER_LINE])
    return '\n'.join(lines[:LINES_PER_PAGE])


def coordinates_to_url(hex_name: str, wall: int, shelf: int, volume: int, page: int) -> str:
    """Generate a Library of Babel URL from coordinates."""
    return f"https://libraryofbabel.info/book.cgi?{hex_name}-w{wall}-s{shelf}-v{volume:02d}:{page}"


def verify_text_on_page(text: str, hex_name: str, wall: int, shelf: int, volume: int, page: int) -> bool:
    """Verify that text appears on the specified page."""
    content = get_page_content(hex_name, wall, shelf, volume, page)
    return text.lower().strip() in content


# Convenience function that matches the old API but works offline
def search_text(text: str, wall: int = 1, shelf: int = 1, volume: int = 1, page: int = 1) -> Tuple[str, int, int, int, int]:
    """
    Find Library of Babel coordinates for text.

    This version works OFFLINE using the local algorithm.
    """
    return search_text_local(text, wall, shelf, volume, page)
