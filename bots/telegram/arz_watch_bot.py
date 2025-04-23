import logging
import requests
from datetime import datetime

from telegram import Update
from telegram.ext import ApplicationBuilder, Application, CommandHandler, ContextTypes

from logger import LoggerFactory
from bots.telegram import messages
from bots.telegram.db import get_total_users, upsert_user

# Configure basic logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


class ArzWatchBot:
    """
    A Telegram bot to display real-time currency, gold, and coin prices.
    """

    def __init__(
        self,
        base_api_url: str,
        token: str,
        api_key: str,
        timeout: int = 30,
    ):
        # Validate input parameters
        if not base_api_url:
            raise ValueError("❌ BASE_API_URL not found in .env file!")
        if not api_key:
            raise ValueError("❌ API_KEY not found in .env file!")
        if not token:
            raise ValueError("❌ Telegram bot token not found in .env file!")

        self.base_api_url = base_api_url
        self.api_key = api_key
        self.token = token
        self.timeout = timeout

        self.logger = LoggerFactory.get_logger(
            "ArzWatchBot", "bots/telegram/arz_watch_bot"
        )
        self.app: Application = ApplicationBuilder().token(self.token).build()

        self._register_handlers()
        self.app.add_error_handler(self._handle_error)

    def _register_handlers(self) -> None:
        """Register all command handlers."""
        self.app.add_handler(CommandHandler("start", self._handle_start))
        self.app.add_handler(CommandHandler("help", self._handle_help))
        self.app.add_handler(CommandHandler("usage", self._handle_usage))

        self.app.add_handler(CommandHandler("gold", self._handle_gold))
        self.app.add_handler(CommandHandler("coin", self._handle_coin))
        self.app.add_handler(CommandHandler("crypto", self._handle_crypto))
        self.app.add_handler(CommandHandler("currency", self._handle_currency))

    async def _handle_start(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle /start command."""
        user = update.effective_user
        username = user.username or ""
        first_name = user.first_name or ""
        last_name = user.last_name or ""

        upsert_user(user.id, username, first_name, last_name)
        total_users = get_total_users()
        name_to_welcome = first_name or username

        await update.message.reply_text(
            messages.welcome(name_to_welcome, total_users), parse_mode="HTML"
        )

        self.logger.info(f"New user: {username} {first_name} {last_name}")

        payload = {
            "user_id": user.id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "is_bot": user.is_bot,
            "phone_number": getattr(user, "phone_number", ""),
            "language_code": getattr(user, "language_code", ""),
            "last_seen": update.message.date.isoformat(),
        }

        headers = {"Authorization": f"Api-Key {self.api_key}"}
        api_url = f"{self.base_api_url}/telegram/create-user/"

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 201:
                self.logger.info("✅ Successfully saved user info.")

        except Exception as e:
            self.logger.error(f"❌ Exception during user info save: {e}")

    async def _handle_help(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle /help command."""
        await update.message.reply_text(messages.help(), parse_mode="HTML")

    async def _handle_usage(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle /usage command."""

        headers = {"Authorization": f"Api-Key {self.api_key}"}
        api_url = f"{self.base_api_url}/telegram/user-info/"
        tg_user = update.effective_user

        payload = {
            "user_id": tg_user.id,
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                self.logger.info("✅ Successfully retrieved user info.")
                user = response.json()
                await update.message.reply_text(
                    messages.usage(
                        tg_user,
                        user["request_count"],
                        user["max_request_count"],
                        user["created_at"],
                    ),
                    parse_mode="HTML",
                )

            else:
                self.logger.error(
                    f"❌ Error retrieving user info: {response.status_code}"
                )
                await update.message.reply_text(messages.error(), parse_mode="HTML")

        except Exception as e:
            self.logger.error(f"❌ Exception during user info save: {e}")
            await update.message.reply_text(messages.error(), parse_mode="HTML")

    async def _fetch_and_reply(
        self, update: Update, endpoint: str, formatter_func
    ) -> None:
        """
        Helper function to fetch data and send formatted message.

        Args:
            update (Update): The Telegram update.
            endpoint (str): API endpoint.
            formatter_func (Callable): Function to format the response message.
        """
        headers = {"Authorization": f"Api-Key {self.api_key}"}
        api_url = f"{self.base_api_url}/scrapers/{endpoint}/"

        user = update.effective_user

        payload = {
            "user_id": user.id,
        }
        try:
            response = requests.post(
                api_url, json=payload, timeout=self.timeout, headers=headers
            )

            if response.status_code != 200:
                await update.message.reply_text(
                    "❌شما نمی‌توانید درخواست جدیدی داشته باشید!", parse_mode="HTML"
                )
                return

            data = response.json()
            items = data.get("data", [])
            retrieved_at = datetime.fromisoformat(data.get("retrieved_at", "N/A"))

            if not items:
                raise ValueError("No data returned.")

            await update.message.reply_text(
                formatter_func(items, retrieved_at), parse_mode="HTML"
            )
        except Exception as e:
            self.logger.error(f"❌ Error fetching {endpoint} data: {e}")
            await update.message.reply_text(messages.error(), parse_mode="HTML")

    async def _handle_gold(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle /gold command."""
        await self._fetch_and_reply(update, "tgju/gold", messages.gold)

    async def _handle_coin(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle /coin command."""
        await self._fetch_and_reply(update, "tgju/coin", messages.coin)

    async def _handle_crypto(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle /crypto command."""
        await self._fetch_and_reply(update, "coinex/crypto", messages.crypto)

    async def _handle_currency(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle /currency command."""
        await self._fetch_and_reply(update, "tgju/currency", messages.currency)

    async def _handle_error(
        self, update: object, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle any unexpected errors in the bot."""
        self.logger.error("Unhandled error occurred", exc_info=context.error)
        if isinstance(update, Update) and update.message:
            await update.message.reply_text(messages.error(), parse_mode="HTML")

    def run(self) -> None:
        """Start the bot polling."""
        self.logger.info("🚀 ArzWatchBot is starting polling...")
        self.app.run_polling()
