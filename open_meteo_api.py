import urllib.parse

import requests
from streamlit.logger import get_logger

logger = get_logger(__name__)


# open-meteoのAPIから週間の最低/最高気温を取得
def fetch_daily_max_min_temp(latitude, longitude, timezone="Asia/Tokyo"):
    timezone = urllib.parse.quote(timezone)
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min&timezone={timezone}"

    logger.info(f"fetch {url}")
    r = requests.get(url, timeout=(3, 10))
    r.raise_for_status()
    data = r.json()
    if "daily" not in data:
        raise ValueError("OpenMeteoの返り値が不正です。")
    return data["daily"]
