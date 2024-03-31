from enum import Enum, unique, auto


@unique
class SignInProvider(str, Enum):
    GOOGLE = auto()
    WEBSITE = auto()
