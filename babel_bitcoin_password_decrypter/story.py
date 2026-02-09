"""
Story-based encoding: Convert entropy to memorable vivid sentences.

Uses 256-word lists (8 bits each) in a sentence structure:
"[Article] [Adjective] [Noun] [Verb] [Preposition] [Location]."

4 sentences = 4 * 32 bits = 128 bits
"""
from __future__ import annotations

from typing import List

# 256 vivid, distinct adjectives (8 bits)
ADJECTIVES = [
    "purple", "golden", "tiny", "giant", "ancient", "crystal", "silver", "frozen",
    "burning", "flying", "dancing", "sleeping", "hungry", "angry", "lazy", "brave",
    "cosmic", "electric", "magnetic", "radioactive", "invisible", "glowing", "shadow", "thunder",
    "velvet", "iron", "copper", "diamond", "rubber", "liquid", "foggy", "stormy",
    "sunny", "midnight", "crimson", "emerald", "sapphire", "amber", "ivory", "obsidian",
    "hollow", "solid", "twisted", "straight", "curved", "spiral", "zigzag", "circular",
    "silent", "roaring", "whispering", "screaming", "humming", "clicking", "buzzing", "chirping",
    "sweet", "bitter", "salty", "spicy", "sour", "smoky", "fresh", "rotten",
    "rapid", "slow", "instant", "eternal", "brief", "endless", "sudden", "gradual",
    "northern", "southern", "eastern", "western", "central", "outer", "inner", "upper",
    "smooth", "rough", "bumpy", "slick", "sticky", "fluffy", "crispy", "soggy",
    "happy", "sad", "excited", "calm", "nervous", "proud", "shy", "bold",
    "clever", "foolish", "wise", "naive", "cunning", "honest", "sneaky", "loyal",
    "wild", "tame", "fierce", "gentle", "savage", "peaceful", "chaotic", "orderly",
    "rich", "poor", "fancy", "plain", "elegant", "rustic", "modern", "vintage",
    "hot", "cold", "warm", "cool", "tepid", "scalding", "chilly", "mild",
    "bright", "dim", "dazzling", "murky", "radiant", "gloomy", "shiny", "matte",
    "heavy", "light", "dense", "hollow", "massive", "petite", "bulky", "slim",
    "young", "old", "newborn", "aged", "teenage", "mature", "infant", "elderly",
    "royal", "common", "noble", "peasant", "imperial", "tribal", "urban", "rural",
    "magic", "cursed", "blessed", "haunted", "enchanted", "hexed", "charmed", "jinxed",
    "metal", "wooden", "stone", "glass", "plastic", "paper", "cloth", "leather",
    "toxic", "healing", "deadly", "harmless", "potent", "weak", "supreme", "inferior",
    "secret", "public", "hidden", "exposed", "buried", "floating", "sunken", "elevated",
    "prime", "secondary", "tertiary", "final", "initial", "middle", "ultimate", "basic",
    "quantum", "atomic", "molecular", "cellular", "organic", "synthetic", "hybrid", "pure",
    "local", "global", "regional", "national", "continental", "planetary", "stellar", "galactic",
    "digital", "analog", "virtual", "physical", "mental", "spiritual", "emotional", "logical",
    "primary", "backup", "spare", "main", "auxiliary", "reserve", "surplus", "deficit",
    "positive", "negative", "neutral", "mixed", "balanced", "biased", "fair", "skewed",
    "mobile", "static", "portable", "fixed", "nomadic", "settled", "migratory", "rooted",
    "fragile", "sturdy", "delicate", "robust", "brittle", "flexible", "rigid", "elastic",
]

# 256 memorable nouns (8 bits)
NOUNS = [
    "elephant", "dragon", "robot", "wizard", "penguin", "dolphin", "tiger", "phoenix",
    "unicorn", "goblin", "pirate", "ninja", "samurai", "viking", "knight", "princess",
    "spaceship", "submarine", "helicopter", "bicycle", "skateboard", "rocket", "balloon", "train",
    "castle", "pyramid", "lighthouse", "windmill", "factory", "hospital", "library", "museum",
    "diamond", "emerald", "ruby", "pearl", "crystal", "meteor", "comet", "asteroid",
    "volcano", "glacier", "canyon", "waterfall", "mountain", "island", "desert", "jungle",
    "octopus", "jellyfish", "starfish", "seahorse", "whale", "shark", "turtle", "crab",
    "butterfly", "dragonfly", "firefly", "beetle", "spider", "scorpion", "mantis", "cricket",
    "eagle", "owl", "raven", "parrot", "flamingo", "peacock", "penguin", "toucan",
    "lion", "wolf", "fox", "bear", "panda", "koala", "monkey", "gorilla",
    "snake", "lizard", "crocodile", "chameleon", "gecko", "iguana", "cobra", "python",
    "frog", "toad", "salamander", "newt", "axolotl", "tadpole", "tortoise", "terrapin",
    "mushroom", "cactus", "bamboo", "bonsai", "orchid", "lotus", "sunflower", "rose",
    "pizza", "taco", "sushi", "burger", "donut", "pretzel", "waffle", "pancake",
    "guitar", "piano", "violin", "trumpet", "drum", "flute", "harp", "accordion",
    "telescope", "microscope", "compass", "hourglass", "sundial", "pendulum", "prism", "magnet",
    "sword", "shield", "bow", "spear", "hammer", "axe", "dagger", "staff",
    "crown", "throne", "scepter", "chalice", "amulet", "pendant", "ring", "bracelet",
    "book", "scroll", "map", "globe", "atlas", "diary", "journal", "grimoire",
    "candle", "lantern", "torch", "bonfire", "campfire", "fireplace", "furnace", "kiln",
    "clock", "calendar", "timer", "stopwatch", "metronome", "alarm", "bell", "gong",
    "mirror", "window", "door", "gate", "bridge", "tunnel", "ladder", "staircase",
    "cloud", "rainbow", "lightning", "snowflake", "raindrop", "hailstone", "tornado", "hurricane",
    "planet", "moon", "star", "sun", "galaxy", "nebula", "blackhole", "quasar",
    "atom", "molecule", "electron", "proton", "neutron", "photon", "quark", "neutrino",
    "ghost", "vampire", "zombie", "werewolf", "mummy", "skeleton", "demon", "angel",
    "fairy", "elf", "dwarf", "giant", "troll", "ogre", "centaur", "mermaid",
    "chef", "doctor", "pilot", "captain", "general", "professor", "detective", "inventor",
    "king", "queen", "prince", "emperor", "sultan", "pharaoh", "shogun", "chief",
    "baby", "child", "teenager", "adult", "elder", "grandma", "grandpa", "ancestor",
    "cat", "dog", "hamster", "rabbit", "parrot", "goldfish", "ferret", "hedgehog",
    "ant", "bee", "wasp", "moth", "fly", "mosquito", "ladybug", "grasshopper",
]

# 256 action verbs (8 bits)
VERBS = [
    "dances", "sleeps", "jumps", "flies", "swims", "runs", "walks", "crawls",
    "sings", "shouts", "whispers", "laughs", "cries", "snores", "hums", "yells",
    "eats", "drinks", "cooks", "bakes", "fries", "grills", "roasts", "steams",
    "builds", "breaks", "fixes", "creates", "destroys", "repairs", "crafts", "forges",
    "hides", "seeks", "finds", "loses", "discovers", "explores", "investigates", "searches",
    "teaches", "learns", "studies", "reads", "writes", "draws", "paints", "sculpts",
    "fights", "defends", "attacks", "retreats", "surrenders", "conquers", "invades", "liberates",
    "grows", "shrinks", "expands", "contracts", "stretches", "compresses", "inflates", "deflates",
    "rises", "falls", "floats", "sinks", "hovers", "glides", "soars", "plummets",
    "opens", "closes", "locks", "unlocks", "seals", "breaks", "enters", "exits",
    "starts", "stops", "pauses", "resumes", "continues", "repeats", "restarts", "finishes",
    "appears", "vanishes", "fades", "emerges", "dissolves", "materializes", "teleports", "transforms",
    "spins", "twirls", "rotates", "revolves", "orbits", "spirals", "zigzags", "bounces",
    "glows", "sparkles", "shimmers", "flashes", "blinks", "radiates", "illuminates", "dims",
    "burns", "freezes", "melts", "boils", "evaporates", "condenses", "crystallizes", "petrifies",
    "explodes", "implodes", "erupts", "collapses", "shatters", "crumbles", "disintegrates", "reconstructs",
    "thinks", "dreams", "imagines", "remembers", "forgets", "realizes", "understands", "wonders",
    "loves", "hates", "fears", "desires", "envies", "admires", "respects", "ignores",
    "helps", "hurts", "heals", "harms", "saves", "dooms", "protects", "endangers",
    "gives", "takes", "shares", "steals", "borrows", "lends", "donates", "receives",
    "wins", "loses", "ties", "competes", "cooperates", "challenges", "surrenders", "triumphs",
    "waits", "rushes", "delays", "hurries", "lingers", "dawdles", "hastens", "stalls",
    "arrives", "departs", "returns", "leaves", "stays", "visits", "travels", "migrates",
    "climbs", "descends", "ascends", "drops", "lifts", "raises", "lowers", "elevates",
    "pulls", "pushes", "drags", "carries", "throws", "catches", "tosses", "hurls",
    "bends", "straightens", "twists", "curves", "folds", "unfolds", "wraps", "unwraps",
    "fills", "empties", "pours", "spills", "drains", "floods", "overflows", "dries",
    "connects", "disconnects", "links", "separates", "joins", "splits", "merges", "divides",
    "attracts", "repels", "pulls", "pushes", "draws", "drives", "lures", "chases",
    "guards", "watches", "monitors", "patrols", "scouts", "surveys", "inspects", "examines",
    "collects", "scatters", "gathers", "disperses", "accumulates", "distributes", "hoards", "shares",
    "celebrates", "mourns", "parties", "grieves", "rejoices", "laments", "cheers", "weeps",
]

# 256 locations (8 bits)
LOCATIONS = [
    "Tokyo", "Paris", "Mars", "Atlantis", "Narnia", "Mordor", "Gotham", "Hogwarts",
    "Egypt", "Alaska", "Hawaii", "Iceland", "Brazil", "Kenya", "India", "China",
    "the moon", "the sun", "Jupiter", "Saturn", "Neptune", "Pluto", "Venus", "Mercury",
    "a volcano", "a glacier", "a canyon", "a cave", "a forest", "a desert", "a swamp", "an island",
    "the sky", "the ocean", "the clouds", "the stars", "space", "the void", "heaven", "limbo",
    "a castle", "a dungeon", "a tower", "a palace", "a fortress", "a temple", "a shrine", "a tomb",
    "a kitchen", "a bedroom", "a bathroom", "a basement", "an attic", "a garage", "a closet", "a hallway",
    "a school", "a hospital", "a prison", "a library", "a museum", "a theater", "a stadium", "an arena",
    "a garden", "a park", "a zoo", "a farm", "a ranch", "a vineyard", "an orchard", "a greenhouse",
    "a bridge", "a tunnel", "a highway", "a railroad", "an airport", "a harbor", "a dock", "a pier",
    "a mountain", "a valley", "a plateau", "a cliff", "a beach", "a shore", "a riverbank", "a lakeside",
    "a rainforest", "a tundra", "a savanna", "a prairie", "a meadow", "a marsh", "a bog", "a fen",
    "underwater", "underground", "midair", "outer space", "another dimension", "the future", "the past", "nowhere",
    "a restaurant", "a cafe", "a bar", "a bakery", "a market", "a mall", "a shop", "a store",
    "a lab", "a factory", "a warehouse", "a workshop", "a studio", "an office", "a clinic", "a pharmacy",
    "a church", "a mosque", "a synagogue", "a monastery", "a chapel", "a cathedral", "a pagoda", "a shrine",
    "a circus", "a carnival", "a fair", "a festival", "a parade", "a concert", "a party", "a wedding",
    "a battlefield", "a graveyard", "a memorial", "a monument", "a statue", "a fountain", "a plaza", "a square",
    "a rooftop", "a balcony", "a patio", "a deck", "a porch", "a terrace", "a courtyard", "a garden",
    "a spaceship", "a submarine", "a helicopter", "a hot air balloon", "a train", "a bus", "a taxi", "a limousine",
    "a treehouse", "a cabin", "a cottage", "a mansion", "a hut", "a tent", "an igloo", "a yurt",
    "a planet", "a comet", "an asteroid", "a nebula", "a galaxy", "a black hole", "a wormhole", "a supernova",
    "a dream", "a nightmare", "a memory", "a vision", "an illusion", "a simulation", "a hologram", "a mirage",
    "a mirror world", "a parallel universe", "an alternate timeline", "a pocket dimension", "the astral plane", "the shadow realm", "the spirit world", "the underworld",
    "Wonderland", "Oz", "Neverland", "El Dorado", "Shangri-La", "Camelot", "Valhalla", "Olympus",
    "New York", "London", "Rome", "Berlin", "Moscow", "Sydney", "Dubai", "Singapore",
    "a battlefield", "a throne room", "a treasure vault", "a dragon's lair", "a wizard's tower", "a pirate ship", "a haunted house", "a secret base",
    "the North Pole", "the South Pole", "the equator", "the tropics", "the arctic", "the antarctic", "the bermuda triangle", "area 51",
    "a black market", "a secret society", "a hidden temple", "a lost city", "a forgotten realm", "a forbidden zone", "a restricted area", "a no man's land",
    "a rainbow", "a storm cloud", "a lightning bolt", "a sunbeam", "a moonbeam", "a starlight", "an aurora", "a twilight zone",
    "infinity", "eternity", "oblivion", "paradise", "purgatory", "chaos", "order", "balance",
    "your imagination", "my dreams", "their memories", "our future", "his past", "her destiny", "its origin", "the unknown",
]

# Articles/starters for variety
ARTICLES = ["A", "The", "One", "My", "Your", "Their", "Some", "That"]


def entropy_to_story(entropy: bytes) -> str:
    """
    Convert 16 bytes (128 bits) of entropy to 4 memorable sentences.

    Each sentence uses 4 bytes (32 bits):
    - 1 byte for adjective
    - 1 byte for noun
    - 1 byte for verb
    - 1 byte for location
    """
    if len(entropy) != 16:
        raise ValueError(f"Expected 16 bytes, got {len(entropy)}")

    sentences = []
    for i in range(4):
        base = i * 4
        adj_idx = entropy[base]
        noun_idx = entropy[base + 1]
        verb_idx = entropy[base + 2]
        loc_idx = entropy[base + 3]

        adj = ADJECTIVES[adj_idx]
        noun = NOUNS[noun_idx]
        verb = VERBS[verb_idx]
        loc = LOCATIONS[loc_idx]

        # Vary the article based on sentence number
        article = ARTICLES[i % len(ARTICLES)]

        sentence = f"{article} {adj} {noun} {verb} in {loc}."
        sentences.append(sentence)

    return "\n".join(sentences)


def story_to_entropy(story: str) -> bytes:
    """
    Convert a story back to 16 bytes of entropy.
    """
    # Build reverse lookup dictionaries
    adj_to_idx = {adj.lower(): i for i, adj in enumerate(ADJECTIVES)}
    noun_to_idx = {noun.lower(): i for i, noun in enumerate(NOUNS)}
    verb_to_idx = {verb.lower(): i for i, verb in enumerate(VERBS)}
    loc_to_idx = {loc.lower(): i for i, loc in enumerate(LOCATIONS)}

    # Parse sentences
    lines = [line.strip() for line in story.strip().split('\n') if line.strip()]
    if len(lines) != 4:
        # Try splitting by periods
        lines = [s.strip() for s in story.replace('\n', ' ').split('.') if s.strip()]

    if len(lines) != 4:
        raise ValueError(f"Expected 4 sentences, got {len(lines)}")

    entropy = []
    for line in lines:
        # Remove trailing period and lowercase
        line = line.rstrip('.').lower()
        words = line.split()

        # Find adjective, noun, verb, location
        adj_idx = noun_idx = verb_idx = loc_idx = None

        for word in words:
            if word in adj_to_idx and adj_idx is None:
                adj_idx = adj_to_idx[word]
            elif word in noun_to_idx and noun_idx is None:
                noun_idx = noun_to_idx[word]
            elif word in verb_to_idx and verb_idx is None:
                verb_idx = verb_to_idx[word]

        # Location is trickier - check multi-word locations
        line_lower = line.lower()
        for loc in LOCATIONS:
            if loc.lower() in line_lower:
                loc_idx = loc_to_idx[loc.lower()]
                break

        if None in [adj_idx, noun_idx, verb_idx, loc_idx]:
            raise ValueError(f"Could not parse sentence: {line}")

        entropy.extend([adj_idx, noun_idx, verb_idx, loc_idx])

    return bytes(entropy)
