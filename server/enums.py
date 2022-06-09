from enum import Enum


# Plik zawierający enumy, identyczny jest w aplikacji klienckiej, dla zachowania kompatybilności i zachowania kontekstu,
# zamiast używania magicznych numerków, które nie wiadomo co oznaczają

class Color(Enum):
    """
    An enumeration.
    Options:
    white, black, red, green, blue, cyan, yellow, magenta
    """
    white = 0
    black = 1
    red = 2
    green = 3
    blue = 4
    cyan = 5
    yellow = 6
    magenta = 7
    default = 8


class Icon(Enum):
    """
    An enumeration.
    Options:
    car, home, holidays, education, health, fun, kids, gifts, other
    """
    car = 0
    home = 1
    holiday = 2
    education = 3
    health = 4
    fun = 5
    kids = 6
    gifts = 7
    other = 8


class Category(Enum):
    """
    An enumeration.
    Options:
    food_and_drink, shopping, accommodation, transport, car, entertainment, electronic, funding, investments, income, other
    """
    food_and_drink = 0
    shopping = 1
    accommodation = 2
    transport = 3
    car = 4
    entertainment = 5
    electronic = 6
    funding = 7
    investments = 8
    income = 9
    other = 10


class Period(Enum):
    """
    An enumeration.
    Options:
    none, daily, monthly, yearly
    """
    none = 0
    daily = 1
    monthly = 2
    yearly = 3
