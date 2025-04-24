from telegram import User
from datetime import datetime
from typing import Union, List, Dict
from bots.utils import (
    format_price,
    build_item_section,
    persian_date_time,
    get_change_symbol,
    parse_percentage,
    time_until_midnight_tehran,
)


# === Message Templates === #
def welcome(username: str, total_users: int) -> str:
    return f"""
سلام 👋 <b>{username}</b> عزیز!  
به ربات <b>ArzWatch</b> خوش اومدی 🔥

این ربات برای نمایش قیمت‌های لحظه‌ای بازار طراحی شده 🧑‍💻

<code><b>{total_users}</b></code> نفر درحال استفاده از این ربات هستند. 👥

برای مشاهده دستورات موجود، کافیه از دستور زیر استفاده کنی:
👉 /help

برای انتقادات، پیشنهادات و یا گزارش خرابی و باگ به این آیدی پیام دهید:
@pouria_drd
"""


def help() -> str:
    return """
📚 <b>راهنمای دستورات ربات ArzWatch</b>

/gold - قیمت طلا
/coin - قیمت سکه
/crypto - قیمت ارز دیجیتال
/currency - قیمت ارزها
/usage - نمایش اطلاعات مصرفی
/help - نمایش همین راهنما  

💡 همه‌ی اطلاعات از منابع معتبر و به‌روز جمع‌آوری میشه و ربات هر چند دقیقه یکبار آپدیت میشه!


برای انتقادات، پیشنهادات و یا گزارش خرابی و باگ به این آیدی پیام دهید:
@pouria_drd
"""


def gold(golds: List[Dict[str, str]], last_updated: datetime) -> str:
    date, time = persian_date_time(last_updated)
    body = "\n".join([build_item_section(gold) for gold in golds])
    return f"""
<b>📊 قیمت طلا</b>

🗓️ <b>{date}</b> ⏰ <b>{time}</b>
———————————————
{body}
"""


def coin(coins: List[Dict[str, str]], last_updated: datetime) -> str:
    date, time = persian_date_time(last_updated)
    body = "\n".join([build_item_section(coin) for coin in coins])
    return f"""
<b>📊 قیمت سکه</b>

🗓️ <b>{date}</b> ⏰ <b>{time}</b>
———————————————
{body}
"""


def currency(currencies: List[Dict[str, str]], last_updated: datetime) -> str:
    date, time = persian_date_time(last_updated)
    flags = {
        "دلار": "🇺🇸",
        "یورو": "🇪🇺",
        "درهم امارات": "🇦🇪",
        "پوند انگلیس": "🇬🇧",
        "لیر ترکیه": "🇹🇷",
        "یوان چین": "🇨🇳",
        "روبل روسیه": "🇷🇺",
    }
    body = "\n".join(
        [
            build_item_section(currency, flag=flags.get(currency["title"], "🏳️"))
            for currency in currencies
        ]
    )
    return f"""
<b>📊 قیمت ارزها</b>

🗓️ <b>{date}</b> ⏰ <b>{time}</b>
———————————————
{body}
"""


def crypto(coins: List[Dict[str, str]], last_updated: datetime) -> str:
    date, time = persian_date_time(last_updated)
    body = "\n".join(
        [
            f"""
💰 <b>{coin['name_fa']}</b> <code>({coin['symbol']})</code>
💵 قیمت دلار: <code>{coin['price_usd']}</code>
💵 قیمت تومان: <code>{format_price(coin['price_irr'])}</code>
💰 مارکت کپ: <code>{coin['market_cap']}</code>
{get_change_symbol(parse_percentage(coin['change_24h']))} تغییرات ۲۴ساعته: <code>{coin['change_24h']}</code>
———————————————
"""
            for coin in coins
        ]
    )
    return f"""
<b>📊 قیمت ارز دیجیتال</b>

🗓️ <b>{date}</b> ⏰ <b>{time}</b>
———————————————
{body}
"""


def error() -> str:
    return "❌ خطایی رخ داد! لطفا دوباره امتحان کنید."


def usage(
    user: User,
    request_count: Union[str, int],
    max_request_count: Union[str, int],
    created_at: datetime,
) -> str:
    name = user.first_name or user.name.strip("@")
    persian_date, persian_time = persian_date_time(created_at)

    # Normalize counts
    request_count = int(request_count)
    max_request_count = int(max_request_count)
    percent = int((request_count / max_request_count) * 100)

    # Emoji indicator based on usage level
    if percent < 40:
        usage_emoji = "🟢"
    elif percent < 70:
        usage_emoji = "🟡"
    elif percent < 90:
        usage_emoji = "🟠"
    else:
        usage_emoji = "🔴"

    # Warning message
    if percent >= 100:
        warning = "⛔ <b>شما به سقف مجاز امروز رسیدید !</b>"
    elif percent >= 90:
        warning = "🚨 <b>شما به سقف مجاز امروز نزدیک شده‌اید!</b>"
    elif percent >= 70:
        warning = "⚠️ <b>در حال نزدیک شدن به سقف مجاز هستید.</b>"
    else:
        warning = ""

    return f"""
خیلی خوشحالیم که از ربات ما استفاده می‌کنی <b>{name}</b> !

اطلاعات مصرفی شما:

{usage_emoji} <b>درصد مصرف:</b> <code>{percent}%</code>
📊 <b>تعداد درخواست امروز:</b> <code>{request_count}</code> از <code>{max_request_count}</code>
🗓️تاریخ عضویت: <b>{persian_date}</b> ⏰ <b>{persian_time}</b>

{warning}
"""


# ⏳ <b>زمان باقی‌مانده تا ریست:</b> {time_until_midnight_tehran()}
