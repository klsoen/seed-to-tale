# Seed to Tale

Convert BIP39 seed phrases to memorable 4-sentence stories.

## Concept

Instead of remembering 12 random words, remember a **4-sentence story** like:

> A settled lotus blinks in Paris.
> The southern tortoise opens in a warehouse.
> One sapphire gecko lingers in a throne room.
> My global star resumes in a greenhouse.

This story encodes the same 128-bit entropy as your seed phrase. You can convert the story back to your seed phrase anytime.

## How It Works

Each sentence encodes 32 bits using 4 word lists (256 words each = 8 bits):
- Adjective + Noun + Verb + Location
- 4 sentences × 32 bits = 128 bits = 12-word BIP39 seed

**Security is identical to BIP39** - same 2^128 possible combinations.

## Installation

```bash
pip install seed-to-tale
```

Or from source:

```bash
git clone https://github.com/klsoen/seed-to-tale.git
cd seed-to-tale
pip install -e .
```

## Usage

### Encode a Seed Phrase to a Story

```bash
seed-to-tale encode --story "voice clock able naive tonight decorate mule night spike miss network month"
```

Output:
```
A settled lotus blinks in Paris.
The southern tortoise opens in a warehouse.
One sapphire gecko lingers in a throne room.
My global star resumes in a greenhouse.
```

### Decode a Story to Seed Phrase

```bash
seed-to-tale decode --story --seed "A settled lotus blinks in Paris. The southern tortoise opens in a warehouse. One sapphire gecko lingers in a throne room. My global star resumes in a greenhouse."
```

Output:
```
voice clock able naive tonight decorate mule night spike miss network month
```

## Python API

```python
from seed_to_tale import seed_to_story, story_to_seed

# Encode seed to story
story = seed_to_story("voice clock able naive tonight decorate mule night spike miss network month")
print(story)

# Decode story back to seed
seed = story_to_seed(story)
print(seed)
```

## Comparison to Other Approaches

| Approach | How it works | Pros | Cons |
|----------|--------------|------|------|
| **BIP39** | 12 random words from 2048-word list | Standard, checksummed | Hard to memorize random words |
| **Stegoseed** | Hides BIP39 words in generated prose | BIP39 words visible, easy decode | Awkward text, words in plain sight |
| **Seed to Tale** | Re-encodes entropy into story structure | Natural sentences, original words hidden | Requires this tool to decode |

## Security Note

This tool does NOT add security. It encodes the same 128 bits in a different format. Treat your story with the same care as your seed phrase.

**Important:** The word lists are baked into this tool. If you lose access to the tool and only have your story, you need the exact same word lists to recover your seed.

## License

MIT
