"""
Main converter: seed phrase <-> pronounceable babel string <-> Library of Babel URL.

Flow:
  Encode: seed phrase -> entropy -> babel string (memorizable)
  Decode: babel string -> entropy -> seed phrase -> Library of Babel URL
"""
from __future__ import annotations

from .bip39 import mnemonic_to_entropy, entropy_to_mnemonic
from .syllables import bytes_to_syllables, syllables_to_bytes, bytes_to_syllable_list
from .babel_lib import search_text, coordinates_to_url, get_page_content, format_page
from .story import entropy_to_story, story_to_entropy


def seed_to_babel(mnemonic: str) -> str:
    """
    Convert a 12-word BIP39 seed phrase to a pronounceable babel string.

    The babel string encodes the seed's entropy and can be used to recover
    both the seed phrase and its Library of Babel location.
    """
    entropy = mnemonic_to_entropy(mnemonic)
    return bytes_to_syllables(entropy)


def babel_to_seed(babel_string: str) -> str:
    """
    Convert a babel string back to a BIP39 seed phrase.
    """
    entropy = syllables_to_bytes(babel_string)
    return entropy_to_mnemonic(entropy)


def babel_to_url(babel_string: str) -> str:
    """
    Convert a babel string to a Library of Babel URL.

    The URL, when opened, displays a page containing the seed phrase.
    """
    # Decode babel string to seed phrase
    seed_phrase = babel_to_seed(babel_string)

    # Find Library of Babel coordinates for the seed phrase text
    hex_name, wall, shelf, volume, page = search_text(seed_phrase)

    # Generate URL
    return coordinates_to_url(hex_name, wall, shelf, volume, page)


def seed_to_url(mnemonic: str) -> str:
    """
    Convert a seed phrase directly to its Library of Babel URL.
    """
    hex_name, wall, shelf, volume, page = search_text(mnemonic)
    return coordinates_to_url(hex_name, wall, shelf, volume, page)


def seed_to_story(mnemonic: str) -> str:
    """
    Convert a seed phrase to a memorable story (4 vivid sentences).
    """
    entropy = mnemonic_to_entropy(mnemonic)
    return entropy_to_story(entropy)


def story_to_seed(story: str) -> str:
    """
    Convert a story back to a seed phrase.
    """
    entropy = story_to_entropy(story)
    return entropy_to_mnemonic(entropy)


def story_to_url(story: str) -> str:
    """
    Convert a story to a Library of Babel URL.
    """
    seed_phrase = story_to_seed(story)
    hex_name, wall, shelf, volume, page = search_text(seed_phrase)
    return coordinates_to_url(hex_name, wall, shelf, volume, page)


def story_to_page(story: str) -> str:
    """
    Convert a story to the Library of Babel page content (OFFLINE).

    Returns the formatted 3200-character page showing the seed phrase.
    """
    seed_phrase = story_to_seed(story)
    hex_name, wall, shelf, volume, page = search_text(seed_phrase)
    content = get_page_content(hex_name, wall, shelf, volume, page)
    return format_page(content)


def seed_to_page(mnemonic: str) -> str:
    """
    Convert a seed phrase to its Library of Babel page content (OFFLINE).
    """
    hex_name, wall, shelf, volume, page = search_text(mnemonic)
    content = get_page_content(hex_name, wall, shelf, volume, page)
    return format_page(content)


def get_babel_location(story: str) -> dict:
    """
    Get the Library of Babel location info for a story (OFFLINE).

    Returns dict with hex_name, wall, shelf, volume, page, url.
    """
    seed_phrase = story_to_seed(story)
    hex_name, wall, shelf, volume, page = search_text(seed_phrase)
    return {
        'hex_name': hex_name,
        'wall': wall,
        'shelf': shelf,
        'volume': volume,
        'page': page,
        'url': coordinates_to_url(hex_name, wall, shelf, volume, page),
        'seed_phrase': seed_phrase
    }


def format_babel_string(babel: str, chunk_size: int = 4) -> str:
    """
    Format a babel string for easier reading/memorization.

    Breaks into chunks: "aztulinerblinken" -> "aztu-line-rbli-nken"
    """
    chunks = [babel[i:i + chunk_size] for i in range(0, len(babel), chunk_size)]
    return '-'.join(chunks)


def format_as_sentences(mnemonic: str) -> str:
    """
    Format a seed phrase as memorable pseudo-sentences.

    Groups 16 syllables into 4 "sentences" of 4 syllables each,
    with 2 syllables per "word".

    Example output:
        "Augai zofug. Airoru rpaip. Ifalma ulpor. Erdex estal."
    """
    entropy = mnemonic_to_entropy(mnemonic)
    syllables = bytes_to_syllable_list(entropy)

    # Group into words (2 syllables each) and sentences (2 words each)
    sentences = []
    for i in range(0, len(syllables), 4):
        chunk = syllables[i:i + 4]
        if len(chunk) >= 4:
            word1 = chunk[0] + chunk[1]
            word2 = chunk[2] + chunk[3]
            sentence = f"{word1.capitalize()} {word2}."
        elif len(chunk) >= 2:
            word1 = chunk[0] + chunk[1] if len(chunk) > 1 else chunk[0]
            sentence = f"{word1.capitalize()}."
        else:
            sentence = f"{chunk[0].capitalize()}."
        sentences.append(sentence)

    return " ".join(sentences)
