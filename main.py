from bots.telegram import ArzWatchBot
from core.config import (
    BASE_API_URL,
    API_ACCESS_KEY,
    TELEGRAM_BOT_TIMEOUT,
    TELEGRAM_BOT_TOKEN,
)


def main():
    # Check if the BASE_API_URL and TELEGRAM_BOT_TOKEN are set
    if not BASE_API_URL or not TELEGRAM_BOT_TOKEN or not API_ACCESS_KEY:
        raise ValueError(
            "BASE_API_URL and TELEGRAM_BOT_TOKEN and API_ACCESS_KEY must be set in environment variables."
        )

    # Create an instance of the ArzWatchBot class
    bot = ArzWatchBot(
        token=TELEGRAM_BOT_TOKEN,
        base_api_url=BASE_API_URL,
        api_key=API_ACCESS_KEY,
        timeout=int(TELEGRAM_BOT_TIMEOUT),
    )

    # Run the bot
    bot.run()


if __name__ == "__main__":
    main()
