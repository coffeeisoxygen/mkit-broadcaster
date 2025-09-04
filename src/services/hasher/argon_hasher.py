from argon2 import PasswordHasher, exceptions
from loguru import logger

from .intf_hasher import IPasswordHasher


class ArgonPasswordHasher(IPasswordHasher):
    def __init__(self):
        self._hasher = PasswordHasher()

    def hash(self, password: str) -> str:
        logger.debug("Hashing password with Argon2.")
        hashed = self._hasher.hash(password)
        logger.debug("Password hashed successfully.")
        return hashed

    def verify(self, hashed: str, password: str) -> bool:
        logger.debug("Verifying password with Argon2.")
        try:
            result = self._hasher.verify(hashed, password)
            logger.debug("Password verification result: {}", result)
            return result
        except exceptions.VerifyMismatchError:
            logger.warning("Password verification failed: mismatch.")
            return False
