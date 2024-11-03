from passlib.hash import argon2



def hash_password(password: str) -> str:
    hashed_password = argon2.hash(password)
    return hashed_password

def verify_password(stored_hashed_password: str, password: str) -> bool:
    return argon2.verify(password, stored_hashed_password)


