class RawNumberMatcher:
    regex = "^[0-9]+(\.\d+)?"

    def value(self, str):
        return float(str)
