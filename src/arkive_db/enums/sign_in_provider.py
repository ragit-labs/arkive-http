from enum import Enum, auto, unique


@unique
class SignInProvider(str, Enum):
    GOOGLE = auto()
    WEBSITE = auto()
