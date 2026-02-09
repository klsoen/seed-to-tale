# Babel Bitcoin Password Decrypter

Convert BIP39 seed phrases to memorable stories that map to Library of Babel pages.

## Concept

Instead of remembering 12 random words, remember a **2-sentence story** like:

> A bound dusk squid loudly destroys in a lovely island near Cologne.
> The elegant steel golem wrongfully hates in a vibrant badlands near Karachi.

This story encodes the same 128-bit entropy as your seed phrase. You can:
1. Convert the story back to your seed phrase
2. Get a Library of Babel URL where your seed phrase appears
3. View the Library of Babel page **offline** (no internet required)

## Installation

```bash
pip install babel-bitcoin-password-decrypter
```

Or with Poetry:

```bash
git clone https://github.com/klsoen/babel-bitcoin-password-decrypter.git
cd babel-bitcoin-password-decrypter
poetry install
```

## Usage

### Encode a Seed Phrase to a Story (Recommended)

```bash
babel-btc encode --story "voice clock able naive tonight decorate mule night spike miss network month"
```

Output:
```
A bound dusk squid loudly destroys in a lovely island near Cologne.
The elegant steel golem wrongfully hates in a vibrant badlands near Karachi.
```

### Decode a Story to Library of Babel URL

```bash
babel-btc decode --story "A bound dusk squid loudly destroys in a lovely island near Cologne. The elegant steel golem wrongfully hates in a vibrant badlands near Karachi."
```

Output:
```
https://libraryofbabel.info/book.cgi?5t62rny...-w1-s1-v01:1
```

### Decode a Story to Seed Phrase

```bash
babel-btc decode --story --seed "A bound dusk squid loudly destroys in a lovely island near Cologne. The elegant steel golem wrongfully hates in a vibrant badlands near Karachi."
```

Output:
```
voice clock able naive tonight decorate mule night spike miss network month
```

### View Library of Babel Page Offline

No internet required! Display the full 3200-character Library of Babel page locally:

```bash
babel-btc decode --story --page "A bound dusk squid loudly destroys in a lovely island near Cologne. The elegant steel golem wrongfully hates in a vibrant badlands near Karachi."
```

Output:
```
Seed phrase: voice clock able naive tonight decorate mule night spike miss network month

Library of Babel Location:
  Hex: 5t62rny...
  Wall: 1, Shelf: 1, Volume: 1, Page: 1

URL: https://libraryofbabel.info/book.cgi?...

================================================================================
PAGE CONTENT (3200 characters, 80x40):
================================================================================
voice clock able naive tonight decorate mule night spike miss network month
[... rest of page is spaces ...]
```

### Alternative: Syllable Encoding

If you prefer syllable-based encoding instead of stories:

```bash
# Encode to syllables
babel-btc encode "your twelve word seed phrase here"

# With formatting
babel-btc encode --format "your twelve word seed phrase here"

# Decode syllables
babel-btc decode "abebeiabebeiabebeiabebeiabebeiabebeiabebeiabebeiabebeiabebeiabebeiaibelt"
```

## Python API

```python
from babel_bitcoin_password_decrypter import (
    seed_to_story, story_to_seed, story_to_url,
    story_to_page, get_babel_location,
    seed_to_babel, babel_to_seed
)

# Encode seed to memorable story
story = seed_to_story("voice clock able naive tonight decorate mule night spike miss network month")
print(story)

# Decode story back to seed
seed = story_to_seed(story)
print(seed)

# Get Library of Babel URL
url = story_to_url(story)
print(url)

# Get page content offline
page = story_to_page(story)
print(page)

# Get full location info
location = get_babel_location(story)
print(location['hex_name'], location['wall'], location['shelf'], location['volume'], location['page'])
```

## How It Works

1. **Story Encoding**: Each sentence encodes 64 bits using 8 word lists:
   - 256 quality adjectives (8 bits) - fierce, gentle, ancient...
   - 256 color adjectives (8 bits) - crimson, azure, golden...
   - 256 creatures (8 bits) - dragon, wizard, phoenix...
   - 256 adverbs (8 bits) - silently, boldly, gracefully...
   - 256 verbs (8 bits) - dances, guards, transforms...
   - 256 place adjectives (8 bits) - hidden, ancient, sacred...
   - 256 place types (8 bits) - temple, fortress, volcano...
   - 256 locations (8 bits) - Tokyo, Atlantis, Mars...
   - **2 sentences = 128 bits = 12-word BIP39 seed**

2. **Library of Babel**: The algorithm computes the exact "hexagon" coordinates where your seed phrase appears in the Library of Babel's infinite collection.

3. **Offline Mode**: The Library of Babel algorithm is implemented locally, so you can verify your seed phrase appears on the correct page without any internet connection.

## Security Note

This tool does NOT add any security. It simply re-encodes the same entropy in a different format. Treat your story with the same security as your seed phrase.

## License

MIT
