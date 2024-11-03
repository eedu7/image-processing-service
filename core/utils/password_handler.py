from passlib.hash import argon2


class PasswordHandler:
    @staticmethod
    def hash_password(password: str) -> str:
        hashed_password = argon2.hash(password)
        return hashed_password

    @staticmethod
    def verify_password(stored_hashed_password: str, password: str) -> bool:
        return argon2.verify(password, stored_hashed_password)
