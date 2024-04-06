from enum import Enum, auto, unique


@unique
class SignInProvider(Enum):
    GOOGLE = auto()
    WEBSITE = auto()


__all__ = ["SignInProvider"]
