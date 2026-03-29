class TradingBotException(Exception):
    pass

class ValidationError(TradingBotException):
    pass

class APIError(TradingBotException):
    pass