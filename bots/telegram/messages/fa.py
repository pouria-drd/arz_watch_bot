from zoneinfo import ZoneInfo
from persiantools.jdatetime import JalaliDateTime


def welcome(username: str, total_users: int) -> str:
    return f"""
سلام 👋 <b>{username}</b> عزیز!  
به ربات <b>ArzWatch</b> خوش اومدی 🔥

این ربات برای نمایش قیمت‌های لحظه‌ای بازار طراحی شده 🧑‍💻

<code><b>{total_users}</b></code> نفر درحال استفاده از این ربات هستند. 👥

برای مشاهده دستورات موجود، کافیه از دستور زیر استفاده کنی:
👉 /help
"""


def help() -> str:
    return """
📚 <b>راهنمای دستورات ربات ArzWatch</b>

/gold - قیمت طلا
/coin - قیمت سکه
/crypto - قیمت ارز دیجیتال
/currency - قیمت ارزها
/help - نمایش همین راهنما  

💡 همه‌ی اطلاعات از منابع معتبر و به‌روز جمع‌آوری میشه و ربات هر چند دقیقه یکبار آپدیت میشه!
"""


def gold(golds, last_updated) -> str:
    # Convert UTC to Tehran timezone
    tehran_time = last_updated.astimezone(ZoneInfo("Asia/Tehran"))
    jalali_time = JalaliDateTime.to_jalali(tehran_time)

    persian_date = jalali_time.strftime("%d %B %Y", locale="fa")
    persian_time = jalali_time.strftime("%H:%M", locale="fa")

    response = f"""
<b>📊 قیمت طلا</b>

🗓️ <b>{persian_date}</b> ⏰ <b>{persian_time}</b>
———————————————
"""
    for gold in golds:
        fa_title = gold["title"]
        # Format the price with commas
        formatted_price = "{:,}".format(int(int(gold["price"]) / 10))

        # Check if the change is negative or positive
        change_symbol = "📉" if int(gold["changeAmount"]) < 0 else "📈"

        # Adding the gold data to the response
        response += f"""
🔹 <b>{fa_title}</b>
💰 <b>قیمت:</b> <code>{formatted_price}</code> تومان
{change_symbol} <b>مقدار تغییر:</b> <code>{gold['changeAmount']}</code>
{change_symbol} <b>درصد تغییر:</b> <code>{gold['changePercentage']}</code>
———————————————
"""
    return response


def coin(coins, last_updated) -> str:
    # Convert UTC to Tehran timezone
    tehran_time = last_updated.astimezone(ZoneInfo("Asia/Tehran"))
    jalali_time = JalaliDateTime.to_jalali(tehran_time)

    persian_date = jalali_time.strftime("%d %B %Y", locale="fa")
    persian_time = jalali_time.strftime("%H:%M", locale="fa")

    response = f"""
<b>📊 قیمت سکه</b>

🗓️ <b>{persian_date}</b> ⏰ <b>{persian_time}</b>
———————————————
"""
    for coin in coins:
        fa_title = coin["title"]

        # Format the price with commas
        formatted_price = "{:,}".format(int(int(coin["price"]) / 10))

        # Check if the change is negative or positive
        change_symbol = "📉" if int(coin["changeAmount"]) < 0 else "📈"

        # Adding the coin data to the response
        response += f"""
🔹 <b>{fa_title}</b>
💰 <b>قیمت:</b> <code>{formatted_price}</code> تومان
{change_symbol} <b>مقدار تغییر:</b> <code>{coin['changeAmount']}</code>
{change_symbol} <b>درصد تغییر:</b> <code>{coin['changePercentage']}</code>
———————————————
"""

    return response


def currency(currencies, last_updated) -> str:
    # Convert UTC to Tehran timezone
    tehran_time = last_updated.astimezone(ZoneInfo("Asia/Tehran"))
    jalali_time = JalaliDateTime.to_jalali(tehran_time)

    persian_date = jalali_time.strftime("%d %B %Y", locale="fa")
    persian_time = jalali_time.strftime("%H:%M", locale="fa")

    # Flag mapping
    flag_map = {
        "دلار": "🇺🇸",
        "یورو": "🇪🇺",
        "درهم امارات": "🇦🇪",
        "پوند انگلیس": "🇬🇧",
        "لیر ترکیه": "🇹🇷",
        "یوان چین": "🇨🇳",
        "روبل روسیه": "🇷🇺",
    }

    response = f"""
<b>📊 قیمت ارزها</b>

🗓️ <b>{persian_date}</b> ⏰ <b>{persian_time}</b>
———————————————
"""
    for currency in currencies:
        fa_title = currency["title"]

        flag = flag_map.get(fa_title, "🏳️")  # Default flag if not found
        # Format the price with commas
        formatted_price = "{:,}".format(int(int(currency["price"]) / 10))
        # Check if the change is negative or positive
        change_symbol = "📉" if int(currency["changeAmount"]) < 0 else "📈"
        # Adding the currency data to the response
        response += f"""
🔹 <b>{fa_title}</b> {flag}
💰 <b>قیمت:</b> <code>{formatted_price}</code> تومان
{change_symbol} <b>مقدار تغییر:</b> <code>{currency['changeAmount']}</code>
{change_symbol} <b>درصد تغییر:</b> <code>{currency['changePercentage']}</code>
———————————————
"""

    return response


def error() -> str:
    return "❌ خطای داخلی. لطفا دوباره امتحان کن."
