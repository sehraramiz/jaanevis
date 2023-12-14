import logging
import sys

import requests

if __name__ == "__main__":
    sys.path = ["", ".."] + sys.path[1:]

from jaanevis.config import settings

logger = logging.getLogger(__name__)


def send_message_to_channel(msg: str) -> None:
    data = {
        "chat_id": f"@{settings.TELEGRAM_CHANNEL_ID}",
        "text": msg,
        "parse_mode": "html",
        "entities": ["hashtag"],
    }
    url = "https://api.telegram.org/bot{}/sendMessage".format(
        settings.TELEGRAM_BOT_TOKEN
    )
    result = requests.post(url, json=data)
    print(result.text)


if __name__ == "__main__":
    send_message_to_channel("this\nis a test\nwith #hashtag")
