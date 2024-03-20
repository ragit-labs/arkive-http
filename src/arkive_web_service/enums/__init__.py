from enum import Enum, unique, auto


@unique
class SignInProvider(Enum):
    GOOGLE = auto()
    WEBSITE = auto()


__all__ = ["SignInProvider"]
