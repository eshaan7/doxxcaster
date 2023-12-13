import subprocess

from doxxcaster.bot.logger import LOGGER
from doxxcaster.bot.settings import XMTP_ENVIRONMENT

__all__ = ["send_xmtp_message"]


def send_xmtp_message(address: str, message: str) -> str | None | bool:
    """
    Optionally returns XMTP message ID.
    """
    try:
        stdout = subprocess.check_output(
            ["./xmtp", "-e", XMTP_ENVIRONMENT, "send", address, message]
        )
        stdout = stdout.decode()
        if stdout == "null":
            return None
        return stdout
    except Exception as exc:
        LOGGER.error("[send_xmtp_message] Failed sending XMTP message: %s", exc)
        return False
