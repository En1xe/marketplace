from enum import Enum


class VerificationCodesOperationTypes(str, Enum):
    CHANGE_PASSWORD = 'change_password'
    CHANGE_EMAIL = 'change_email'
    VERIFICATION = 'verification'
    