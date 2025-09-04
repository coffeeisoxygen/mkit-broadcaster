from argon2 import PasswordHasher, exceptions

from .intf_hasher import IPasswordHasher


class ArgonPasswordHasher(IPasswordHasher):
    def __init__(self):
        self._hasher = PasswordHasher()

    def hash(self, password: str) -> str:
        return self._hasher.hash(password)

    def verify(self, password: str, hashed: str) -> bool:
        try:
            return self._hasher.verify(hashed, password)
        except exceptions.VerifyMismatchError:
            return False
