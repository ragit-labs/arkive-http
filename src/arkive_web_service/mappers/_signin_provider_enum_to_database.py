from arkive_db.enums import SignInProvider
from arkive_web_service.enums import SignInProvider as SignInProviderEnum


def signin_provide_enum_to_database(enum: SignInProviderEnum) -> SignInProvider:
    if enum == SignInProviderEnum.GOOGLE:
        return SignInProvider.GOOGLE
    elif enum == SignInProviderEnum.WEBSITE:
        return SignInProvider.WEBSITE


__all__ = ["signin_provide_enum_to_database"]
