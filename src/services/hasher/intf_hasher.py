from abc import ABC, abstractmethod


class IPasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        """Hash a plain password."""
        pass

    @abstractmethod
    def verify(self, hashed: str, password: str) -> bool:
        """Verify a plain password against a hash."""
        pass
