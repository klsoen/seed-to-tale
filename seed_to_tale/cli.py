"""
Command-line interface for babel-bitcoin-password-decrypter.
"""

import argparse
import sys

from .converter import (
    seed_to_babel, babel_to_seed, babel_to_url, seed_to_url,
    format_babel_string, format_as_sentences,
    seed_to_story, story_to_seed, story_to_url,
    story_to_page, seed_to_page, get_babel_location
)


def main():
    parser = argparse.ArgumentParser(
        description="Convert BIP39 seed phrases to memorable stories and Library of Babel URLs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert seed phrase to a memorable story (RECOMMENDED)
  babel-btc encode --story "your twelve word seed phrase here"

  # Convert story back to Library of Babel URL
  babel-btc decode --story "A purple elephant dances in Tokyo..."

  # Convert seed phrase to syllable string
  babel-btc encode "abandon abandon ... about"

  # Show seed phrase from story
  babel-btc decode --story --seed "A purple elephant..."
        """
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Encode command
    encode_parser = subparsers.add_parser(
        'encode',
        help='Convert a seed phrase to a memorable format'
    )
    encode_parser.add_argument(
        'seed_phrase',
        help='12-word BIP39 seed phrase (in quotes)'
    )
    encode_parser.add_argument(
        '--story',
        action='store_true',
        help='Output as memorable story (4 vivid sentences) - RECOMMENDED'
    )
    encode_parser.add_argument(
        '--format', '-f',
        action='store_true',
        help='Format syllable output with hyphens'
    )
    encode_parser.add_argument(
        '--url', '-u',
        action='store_true',
        help='Also output the Library of Babel URL'
    )

    # Decode command
    decode_parser = subparsers.add_parser(
        'decode',
        help='Convert a story/babel string to Library of Babel URL'
    )
    decode_parser.add_argument(
        'input',
        help='The story or babel string to decode'
    )
    decode_parser.add_argument(
        '--story',
        action='store_true',
        help='Input is a story (4 sentences)'
    )
    decode_parser.add_argument(
        '--seed', '-s',
        action='store_true',
        help='Output seed phrase instead of URL'
    )
    decode_parser.add_argument(
        '--page', '-p',
        action='store_true',
        help='Show Library of Babel page content (OFFLINE - no internet required)'
    )

    args = parser.parse_args()

    try:
        if args.command == 'encode':
            if args.story:
                print(seed_to_story(args.seed_phrase))
            else:
                babel = seed_to_babel(args.seed_phrase)
                if args.format:
                    print(format_babel_string(babel))
                else:
                    print(babel)

            if args.url:
                url = seed_to_url(args.seed_phrase)
                print(f"\nLibrary of Babel URL:\n{url}")

        elif args.command == 'decode':
            if args.story:
                if args.seed:
                    seed = story_to_seed(args.input)
                    print(seed)
                elif args.page:
                    # Show full Library of Babel page (offline)
                    location = get_babel_location(args.input)
                    print(f"Seed phrase: {location['seed_phrase']}")
                    print(f"\nLibrary of Babel Location:")
                    print(f"  Hex: {location['hex_name'][:50]}...")
                    print(f"  Wall: {location['wall']}, Shelf: {location['shelf']}, Volume: {location['volume']}, Page: {location['page']}")
                    print(f"\nURL: {location['url']}")
                    print(f"\n{'='*80}")
                    print("PAGE CONTENT (3200 characters, 80×40):")
                    print('='*80)
                    page_content = story_to_page(args.input)
                    print(page_content)
                else:
                    url = story_to_url(args.input)
                    print(url)
            else:
                # Syllable mode - remove formatting
                clean_babel = args.input.replace('-', '').replace(' ', '').replace('.', '').lower()
                if args.seed:
                    seed = babel_to_seed(clean_babel)
                    print(seed)
                elif args.page:
                    # Show full Library of Babel page (offline)
                    seed = babel_to_seed(clean_babel)
                    print(f"Seed phrase: {seed}")
                    print(f"\n{'='*80}")
                    print("PAGE CONTENT (3200 characters, 80×40):")
                    print('='*80)
                    page_content = seed_to_page(seed)
                    print(page_content)
                else:
                    url = babel_to_url(clean_babel)
                    print(url)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
