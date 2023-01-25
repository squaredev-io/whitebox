import bcrypt


def to_utf8(ps):
    return ps.encode("utf-8")


def hash_password(password):
    return bcrypt.hashpw(to_utf8(password), bcrypt.gensalt()).decode("utf8")


def passwords_match(hashed_password, password):
    return bcrypt.checkpw(to_utf8(password), to_utf8(hashed_password))
