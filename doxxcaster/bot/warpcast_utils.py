from typing import Optional

from farcaster import Warpcast
from farcaster.models import ApiCast, Parent

from doxxcaster.bot.logger import LOGGER

__all__ = ["build_cast_url", "extract_username_from_cast", "reply_to_cast"]


def build_cast_url(fname: str, cast_hash: str) -> str:
    return f"https://warpcast.com/{fname}/{cast_hash}"


def extract_username_from_cast(wc: Warpcast, cast: ApiCast) -> Optional[str]:
    split_str = cast.text.split(" ")
    if len(split_str) == 2:
        # this cast itself may have the fname to dox
        return split_str[1].removeprefix("@")
    elif len(split_str) == 1:
        # this cast was a reply to parent cast to dox parent cast's author
        if cast.parent_hash:
            parent_cast = wc.get_cast(cast.parent_hash).cast
            if parent_cast and parent_cast.author.username:
                return parent_cast.author.username


def reply_to_cast(wc: Warpcast, cast: ApiCast, message: str) -> Optional[ApiCast]:
    """
    Post a reply cast with given message to the given cast.

    Args:
        wc: Warpcast instance.
        cast: The parent cast to reply to.

    Returns:
        None
    """
    try:
        cast_content = wc.post_cast(
            message[:320],  # warpcast doesn't allow more than 320 chars
            parent=Parent(
                fid=cast.author.fid,
                hash=cast.hash,
            ),
        )
        return cast_content.cast
    except Exception as exc:
        LOGGER.exception("[cast_reply] Failed sending message: %s", exc)
