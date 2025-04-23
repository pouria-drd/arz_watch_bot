from zoneinfo import ZoneInfo
from typing import Union, Tuple, Dict
from datetime import datetime, timedelta
from persiantools.jdatetime import JalaliDateTime


def format_price(value: Union[str, int]) -> str:
    """
    Formats a given price value to include commas.

    Args:
        value (Union[str, int]): The price value to format.

    Returns:
        str: The formatted price value. Example: "12,345,678".
    """
    return f"{int(int(value) / 10):,}"


def get_change_symbol(change_amount: Union[str, int]) -> str:
    """
    Returns the appropriate change symbol based on the given change amount.

    Args:
        change_amount (Union[str, int]): The change amount to check.

    Returns:
        str: The change symbol. Example: "📉" or "📈".
    """
    return "📉" if int(change_amount) < 0 else "📈"


def build_item_section(item: Dict[str, str], flag: str = "") -> str:
    """
    Builds a section for a given item with the given flag.

    Args:
        item (Dict[str, str]): The item to build the section for.
        flag (str): The flag to display next to the item title.

    Returns:
        str: The built section.
    """
    title = item["title"]
    price = format_price(item["price"])
    symbol = get_change_symbol(item["change_amount"])

    return f"""
🔹 <b>{title}</b> {flag}
💰 <b>قیمت:</b> <code>{price}</code> تومان
{symbol} <b>مقدار تغییر:</b> <code>{item['change_amount']}</code>
{symbol} <b>درصد تغییر:</b> <code>{item['change_percentage']}</code>
———————————————"""


def persian_date_time(dt: Union[str, datetime]) -> Tuple[str, str]:
    """
    Converts a given datetime (or ISO-format string) to Persian date and time.

    Args:
        dt (Union[str, datetime]): datetime object or ISO-format datetime string.

    Returns:
        Tuple[str, str]: Persian date and time in string format.
    """
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt)
        except ValueError:
            raise ValueError(
                "Invalid datetime string format passed to persian_date_time"
            )

    tehran_time = dt.astimezone(ZoneInfo("Asia/Tehran"))
    jalali = JalaliDateTime.to_jalali(tehran_time)
    return (
        jalali.strftime("%d %B %Y", locale="fa"),
        jalali.strftime("%H:%M", locale="fa"),
    )


def time_until_midnight_tehran() -> str:
    """
    Returns the time until midnight in Tehran.

    Returns:
        str: The time until midnight in Tehran.
    """
    # Get the current time in Tehran
    now = datetime.now(ZoneInfo("Asia/Tehran"))
    # Calculate the time until tomorrow's midnight
    tomorrow = (now + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    # Calculate the time difference between now and tomorrow
    remaining = tomorrow - now
    hours, remainder = divmod(remaining.seconds, 3600)
    minutes = remainder // 60
    return f"{hours} ساعت و {minutes} دقیقه"
