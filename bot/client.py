import time
import logging
from typing import Dict, Any, Callable
from functools import wraps

from binance.client import Client

from bot.config import settings
from bot.exceptions import APIError

logger = logging.getLogger(__name__)


def retry(max_retries: int = 3, delay: int = 1) -> Callable:
    """
    Retry decorator for API calls
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Retry {attempt} failed: {e}")
                    time.sleep(delay)

            raise APIError("Max retries exceeded")

        return wrapper

    return decorator


class BinanceClient:
    """
    Binance Futures Testnet Client Wrapper
    """

    def __init__(self):
        # 🔐 Validate keys
        if not settings.BINANCE_API_KEY or not settings.BINANCE_API_SECRET:
            raise APIError("API Key/Secret not found. Check your .env file.")

        # ✅ Initialize client
        self.client = Client(
            settings.BINANCE_API_KEY,
            settings.BINANCE_API_SECRET
        )

        # 🔥 FORCE Futures Testnet endpoint (CRITICAL FIX)
        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

        logger.info("Binance Futures Testnet client initialized")

    @retry(max_retries=3, delay=1)
    def place_order(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Place futures order
        """
        try:
            logger.info(f"API Request: {params}")

            response = self.client.futures_create_order(**params)

            logger.info(f"API Response: {response}")

            return response

        except Exception as e:
            logger.error(f"API Error: {e}")
            raise APIError(str(e))

    @retry(max_retries=3, delay=1)
    def get_account_info(self) -> Dict[str, Any]:
        """
        Fetch futures account info (for testing/debugging)
        """
        try:
            response = self.client.futures_account()
            logger.info("Fetched account info successfully")
            return response

        except Exception as e:
            logger.error(f"Account fetch error: {e}")
            raise APIError(str(e))