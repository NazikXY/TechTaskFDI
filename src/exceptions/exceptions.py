
class CurrencyRequestException(Exception):
    def __init__(self, error: dict):
        self.error = error
