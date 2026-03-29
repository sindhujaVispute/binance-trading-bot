from typing import Dict, Any
import logging

from bot.client import BinanceClient
from bot.validators import validate_order
from bot.exceptions import TradingBotException

logger = logging.getLogger(__name__)

class OrderService:
    def __init__(self, dry_run: bool = False):
        self.client = BinanceClient()
        self.dry_run = dry_run

    def create_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float = None
    ) -> Dict[str, Any]:

        try:
            # Normalize input
            symbol = symbol.upper()
            side = side.upper()
            order_type = order_type.upper()

            # Validate input
            validate_order(symbol, side, order_type, quantity, price)

            params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity
            }

            if order_type == "LIMIT":
                params.update({
                    "price": price,
                    "timeInForce": "GTC"
                })

            if order_type == "STOP_LIMIT":
                stop_price = price * 0.99 if side == "BUY" else price * 1.01
                params.update({
                    "price": price,
                    "stopPrice": stop_price,
                    "timeInForce": "GTC"
                })

            logger.info(f"Order request: {params}")

            if self.dry_run:
                logger.info("Dry run enabled — order not sent")
                return {
                    "dry_run": True,
                    "params": params
                }

            response = self.client.place_order(params)

            logger.info(f"Order response: {response}")

            return response

        except Exception as e:
            logger.error(f"Order failed: {str(e)}")
            raise TradingBotException(f"Failed to place order: {str(e)}")