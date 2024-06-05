import bcrypt


def get_hashed_pwd(plain_pwd: str) -> bytes:
    pwd = plain_pwd.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd, salt)


def verify_pwd(plain_pwd: str, hashed_pwd: bytes):
    pwd = plain_pwd.encode("utf-8")
    return bcrypt.checkpw(pwd, hashed_pwd)
