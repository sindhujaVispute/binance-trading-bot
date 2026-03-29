import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BINANCE_API_KEY: str = os.getenv("BINANCE_API_KEY", "")
    BINANCE_API_SECRET: str = os.getenv("BINANCE_API_SECRET", "")
    BASE_URL: str = "https://testnet.binancefuture.com"
  

settings = Settings()
print("KEY:", repr(settings.BINANCE_API_KEY))
print("SECRET:", repr(settings.BINANCE_API_SECRET))