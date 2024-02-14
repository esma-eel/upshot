import random
import string
import secrets
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def generate_from_chars(chars, length):
    result = "".join(random.choice(chars) for _ in range(length))
    return result


def generate_number(length):
    result = generate_from_chars(string.digits, length)
    return result


def generate_string_lc(length):
    result = generate_from_chars(string.ascii_lowercase, length)
    return result


def generate_string_uc(length):
    result = generate_from_chars(string.ascii_uppercase, length)
    return result


def generate_urlsafe_token(length):
    result = secrets.token_urlsafe(length)
    return result


def generate_hex_token(length):
    result = secrets.token_hex(length)
    return result


class PasswordResetTokenGeneratorByProfileEmail(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        login_timestamp = (
            ""
            if user.last_login is None
            else user.last_login.replace(microsecond=0, tzinfo=None)
        )
        email = user.profile.get_primary_email()
        return f"{user.pk}{user.password}{login_timestamp}{timestamp}{email}"


default_token_generator = PasswordResetTokenGeneratorByProfileEmail()
