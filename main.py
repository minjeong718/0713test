import streamlit as st
import pandas as pd

st.set_page_config(page_title="열섬현상과 전력수요 분석", layout="wide")

st.title("🌆 서울·양평 열섬현상과 전력수요 분석")

# -----------------------------
# 데이터 불러오기
# -----------------------------
seoul = pd.read_csv("서울_기온.csv", encoding="cp949")
yangpyeong = pd.read_csv("양평_기온.csv", encoding="cp949")
power = pd.read_csv("전력수요.csv", encoding="cp949")

# 날짜 형식 변환
seoul["일시"] = pd.to_datetime(seoul["일시"])
yangpyeong["일시"] = pd.to_datetime(yangpyeong["일시"])
power["일시"] = pd.to_datetime(power["일시"])

# 필요한 열만 선택 및 이름 변경
seoul = seoul[["일시", "기온(°C)"]].rename(columns={"기온(°C)": "서울기온"})
yangpyeong = yangpyeong[["일시", "기온(°C)"]].rename(columns={"기온(°C)": "양평기온"})

# -----------------------------
# 탭 생성
# -----------------------------
tab1, tab2 = st.tabs(["🌆 열섬 분석", "⚡ 전력 연결"])

# ==========================================================
# 탭1 : 열섬 분석
# ==========================================================
with tab1:

    st.header("서울과 양평의 열섬현상")

    # 같은 시간끼리 합치기
    temp = pd.merge(seoul, yangpyeong, on="일시")

    # 기온차 계산
    temp["기온차"] = temp["서울기온"] - temp["양평기온"]

    # -------------------------
    # ① 1년 기온 변화
    # -------------------------
    st.subheader("① 1년간 서울과 양평 기온 변화")

    line = temp.set_index("일시")[["서울기온", "양평기온"]]
    st.line_chart(line)

    # -------------------------
    # ② 시각별 평균 기온차
    # -------------------------
    st.subheader("② 시각별 평균 기온차 (서울 - 양평)")

    temp["시각"] = temp["일시"].dt.hour
    hour_avg = temp.groupby("시각")["기온차"].mean()

    st.bar_chart(hour_avg)

    # -------------------------
    # ③ 월별 평균 기온차
    # -------------------------
    st.subheader("③ 월별 평균 기온차 (서울 - 양평)")

    temp["월"] = temp["일시"].dt.month
    month_avg = temp.groupby("월")["기온차"].mean()

    st.bar_chart(month_avg)

# ==========================================================
# 탭2 : 전력 연결
# ==========================================================
with tab2:

    st.header("서울 기온과 전력수요의 관계")

    # 서울 기온 + 전력수요 합치기
    data = pd.merge(seoul, power, on="일시")

    # -------------------------
    # ① 산점도
    # -------------------------
    st.subheader("① 기온과 전력수요의 관계")

    st.scatter_chart(
        data,
        x="서울기온",
        y="전력수요(MWh)"
    )

    # -------------------------
    # ② 기온 구간별 평균 전력수요
    # -------------------------
    st.subheader("② 기온 구간별 평균 전력수요")

    bins = [-30, -20, -10, 0, 10, 20, 30, 40]
    labels = [
        "-20~-10",
        "-10~0",
        "0~10",
        "10~20",
        "20~30",
        "30~40",
        "40 이상"
    ]

    data["기온구간"] = pd.cut(
        data["서울기온"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    temp_power = data.groupby("기온구간")["전력수요(MWh)"].mean()

    st.bar_chart(temp_power)

    # -------------------------
    # ③ 월별 평균 전력수요
    # -------------------------
    st.subheader("③ 월별 평균 전력수요")

    data["월"] = data["일시"].dt.month

    month_power = data.groupby("월")["전력수요(MWh)"].mean()

    st.bar_chart(month_power)
