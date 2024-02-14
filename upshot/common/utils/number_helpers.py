import re


def ir_phone_number(value):
    pattern = r"(((0?9)|(\+?989))\d{9})"
    return bool(re.match(pattern, value))
