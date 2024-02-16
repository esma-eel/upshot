import re


def get_password_pattern():
    password_pattern = (
        r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    )
    return password_pattern


def get_password_rules():
    return [
        "At least minimum 8 characters in length",
        "At least one uppercase English letter",
        "At least one lowercase English letter",
        "At least one digit",
        "At least one special character [#?!@$%^&*-]",
    ]


def check_password_strength(password):
    password_pattern = get_password_pattern()
    return re.match(password_pattern, password)


def are_passwords_same(password, repeat_password):
    return password == repeat_password
