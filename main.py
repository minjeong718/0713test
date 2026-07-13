import streamlit as st
import pandas as pd

st.set_page_config(page_title="도시 열섬현상 분석", layout="wide")

st.title("🌆 서울과 양평의 도시 열섬현상 분석")

# 데이터 불러오기
seoul = pd.read_csv("서울_기온.csv", encoding="cp949")
yangpyeong = pd.read_csv("양평_기온.csv", encoding="cp949")

# 날짜 변환
seoul["일시"] = pd.to_datetime(seoul["일시"])
yangpyeong["일시"] = pd.to_datetime(yangpyeong["일시"])

# 필요한 열만 선택 후 이름 변경
seoul = seoul[["일시", "기온(°C)"]].rename(columns={"기온(°C)": "서울"})
yangpyeong = yangpyeong[["일시", "기온(°C)"]].rename(columns={"기온(°C)": "양평"})

# 데이터 합치기
df = pd.merge(seoul, yangpyeong, on="일시")

# 기온차 계산
df["기온차"] = df["서울"] - df["양평"]

# 시간, 월 정보 추가
df["시"] = df["일시"].dt.hour
df["월"] = df["일시"].dt.month

# -------------------------------
# ① 1년간 기온 변화
# -------------------------------
st.header("① 1년간 서울과 양평의 기온 변화")

line_df = df.set_index("일시")[["서울", "양평"]]
st.line_chart(line_df)

# -------------------------------
# ② 시간별 평균 기온차
# -------------------------------
st.header("② 시간(0~23시)별 평균 기온차 (서울 - 양평)")

hour_mean = df.groupby("시")["기온차"].mean()
st.bar_chart(hour_mean)

# -------------------------------
# ③ 월별 평균 기온차
# -------------------------------
st.header("③ 월(1~12월)별 평균 기온차 (서울 - 양평)")

month_mean = df.groupby("월")["기온차"].mean()
st.bar_chart(month_mean)

# -------------------------------
# 요약 통계
# -------------------------------
st.header("📊 요약")

st.write(f"연평균 기온차(서울-양평): **{df['기온차'].mean():.2f}℃**")
st.write(f"최대 기온차: **{df['기온차'].max():.2f}℃**")
st.write(f"최소 기온차: **{df['기온차'].min():.2f}℃**")
