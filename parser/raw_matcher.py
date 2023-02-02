from decimal import Decimal


class RawNumberMatcher:
    regex = "^[0-9]+(\.\d+)?"

    def value(self, str):
        return Decimal(str)


class RawStringMatcher:
    regex = "^\"[a-zA-Z0-9,_]+\""

    def value(self, str):
        return str[1:][:-1]
