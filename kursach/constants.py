BOOKS_UID = { # name : uid
    'My': "123"
}

BOOKS = BOOKS_UID.keys()
BOOKS_LOWERED_UID = {name.lower(): uid for name, uid in BOOKS_UID.items()}
