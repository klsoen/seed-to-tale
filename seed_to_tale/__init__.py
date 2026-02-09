"""
Seed to Tale

Convert BIP39 seed phrases to memorable stories.
"""

from .converter import (
    seed_to_story, story_to_seed,
    seed_to_babel, babel_to_seed
)

__version__ = "0.1.0"
__all__ = ["seed_to_story", "story_to_seed", "seed_to_babel", "babel_to_seed"]
