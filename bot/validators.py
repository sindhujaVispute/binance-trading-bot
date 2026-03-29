from bot.exceptions import ValidationError

VALID_SIDES = {"BUY", "SELL"}
VALID_TYPES = {"MARKET", "LIMIT", "STOP_LIMIT"}

def validate_order(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    if not symbol.isalnum():
        raise ValidationError("Invalid symbol format")

    if side not in VALID_SIDES:
        raise ValidationError("Side must be BUY or SELL")

    if order_type not in VALID_TYPES:
        raise ValidationError("Invalid order type")

    if quantity <= 0:
        raise ValidationError("Quantity must be > 0")

    if order_type in {"LIMIT", "STOP_LIMIT"} and price is None:
        raise ValidationError("Price required for LIMIT/STOP_LIMIT")