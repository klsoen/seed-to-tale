# Babel Bitcoin Password Decrypter

Convert BIP39 seed phrases to memorable stories that map to Library of Babel pages.

## Concept

Instead of remembering 12 random words, remember a **4-sentence story** like:

> A settled lotus blinks in Paris.
> The southern tortoise opens in a warehouse.
> One sapphire gecko lingers in a throne room.
> My global star resumes in a greenhouse.

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
A settled lotus blinks in Paris.
The southern tortoise opens in a warehouse.
One sapphire gecko lingers in a throne room.
My global star resumes in a greenhouse.
```

### Decode a Story to Library of Babel URL

```bash
babel-btc decode --story "A settled lotus blinks in Paris. The southern tortoise opens in a warehouse. One sapphire gecko lingers in a throne room. My global star resumes in a greenhouse."
```

Output:
```
https://libraryofbabel.info/book.cgi?5t62rny...-w1-s1-v01:1
```

### Decode a Story to Seed Phrase

```bash
babel-btc decode --story --seed "A settled lotus blinks in Paris. The southern tortoise opens in a warehouse. One sapphire gecko lingers in a throne room. My global star resumes in a greenhouse."
```

Output:
```
voice clock able naive tonight decorate mule night spike miss network month
```

### View Library of Babel Page Offline

No internet required! Display the full 3200-character Library of Babel page locally:

```bash
babel-btc decode --story --page "A settled lotus blinks in Paris. The southern tortoise opens in a warehouse. One sapphire gecko lingers in a throne room. My global star resumes in a greenhouse."
```

Output:
```
Seed phrase: voice clock able naive tonight decorate mule night spike miss network month

Library of Babel Location:
  Hex: 5t62rnyxmjc65t1058j11voju41dzu8gzvsbtjyo50b3c4h8m5...
  Wall: 1, Shelf: 1, Volume: 1, Page: 1

URL: https://libraryofbabel.info/book.cgi?...

================================================================================
PAGE CONTENT (3200 characters, 80x40):
================================================================================
voice clock able naive tonight decorate mule night spike miss network month
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

1. **Story Encoding**: Each sentence encodes 32 bits using word lists:
   - 256 adjectives (8 bits)
   - 256 nouns (8 bits)
   - 256 verbs (8 bits)
   - 256 locations (8 bits)
   - 4 sentences = 128 bits = 12-word BIP39 seed

2. **Library of Babel**: The algorithm computes the exact "hexagon" coordinates where your seed phrase appears in the Library of Babel's infinite collection.

3. **Offline Mode**: The Library of Babel algorithm is implemented locally, so you can verify your seed phrase appears on the correct page without any internet connection.

## Security Note

This tool does NOT add any security. It simply re-encodes the same entropy in a different format. Treat your story with the same security as your seed phrase.

## License

MIT
