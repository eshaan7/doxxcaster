import os

from dotenv import load_dotenv

load_dotenv()

__all__ = [
    "XMTP_ENVIRONMENT",
    "LOGLEVEL",
    "SECONDS_TO_SLEEP_ON_ERROR",
    "MAX_NUM_BAGS_IN_MESSAGE",
    "FARCASTER_BOT_USERNAME",
    "FARCASTER_BOT_AUTHOR_USERNAME",
    "FARCASTER_ACCESS_TOKEN",
    "AIRSTACK_API_KEY",
]

# options: "dev", "production", "local"
XMTP_ENVIRONMENT = os.getenv("XMTP_ENVIRONMENT", "local")
LOGLEVEL = os.getenv("LOGLEVEL", "info").upper()
SECONDS_TO_SLEEP_ON_ERROR = int(os.getenv("SECONDS_TO_SLEEP_ON_ERROR", "60"))
MAX_NUM_BAGS_IN_MESSAGE = int(os.getenv("MAX_NUM_BAGS_IN_MESSAGE", "5"))
FARCASTER_BOT_USERNAME = os.getenv("FARCASTER_BOT_USERNAME")
FARCASTER_BOT_AUTHOR_USERNAME = os.getenv("FARCASTER_BOT_AUTHOR_USERNAME")
FARCASTER_ACCESS_TOKEN = os.getenv("FARCASTER_ACCESS_TOKEN")
AIRSTACK_API_KEY = os.getenv("AIRSTACK_API_KEY")
