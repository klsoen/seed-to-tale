"""
Story-based encoding: Convert entropy to memorable vivid sentences.

Uses 256-word lists (8 bits each) with 8 elements per sentence:
"A [QUALITY] [COLOR] [CREATURE] [ADVERB] [VERB] in a [PLACE_ADJ] [PLACE] near [LOCATION]."

2 sentences = 2 * 64 bits = 128 bits
"""
from __future__ import annotations

from typing import List

# 256 quality/mood adjectives (8 bits)
QUALITIES = [
    "fierce", "gentle", "ancient", "young", "wild", "tame", "brave", "shy",
    "clever", "foolish", "wise", "naive", "cunning", "honest", "sneaky", "loyal",
    "happy", "sad", "excited", "calm", "nervous", "proud", "bold", "timid",
    "hungry", "sleepy", "angry", "peaceful", "chaotic", "orderly", "lazy", "busy",
    "rich", "poor", "fancy", "plain", "elegant", "rustic", "modern", "vintage",
    "magic", "cursed", "blessed", "haunted", "enchanted", "hexed", "charmed", "doomed",
    "royal", "common", "noble", "peasant", "imperial", "tribal", "urban", "rural",
    "toxic", "healing", "deadly", "harmless", "potent", "weak", "supreme", "humble",
    "secret", "public", "hidden", "exposed", "buried", "floating", "sunken", "elevated",
    "quantum", "atomic", "cosmic", "stellar", "lunar", "solar", "astral", "ethereal",
    "digital", "analog", "virtual", "physical", "mental", "spiritual", "primal", "divine",
    "frozen", "burning", "melting", "boiling", "steaming", "chilling", "warming", "cooling",
    "silent", "roaring", "whispering", "screaming", "humming", "buzzing", "chirping", "howling",
    "fragile", "sturdy", "delicate", "robust", "brittle", "flexible", "rigid", "elastic",
    "mobile", "static", "portable", "fixed", "nomadic", "settled", "roaming", "rooted",
    "rapid", "slow", "instant", "eternal", "brief", "endless", "sudden", "gradual",
    "sweet", "bitter", "salty", "spicy", "sour", "smoky", "fresh", "stale",
    "smooth", "rough", "bumpy", "slick", "sticky", "fluffy", "crispy", "soggy",
    "heavy", "light", "dense", "airy", "massive", "petite", "bulky", "slim",
    "bright", "dim", "dazzling", "murky", "radiant", "gloomy", "luminous", "shadowy",
    "hot", "cold", "warm", "cool", "tepid", "scalding", "chilly", "mild",
    "tall", "short", "long", "wide", "narrow", "thick", "thin", "deep",
    "clean", "dirty", "pure", "tainted", "sterile", "filthy", "spotless", "grimy",
    "wet", "dry", "damp", "parched", "soaked", "arid", "moist", "dewy",
    "loud", "quiet", "noisy", "muted", "booming", "hushed", "thundering", "serene",
    "fast", "slow", "swift", "sluggish", "speedy", "leisurely", "hasty", "patient",
    "strong", "weak", "mighty", "feeble", "powerful", "frail", "invincible", "vulnerable",
    "smart", "dumb", "brilliant", "dim", "genius", "simple", "sharp", "dull",
    "kind", "cruel", "caring", "heartless", "loving", "hateful", "tender", "harsh",
    "true", "false", "real", "fake", "genuine", "phony", "authentic", "counterfeit",
    "free", "trapped", "wild", "caged", "liberated", "bound", "unleashed", "chained",
    "alive", "dead", "living", "undead", "mortal", "immortal", "eternal", "temporal",
]

# 256 color adjectives (8 bits)
COLORS = [
    "red", "blue", "green", "yellow", "orange", "purple", "pink", "brown",
    "black", "white", "gray", "silver", "gold", "bronze", "copper", "platinum",
    "crimson", "scarlet", "ruby", "cherry", "rose", "coral", "salmon", "peach",
    "azure", "cobalt", "navy", "sapphire", "sky", "teal", "turquoise", "cyan",
    "emerald", "jade", "lime", "olive", "mint", "forest", "moss", "sage",
    "lemon", "amber", "honey", "mustard", "canary", "butter", "cream", "ivory",
    "tangerine", "apricot", "rust", "terracotta", "ginger", "cinnamon", "caramel", "mahogany",
    "violet", "lavender", "plum", "grape", "orchid", "magenta", "fuchsia", "mauve",
    "blush", "flamingo", "bubblegum", "watermelon", "raspberry", "strawberry", "carnation", "rouge",
    "chocolate", "coffee", "mocha", "chestnut", "walnut", "hazel", "taupe", "beige",
    "charcoal", "slate", "ash", "smoke", "steel", "iron", "lead", "graphite",
    "pearl", "snow", "cloud", "chalk", "bone", "eggshell", "vanilla", "coconut",
    "sunset", "sunrise", "twilight", "midnight", "dawn", "dusk", "starlight", "moonlight",
    "neon", "electric", "fluorescent", "glowing", "iridescent", "prismatic", "holographic", "metallic",
    "pastel", "vivid", "muted", "faded", "saturated", "washed", "bleached", "dyed",
    "striped", "spotted", "checkered", "marbled", "speckled", "gradient", "ombre", "solid",
    "rainbow", "multicolor", "dichroic", "opalescent", "pearlescent", "shimmering", "sparkling", "glittering",
    "transparent", "translucent", "opaque", "clear", "foggy", "misty", "hazy", "crystalline",
    "fiery", "icy", "earthy", "watery", "airy", "stormy", "sunny", "shadowy",
    "dusty", "sandy", "muddy", "mossy", "rusty", "moldy", "frosty", "dewy",
    "bloody", "milky", "inky", "oily", "glossy", "matte", "satin", "velvet",
    "wine", "burgundy", "maroon", "oxblood", "brick", "auburn", "sienna", "umber",
    "aqua", "marine", "oceanic", "arctic", "tropical", "coastal", "lagoon", "reef",
    "jungle", "woodland", "meadow", "prairie", "desert", "volcanic", "glacial", "alpine",
    "royal", "imperial", "regal", "noble", "divine", "celestial", "cosmic", "mystic",
    "toxic", "nuclear", "radioactive", "chemical", "organic", "synthetic", "natural", "artificial",
    "ancient", "vintage", "antique", "retro", "modern", "futuristic", "timeless", "classic",
    "warm", "cool", "hot", "cold", "neutral", "earthy", "jeweled", "precious",
    "dark", "light", "deep", "pale", "rich", "soft", "bold", "subtle",
    "autumn", "winter", "spring", "summer", "seasonal", "evergreen", "deciduous", "perennial",
    "camouflage", "military", "industrial", "urban", "rural", "tribal", "ethnic", "folk",
    "plain", "patterned", "textured", "smooth", "rough", "woven", "printed", "embossed",
]

# 256 creatures/beings (8 bits)
CREATURES = [
    "dragon", "phoenix", "unicorn", "griffin", "pegasus", "hydra", "sphinx", "chimera",
    "wizard", "witch", "warlock", "sorcerer", "mage", "druid", "shaman", "necromancer",
    "knight", "samurai", "ninja", "viking", "gladiator", "spartan", "ronin", "paladin",
    "pirate", "captain", "admiral", "sailor", "corsair", "buccaneer", "privateer", "mariner",
    "king", "queen", "prince", "princess", "emperor", "empress", "sultan", "pharaoh",
    "elf", "dwarf", "goblin", "orc", "troll", "ogre", "gnome", "hobbit",
    "vampire", "werewolf", "zombie", "ghost", "specter", "wraith", "banshee", "phantom",
    "angel", "demon", "devil", "seraph", "cherub", "archangel", "imp", "succubus",
    "fairy", "pixie", "sprite", "nymph", "dryad", "naiad", "sylph", "leprechaun",
    "giant", "titan", "colossus", "cyclops", "minotaur", "centaur", "satyr", "gorgon",
    "mermaid", "siren", "kraken", "leviathan", "serpent", "wyrm", "basilisk", "cockatrice",
    "elephant", "lion", "tiger", "bear", "wolf", "fox", "leopard", "panther",
    "eagle", "hawk", "falcon", "owl", "raven", "crow", "vulture", "condor",
    "dolphin", "whale", "shark", "octopus", "squid", "jellyfish", "seahorse", "orca",
    "cobra", "python", "viper", "anaconda", "mamba", "rattlesnake", "boa", "asp",
    "crocodile", "alligator", "komodo", "iguana", "chameleon", "gecko", "tortoise", "turtle",
    "spider", "scorpion", "mantis", "beetle", "butterfly", "dragonfly", "firefly", "moth",
    "frog", "toad", "salamander", "newt", "axolotl", "tadpole", "gecko", "skink",
    "monkey", "gorilla", "chimpanzee", "orangutan", "baboon", "lemur", "gibbon", "mandrill",
    "penguin", "flamingo", "peacock", "swan", "crane", "heron", "pelican", "stork",
    "panda", "koala", "kangaroo", "platypus", "wombat", "sloth", "armadillo", "anteater",
    "robot", "android", "cyborg", "automaton", "golem", "construct", "sentinel", "mech",
    "alien", "martian", "xenomorph", "predator", "visitor", "invader", "colonist", "explorer",
    "chef", "artist", "musician", "dancer", "actor", "singer", "poet", "writer",
    "scientist", "professor", "doctor", "inventor", "alchemist", "astronaut", "engineer", "architect",
    "detective", "spy", "assassin", "thief", "rogue", "scout", "ranger", "hunter",
    "monk", "priest", "cleric", "bishop", "cardinal", "pope", "imam", "rabbi",
    "farmer", "shepherd", "fisherman", "miner", "blacksmith", "carpenter", "weaver", "potter",
    "merchant", "trader", "banker", "gambler", "smuggler", "dealer", "broker", "tycoon",
    "soldier", "general", "commander", "marshal", "warlord", "mercenary", "guardian", "sentinel",
    "prophet", "oracle", "seer", "mystic", "sage", "hermit", "pilgrim", "wanderer",
    "child", "elder", "ancestor", "descendant", "heir", "orphan", "prodigy", "savant",
]

# 256 adverbs (8 bits)
ADVERBS = [
    "silently", "loudly", "quietly", "noisily", "softly", "fiercely", "gently", "roughly",
    "quickly", "slowly", "rapidly", "gradually", "suddenly", "steadily", "hastily", "leisurely",
    "carefully", "carelessly", "cautiously", "recklessly", "skillfully", "clumsily", "gracefully", "awkwardly",
    "happily", "sadly", "angrily", "calmly", "nervously", "confidently", "shyly", "boldly",
    "wisely", "foolishly", "cleverly", "stupidly", "cunningly", "honestly", "sneakily", "openly",
    "bravely", "fearfully", "courageously", "timidly", "heroically", "cowardly", "valiantly", "meekly",
    "freely", "reluctantly", "willingly", "grudgingly", "eagerly", "hesitantly", "readily", "warily",
    "secretly", "publicly", "privately", "openly", "covertly", "overtly", "discreetly", "blatantly",
    "eternally", "briefly", "endlessly", "momentarily", "permanently", "temporarily", "constantly", "occasionally",
    "completely", "partially", "fully", "barely", "entirely", "slightly", "totally", "somewhat",
    "perfectly", "imperfectly", "flawlessly", "poorly", "excellently", "terribly", "brilliantly", "miserably",
    "magically", "naturally", "supernaturally", "miraculously", "mysteriously", "obviously", "strangely", "normally",
    "peacefully", "violently", "harmoniously", "chaotically", "serenely", "turbulently", "tranquilly", "wildly",
    "lovingly", "hatefully", "tenderly", "cruelly", "kindly", "harshly", "warmly", "coldly",
    "directly", "indirectly", "straightforwardly", "deviously", "honestly", "deceptively", "plainly", "obscurely",
    "simply", "complexly", "easily", "difficultly", "effortlessly", "laboriously", "smoothly", "roughly",
    "majestically", "humbly", "regally", "modestly", "grandly", "plainly", "elegantly", "crudely",
    "precisely", "vaguely", "accurately", "loosely", "exactly", "approximately", "specifically", "generally",
    "desperately", "casually", "urgently", "lazily", "frantically", "calmly", "anxiously", "relaxedly",
    "joyfully", "mournfully", "gleefully", "sorrowfully", "merrily", "gloomily", "cheerfully", "drearily",
    "powerfully", "weakly", "mightily", "feebly", "forcefully", "limply", "vigorously", "tiredly",
    "beautifully", "uglily", "gorgeously", "hideously", "prettily", "grotesquely", "charmingly", "repulsively",
    "clearly", "confusingly", "plainly", "obscurely", "distinctly", "vaguely", "sharply", "blurrily",
    "brightly", "dimly", "radiantly", "darkly", "luminously", "gloomily", "brilliantly", "dully",
    "deeply", "shallowly", "profoundly", "superficially", "intensely", "mildly", "extremely", "moderately",
    "truly", "falsely", "genuinely", "fakely", "authentically", "artificially", "sincerely", "insincerely",
    "rightfully", "wrongfully", "justly", "unjustly", "fairly", "unfairly", "legally", "illegally",
    "normally", "abnormally", "typically", "unusually", "commonly", "rarely", "frequently", "seldom",
    "intentionally", "accidentally", "deliberately", "randomly", "purposefully", "aimlessly", "methodically", "haphazardly",
    "independently", "dependently", "autonomously", "submissively", "freely", "obediently", "rebelliously", "loyally",
    "invisibly", "visibly", "imperceptibly", "noticeably", "subtly", "obviously", "faintly", "clearly",
    "infinitely", "finitely", "boundlessly", "limitedly", "endlessly", "restrictedly", "vastly", "narrowly",
]

# 256 action verbs (8 bits)
VERBS = [
    "dances", "sleeps", "dreams", "wakes", "rests", "meditates", "prays", "chants",
    "sings", "hums", "whistles", "shouts", "whispers", "screams", "laughs", "cries",
    "runs", "walks", "crawls", "leaps", "jumps", "skips", "hops", "sprints",
    "flies", "soars", "glides", "hovers", "floats", "drifts", "swoops", "dives",
    "swims", "wades", "splashes", "paddles", "surfs", "sails", "rows", "anchors",
    "climbs", "descends", "ascends", "falls", "rises", "drops", "plunges", "sinks",
    "hides", "seeks", "finds", "loses", "discovers", "explores", "searches", "hunts",
    "fights", "battles", "duels", "spars", "wrestles", "boxes", "fences", "jousts",
    "builds", "creates", "crafts", "forges", "constructs", "assembles", "designs", "invents",
    "breaks", "destroys", "smashes", "crushes", "shatters", "demolishes", "wrecks", "ruins",
    "heals", "cures", "mends", "repairs", "restores", "revives", "resurrects", "regenerates",
    "guards", "protects", "defends", "shields", "watches", "patrols", "secures", "fortifies",
    "attacks", "strikes", "charges", "ambushes", "raids", "invades", "assaults", "storms",
    "teaches", "learns", "studies", "reads", "writes", "draws", "paints", "sculpts",
    "cooks", "bakes", "brews", "roasts", "grills", "fries", "steams", "simmers",
    "eats", "drinks", "feasts", "devours", "savors", "tastes", "nibbles", "gulps",
    "grows", "blooms", "flowers", "withers", "sprouts", "roots", "branches", "fruits",
    "transforms", "changes", "morphs", "evolves", "mutates", "adapts", "shifts", "converts",
    "appears", "vanishes", "fades", "emerges", "materializes", "dissolves", "teleports", "phases",
    "glows", "shines", "sparkles", "glitters", "radiates", "illuminates", "blazes", "flickers",
    "burns", "freezes", "melts", "boils", "evaporates", "condenses", "crystallizes", "solidifies",
    "explodes", "implodes", "erupts", "detonates", "combusts", "ignites", "blasts", "bursts",
    "speaks", "talks", "converses", "discusses", "debates", "argues", "negotiates", "bargains",
    "listens", "hears", "eavesdrops", "overhears", "attends", "focuses", "concentrates", "ignores",
    "thinks", "ponders", "contemplates", "reflects", "considers", "analyzes", "calculates", "reasons",
    "remembers", "forgets", "recalls", "reminisces", "memorizes", "recollects", "recognizes", "identifies",
    "loves", "hates", "adores", "despises", "cherishes", "loathes", "admires", "envies",
    "hopes", "fears", "wishes", "dreads", "desires", "craves", "longs", "yearns",
    "wins", "loses", "triumphs", "fails", "succeeds", "conquers", "prevails", "surrenders",
    "leads", "follows", "guides", "trails", "commands", "obeys", "directs", "serves",
    "gives", "takes", "shares", "steals", "donates", "receives", "offers", "accepts",
    "waits", "rushes", "lingers", "hurries", "pauses", "continues", "stops", "proceeds",
]

# 256 place adjectives (8 bits)
PLACE_ADJS = [
    "ancient", "modern", "futuristic", "medieval", "prehistoric", "timeless", "eternal", "temporary",
    "hidden", "exposed", "secret", "public", "private", "open", "closed", "sealed",
    "sacred", "cursed", "blessed", "haunted", "enchanted", "mystical", "magical", "mundane",
    "grand", "humble", "majestic", "modest", "magnificent", "simple", "ornate", "plain",
    "dark", "bright", "dim", "radiant", "shadowy", "luminous", "gloomy", "sunny",
    "cold", "warm", "frozen", "burning", "icy", "fiery", "chilly", "tropical",
    "wet", "dry", "flooded", "parched", "damp", "arid", "misty", "dusty",
    "tall", "short", "towering", "low", "elevated", "sunken", "raised", "buried",
    "wide", "narrow", "vast", "tiny", "expansive", "cramped", "spacious", "compact",
    "empty", "crowded", "abandoned", "bustling", "deserted", "thriving", "desolate", "vibrant",
    "peaceful", "chaotic", "serene", "turbulent", "calm", "stormy", "tranquil", "violent",
    "beautiful", "ugly", "gorgeous", "hideous", "stunning", "dreadful", "lovely", "ghastly",
    "clean", "dirty", "pristine", "filthy", "spotless", "grimy", "pure", "polluted",
    "rich", "poor", "wealthy", "impoverished", "luxurious", "shabby", "opulent", "decrepit",
    "safe", "dangerous", "secure", "perilous", "protected", "hazardous", "guarded", "exposed",
    "famous", "unknown", "legendary", "obscure", "renowned", "forgotten", "celebrated", "neglected",
    "royal", "common", "imperial", "humble", "noble", "peasant", "regal", "ordinary",
    "holy", "unholy", "divine", "demonic", "celestial", "infernal", "heavenly", "hellish",
    "natural", "artificial", "organic", "synthetic", "wild", "cultivated", "untamed", "manicured",
    "living", "dead", "alive", "lifeless", "thriving", "decaying", "flourishing", "withering",
    "floating", "grounded", "airborne", "submerged", "suspended", "anchored", "drifting", "fixed",
    "visible", "invisible", "apparent", "hidden", "obvious", "concealed", "clear", "obscured",
    "solid", "hollow", "dense", "porous", "thick", "thin", "massive", "fragile",
    "colorful", "monochrome", "vibrant", "dull", "vivid", "faded", "brilliant", "muted",
    "noisy", "silent", "loud", "quiet", "thundering", "hushed", "roaring", "peaceful",
    "fragrant", "odorless", "aromatic", "stinking", "perfumed", "fetid", "sweet-smelling", "rank",
    "northern", "southern", "eastern", "western", "central", "outer", "inner", "remote",
    "coastal", "inland", "mountainous", "flat", "hilly", "valley", "plateau", "lowland",
    "urban", "rural", "suburban", "wilderness", "metropolitan", "pastoral", "industrial", "agricultural",
    "underwater", "underground", "aerial", "surface", "subterranean", "celestial", "terrestrial", "aquatic",
    "forbidden", "welcoming", "restricted", "accessible", "exclusive", "inclusive", "limited", "unlimited",
    "legendary", "ordinary", "mythical", "real", "fantastical", "mundane", "extraordinary", "commonplace",
]

# 256 place types (8 bits)
PLACES = [
    "temple", "shrine", "chapel", "cathedral", "mosque", "synagogue", "monastery", "pagoda",
    "castle", "palace", "fortress", "citadel", "stronghold", "keep", "manor", "estate",
    "tower", "spire", "lighthouse", "minaret", "obelisk", "monument", "pillar", "column",
    "cave", "cavern", "grotto", "tunnel", "mine", "burrow", "den", "lair",
    "forest", "jungle", "woods", "grove", "orchard", "thicket", "copse", "woodland",
    "mountain", "volcano", "peak", "summit", "cliff", "ridge", "canyon", "ravine",
    "river", "stream", "waterfall", "spring", "brook", "creek", "rapids", "delta",
    "lake", "pond", "lagoon", "reservoir", "pool", "oasis", "wetland", "marsh",
    "ocean", "sea", "bay", "gulf", "strait", "channel", "reef", "atoll",
    "island", "peninsula", "archipelago", "isthmus", "cape", "cove", "beach", "shore",
    "desert", "dune", "wasteland", "badlands", "prairie", "savanna", "steppe", "tundra",
    "garden", "park", "meadow", "field", "pasture", "lawn", "courtyard", "plaza",
    "city", "town", "village", "hamlet", "metropolis", "settlement", "outpost", "colony",
    "market", "bazaar", "mall", "arcade", "shop", "store", "boutique", "emporium",
    "library", "archive", "museum", "gallery", "theater", "arena", "stadium", "coliseum",
    "school", "academy", "university", "college", "institute", "laboratory", "observatory", "planetarium",
    "hospital", "clinic", "sanctuary", "asylum", "hospice", "infirmary", "dispensary", "pharmacy",
    "prison", "dungeon", "jail", "cell", "cage", "pit", "vault", "tomb",
    "factory", "workshop", "forge", "foundry", "mill", "refinery", "plant", "warehouse",
    "station", "terminal", "port", "harbor", "dock", "pier", "wharf", "marina",
    "bridge", "gate", "arch", "portal", "doorway", "threshold", "passage", "corridor",
    "hall", "chamber", "room", "cabin", "cottage", "hut", "tent", "shelter",
    "throne", "altar", "pedestal", "platform", "stage", "podium", "dais", "rostrum",
    "fountain", "well", "cistern", "aqueduct", "canal", "dam", "levee", "spillway",
    "statue", "sculpture", "carving", "relief", "frieze", "mosaic", "mural", "tapestry",
    "ruin", "remnant", "wreck", "debris", "rubble", "remains", "fossil", "artifact",
    "spaceship", "station", "satellite", "asteroid", "planet", "moon", "comet", "nebula",
    "dimension", "realm", "domain", "kingdom", "empire", "republic", "federation", "union",
    "battlefield", "warzone", "front", "border", "frontier", "boundary", "perimeter", "outskirts",
    "crossroads", "junction", "intersection", "fork", "roundabout", "bypass", "detour", "shortcut",
    "summit", "base", "camp", "headquarters", "bunker", "hideout", "refuge", "haven",
    "paradise", "utopia", "eden", "nirvana", "valhalla", "olympus", "elysium", "avalon",
]

# 256 specific locations (8 bits)
LOCATIONS = [
    "Tokyo", "Paris", "London", "Rome", "Berlin", "Madrid", "Vienna", "Prague",
    "Moscow", "Beijing", "Shanghai", "Seoul", "Bangkok", "Singapore", "Dubai", "Mumbai",
    "Cairo", "Marrakech", "Lagos", "Nairobi", "Johannesburg", "Casablanca", "Tunis", "Algiers",
    "Sydney", "Melbourne", "Auckland", "Wellington", "Fiji", "Tahiti", "Bali", "Manila",
    "New York", "Los Angeles", "Chicago", "Miami", "Boston", "Seattle", "Denver", "Austin",
    "Toronto", "Vancouver", "Montreal", "Quebec", "Ottawa", "Calgary", "Edmonton", "Winnipeg",
    "Mexico City", "Havana", "Lima", "Santiago", "Buenos Aires", "Bogota", "Caracas", "Quito",
    "Rio", "Sao Paulo", "Brasilia", "Salvador", "Recife", "Manaus", "Belem", "Fortaleza",
    "Athens", "Istanbul", "Jerusalem", "Baghdad", "Damascus", "Tehran", "Kabul", "Karachi",
    "Delhi", "Kolkata", "Chennai", "Bangalore", "Hyderabad", "Jaipur", "Varanasi", "Agra",
    "Kyoto", "Osaka", "Hiroshima", "Nagasaki", "Yokohama", "Sapporo", "Kobe", "Nara",
    "Venice", "Florence", "Milan", "Naples", "Pompeii", "Sicily", "Sardinia", "Tuscany",
    "Barcelona", "Seville", "Granada", "Valencia", "Bilbao", "Malaga", "Toledo", "Cordoba",
    "Amsterdam", "Brussels", "Antwerp", "Rotterdam", "Bruges", "Ghent", "Luxembourg", "Zurich",
    "Munich", "Hamburg", "Cologne", "Frankfurt", "Dresden", "Leipzig", "Heidelberg", "Salzburg",
    "Stockholm", "Copenhagen", "Oslo", "Helsinki", "Reykjavik", "Dublin", "Edinburgh", "Cardiff",
    "Warsaw", "Krakow", "Budapest", "Bucharest", "Sofia", "Belgrade", "Zagreb", "Ljubljana",
    "Lisbon", "Porto", "Madeira", "Azores", "Gibraltar", "Malta", "Cyprus", "Crete",
    "Alaska", "Hawaii", "Jamaica", "Bermuda", "Bahamas", "Barbados", "Trinidad", "Aruba",
    "Iceland", "Greenland", "Svalbard", "Faroe", "Lapland", "Siberia", "Mongolia", "Tibet",
    "Sahara", "Gobi", "Atacama", "Mojave", "Kalahari", "Outback", "Patagonia", "Antarctica",
    "Amazon", "Congo", "Borneo", "Madagascar", "Galapagos", "Tasmania", "Sumatra", "Java",
    "Himalayas", "Alps", "Andes", "Rockies", "Pyrenees", "Carpathians", "Urals", "Caucasus",
    "Nile", "Amazon", "Ganges", "Yangtze", "Mississippi", "Danube", "Rhine", "Volga",
    "Atlantis", "Lemuria", "Avalon", "Camelot", "Shangri-La", "El Dorado", "Xanadu", "Arcadia",
    "Narnia", "Hogwarts", "Mordor", "Rivendell", "Gotham", "Metropolis", "Wakanda", "Asgard",
    "Mars", "Venus", "Jupiter", "Saturn", "Neptune", "Pluto", "Mercury", "Uranus",
    "Alpha Centauri", "Andromeda", "Orion", "Sirius", "Proxima", "Kepler", "Trappist", "Betelgeuse",
    "Olympus", "Valhalla", "Hades", "Elysium", "Nirvana", "Shambhala", "Zion", "Eden",
    "Babylon", "Troy", "Carthage", "Sparta", "Thebes", "Memphis", "Persepolis", "Angkor",
    "Machu Picchu", "Petra", "Palmyra", "Timbuktu", "Samarkand", "Constantinople", "Alexandria", "Tenochtitlan",
    "Stonehenge", "Giza", "Easter Island", "Nazca", "Chichen Itza", "Tikal", "Mohenjo-daro", "Gobekli Tepe",
]

# Articles for variety
ARTICLES = ["A", "The"]


def entropy_to_story(entropy: bytes) -> str:
    """
    Convert 16 bytes (128 bits) of entropy to 2 memorable sentences.

    Each sentence uses 8 bytes (64 bits):
    - 1 byte for quality adjective
    - 1 byte for color adjective
    - 1 byte for creature
    - 1 byte for adverb
    - 1 byte for verb
    - 1 byte for place adjective
    - 1 byte for place type
    - 1 byte for location
    """
    if len(entropy) != 16:
        raise ValueError(f"Expected 16 bytes, got {len(entropy)}")

    sentences = []
    for i in range(2):
        base = i * 8
        quality_idx = entropy[base]
        color_idx = entropy[base + 1]
        creature_idx = entropy[base + 2]
        adverb_idx = entropy[base + 3]
        verb_idx = entropy[base + 4]
        place_adj_idx = entropy[base + 5]
        place_idx = entropy[base + 6]
        location_idx = entropy[base + 7]

        quality = QUALITIES[quality_idx]
        color = COLORS[color_idx]
        creature = CREATURES[creature_idx]
        adverb = ADVERBS[adverb_idx]
        verb = VERBS[verb_idx]
        place_adj = PLACE_ADJS[place_adj_idx]
        place = PLACES[place_idx]
        location = LOCATIONS[location_idx]

        article = ARTICLES[i]

        sentence = f"{article} {quality} {color} {creature} {adverb} {verb} in a {place_adj} {place} near {location}."
        sentences.append(sentence)

    return "\n".join(sentences)


def story_to_entropy(story: str) -> bytes:
    """
    Convert a story back to 16 bytes of entropy.
    """
    # Build reverse lookup dictionaries
    quality_to_idx = {w.lower(): i for i, w in enumerate(QUALITIES)}
    color_to_idx = {w.lower(): i for i, w in enumerate(COLORS)}
    creature_to_idx = {w.lower(): i for i, w in enumerate(CREATURES)}
    adverb_to_idx = {w.lower(): i for i, w in enumerate(ADVERBS)}
    verb_to_idx = {w.lower(): i for i, w in enumerate(VERBS)}
    place_adj_to_idx = {w.lower(): i for i, w in enumerate(PLACE_ADJS)}
    place_to_idx = {w.lower(): i for i, w in enumerate(PLACES)}
    location_to_idx = {w.lower(): i for i, w in enumerate(LOCATIONS)}

    # Parse sentences
    lines = [line.strip() for line in story.strip().split('\n') if line.strip()]
    if len(lines) != 2:
        # Try splitting by periods
        lines = [s.strip() for s in story.replace('\n', ' ').split('.') if s.strip()]

    if len(lines) != 2:
        raise ValueError(f"Expected 2 sentences, got {len(lines)}")

    entropy = []
    for line in lines:
        # Remove trailing period and lowercase
        line = line.rstrip('.').lower()
        words = line.split()

        # Find each element in order
        quality_idx = color_idx = creature_idx = adverb_idx = None
        verb_idx = place_adj_idx = place_idx = location_idx = None

        # Parse word by word
        for word in words:
            if word in quality_to_idx and quality_idx is None:
                quality_idx = quality_to_idx[word]
            elif word in color_to_idx and color_idx is None:
                color_idx = color_to_idx[word]
            elif word in creature_to_idx and creature_idx is None:
                creature_idx = creature_to_idx[word]
            elif word in adverb_to_idx and adverb_idx is None:
                adverb_idx = adverb_to_idx[word]
            elif word in verb_to_idx and verb_idx is None:
                verb_idx = verb_to_idx[word]
            elif word in place_adj_to_idx and place_adj_idx is None:
                place_adj_idx = place_adj_to_idx[word]
            elif word in place_to_idx and place_idx is None:
                place_idx = place_to_idx[word]

        # Location - check for matches (some have spaces, but our list doesn't)
        line_lower = line.lower()
        for loc in LOCATIONS:
            if loc.lower() in line_lower:
                location_idx = location_to_idx[loc.lower()]
                break

        missing = []
        if quality_idx is None: missing.append("quality")
        if color_idx is None: missing.append("color")
        if creature_idx is None: missing.append("creature")
        if adverb_idx is None: missing.append("adverb")
        if verb_idx is None: missing.append("verb")
        if place_adj_idx is None: missing.append("place_adj")
        if place_idx is None: missing.append("place")
        if location_idx is None: missing.append("location")

        if missing:
            raise ValueError(f"Could not parse sentence (missing: {', '.join(missing)}): {line}")

        entropy.extend([quality_idx, color_idx, creature_idx, adverb_idx,
                       verb_idx, place_adj_idx, place_idx, location_idx])

    return bytes(entropy)
