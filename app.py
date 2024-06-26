#
# https://www.cultivationdata.net/weather-web-api.html#twoweek


import csv
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit.logger import get_logger

from open_meteo_api import fetch_daily_max_min_temp

logger = get_logger(__name__)

timezone = "Asia/Tokyo"

with open("./data/prefecturalCapital.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    pref_locations = [row for row in reader]

# skip header
pref_locations = pref_locations[1:]

# session_stateに基づき、初来訪か判断
if "first_visit" not in st.session_state:
    st.session_state["first_visit"] = True
    st.info("このセッションは初めて確立されました")

logger.info(f"都道府県データの読込完了{len(pref_locations)}")

st.markdown("### データの読み込み")
option = st.selectbox("都道府県を選択", pref_locations, format_func=lambda p: p[1])
st.markdown("選択中の都道府県: `%s`" % option[1])


@st.cache_data(ttl="1day", show_spinner="キャッシュミス発生")
def get_daily_temp(latitude, longitude):
    with st.spinner("API問い合わせ中"):
        data = fetch_daily_max_min_temp(latitude, longitude)
    dt_now = datetime.now()
    st.markdown("キャッシュ作成日次: `%s`" % dt_now.strftime("%Y年%m月%d日 %H時%M分%S秒"))
    return data


# 天気予報データを取得
data = get_daily_temp(option[2], option[3])

# グラフ描画用のデータフレーム
df = pd.DataFrame(
    {
        "日付": data["time"],
        "最低気温": data["temperature_2m_min"],
        "最高気温": data["temperature_2m_max"],
    }
)

st.divider()

st.markdown("### グラフ描画")
st.markdown("#### st.line_chart")
with st.echo("above"):
    # st.altair_chartのsyntax-sugar
    st.line_chart(df, x="日付", x_label="日付", y_label="気温(℃)", color=["#29B6F6", "#F44336"])

st.markdown("#### px.line")
with st.echo("above"):
    fig = px.line(df, x="日付", y=["最低気温", "最高気温"])
    st.plotly_chart(fig)
