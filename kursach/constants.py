BOOKS_UID = { # name : uid
    "A Bend in the Road": "0375430830",
    "1984": "8423328651",
    "Five Days in Paris": "0553474294",
    "Fahrenheit 451": "0345274318",
    "The Little Prince": "0152023984",
}

BOOKS = BOOKS_UID.keys()
BOOKS_LOWERED_UID = {name.lower(): uid for name, uid in BOOKS_UID.items()}
