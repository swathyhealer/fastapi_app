from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashFunctions:
    @staticmethod
    def bcrypt_hasher(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def bcrypt_hash_checker(password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)
