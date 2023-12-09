import subprocess
from typing import Optional

from doxxcaster.bot.logger import LOGGER

__all__ = ["send_xmtp_message"]


def send_xmtp_message(address: str, message: str) -> Optional[str]:
    """
    Optionally returns XMTP message ID.
    """
    try:
        stdout = subprocess.check_output(
            ["./xmtp", "-e", "production", "send", address, message]
        )
        return stdout.decode()
    except Exception as exc:
        LOGGER.error("[send_xmtp_message] Failed sending XMTP message: %s", exc)
