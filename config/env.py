from dotenv import load_dotenv
import os

load_dotenv()
# Read credentials from environment
CONSUMER_KEY = os.getenv("KOTAK_CONSUMER_KEY")
MOBILE = os.getenv("KOTAK_MOBILE")
UCC = os.getenv("KOTAK_UCC")
MPIN = os.getenv("KOTAK_MPIN")

def validate_env():
    missing = [k for k, v in globals().items()
               if k.isupper() and v is None]
    if missing:
        raise RuntimeError(f"Missing env vars: {missing}")