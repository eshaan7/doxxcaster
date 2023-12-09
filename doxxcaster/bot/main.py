import asyncio
import time
from typing import List

from farcaster import Warpcast
from farcaster.models import ApiCast

from doxxcaster.bot.airstack_utils import (
    get_erc20_token_balances_of_fc_user,
    get_socials_of_fc_user,
)
from doxxcaster.bot.logger import LOGGER
from doxxcaster.bot.models import ERC20Balance, Socials
from doxxcaster.bot.settings import (
    FARCASTER_ACCESS_TOKEN,
    FARCASTER_BOT_AUTHOR_USERNAME,
    FARCASTER_BOT_USERNAME,
    MAX_NUM_BAGS_IN_MESSAGE,
    SECONDS_TO_SLEEP_ON_ERROR,
)
from doxxcaster.bot.warpcast_utils import extract_username_from_cast, reply_to_cast


def build_message(
    fname: str, socials: Socials, erc20_balances: List[ERC20Balance]
) -> str:
    socials_str = "\n".join(
        (
            f"{heading}: {', '.join(getattr(socials, field)[:5])}"
        )  # this limit is to not exceed a cast's characters limit (320)
        for heading, field in [
            # ("Addresses", "addresses"), # disabling this to allow more room for bags
            ("ENS", "ens_names"),
            ("Twitter (X)", "twitter_usernames"),
            ("Lens", "lens_names"),
            ("Farcaster", "fc_names"),
        ]
        if getattr(socials, field)
    )
    bags_str = "\n".join(
        f"{idx+1}. {int(erc20_balance.amount)} ${erc20_balance.symbol}"
        + (
            (
                f", 24h ⬆️ {round(abs(erc20_balance.priceChange24h), 2)}"
                if erc20_balance.priceChange24h > 0
                else f", 24h ⬇️ {round(abs(erc20_balance.priceChange24h), 2)}"
            )
            if erc20_balance.priceChange24h is not None
            else ""
        )
        for idx, erc20_balance in enumerate(erc20_balances[:MAX_NUM_BAGS_IN_MESSAGE])
    )

    return f"""🥷 Doxxing @{fname}

👤 Socials: 
{socials_str}

💰 Bags:
{bags_str}
"""


async def handle_cast(wc: Warpcast, cast: ApiCast, fname: str) -> None:
    try:
        # fetch user details from Airstack
        LOGGER.info(
            "[+] Fetching socials and balances details (username=%s, cast_hash=%s, user=%s).",
            fname,
            cast.hash,
            cast.author.username,
        )
        socials = await get_socials_of_fc_user(fname)
        erc20_balances = await get_erc20_token_balances_of_fc_user(fname)

        # construct the reply cast's text
        message = build_message(fname, socials, erc20_balances)

        # post reply cast
        reply_to_cast(wc, cast, message=message)
        LOGGER.info(
            "[+] Successfully replied to cast (username=%s, cast_hash=%s, user=%s).",
            fname,
            cast.hash,
            cast.author.username,
        )
    except Exception as exc:
        LOGGER.exception("[handle_cast] Failed: %s", exc)


def start_notification_stream() -> None:
    # TODO: could use mnemonic too but that would be much less secure
    wc = Warpcast(access_token=FARCASTER_ACCESS_TOKEN)

    for notif in wc.stream_notifications(skip_existing=True):
        if notif and notif.content.cast.text.startswith(f"@{FARCASTER_BOT_USERNAME}"):
            cast = notif.content.cast
            LOGGER.info(
                "[#] Got notification %s (cast_hash=%s, user=%s)",
                notif.id,
                cast.hash,
                cast.author.username,
            )
            # like the cast by our bot as an acknowledgement
            wc.like_cast(cast.hash)
            LOGGER.info(
                "[+] Acknowledged (cast_hash=%s, user=%s).",
                cast.hash,
                cast.author.username,
            )
            # extract username from either cast's text or parent cast's author
            fname = extract_username_from_cast(wc, cast)
            if fname:
                # if valid username detected we proceed further
                LOGGER.info(
                    "[+] Valid username found (username=%s, cast_hash=%s, user=%s).",
                    fname,
                    cast.hash,
                    cast.author.username,
                )
                asyncio.run(handle_cast(wc, cast, fname))
            else:
                # else just reply to the cast with an error message
                LOGGER.info(
                    "[-] No valid username found (cast_hash=%s, user=%s).",
                    cast.hash,
                    cast.author.username,
                )
                reply_to_cast(
                    wc,
                    cast,
                    message=f"Invalid command. Contact @{FARCASTER_BOT_AUTHOR_USERNAME} for help.",
                )


def main():
    LOGGER.info("Starting notification stream in main")
    while True:
        try:
            start_notification_stream()
        except Exception as exc:
            LOGGER.exception(
                "Error occurred in notification stream, main function: %s", exc
            )
            time.sleep(SECONDS_TO_SLEEP_ON_ERROR)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        LOGGER.error("Error occurred __main__ function: %s", exc)
