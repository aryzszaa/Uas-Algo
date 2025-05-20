import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Covid-19 Indonesia", layout="wide")
st.title("📊 Dashboard Data Covid-19 Indonesia")

# Load data
@st.cache_data
def load_data():
    df = df = pd.read_csv("data_covid_indonesia.csv")
    df["tanggal"] = pd.to_datetime(df["tanggal"])
    df["provinsi"] = df["provinsi"].astype(str)
    return df

df = load_data()

# Sidebar - Filter
st.sidebar.header("🔎 Filter Data")
provinsi_selected = st.sidebar.multiselect(
    "Pilih Provinsi", options=df["provinsi"].unique(), default=df["provinsi"].unique()
)
tanggal_mulai = st.sidebar.date_input("Tanggal Mulai", df["tanggal"].min())
tanggal_akhir = st.sidebar.date_input("Tanggal Akhir", df["tanggal"].max())

# Filter data
filtered_df = df[
    (df["provinsi"].isin(provinsi_selected)) &
    (df["tanggal"] >= pd.to_datetime(tanggal_mulai)) &
    (df["tanggal"] <= pd.to_datetime(tanggal_akhir))
]

# Statistik agregat
st.subheader("📈 Statistik Agregat")
total_kasus = int(filtered_df["kasus_harian"].sum())
total_sembuh = int(filtered_df["sembuh"].sum())
total_meninggal = int(filtered_df["meninggal"].sum())

rate_sembuh = (total_sembuh / total_kasus) * 100 if total_kasus else 0
rate_meninggal = (total_meninggal / total_kasus) * 100 if total_kasus else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Kasus", f"{total_kasus:,}")
col2.metric("Tingkat Kesembuhan", f"{rate_sembuh:.2f}%")
col3.metric("Rasio Kematian", f"{rate_meninggal:.2f}%")

# Grafik kasus harian
st.subheader("📅 Grafik Kasus Harian")
kasus_per_tanggal = filtered_df.groupby("tanggal")["kasus_harian"].sum()
st.line_chart(kasus_per_tanggal)

# Tabel data per provinsi
st.subheader("🗺️ Data Per Provinsi")
df_provinsi = filtered_df.groupby("provinsi").agg({
    "kasus_harian": "sum",
    "sembuh": "sum",
    "meninggal": "sum"
}).reset_index()

df_provinsi["Tingkat Kesembuhan (%)"] = (df_provinsi["sembuh"] / df_provinsi["kasus_harian"]) * 100
df_provinsi["Rasio Kematian (%)"] = (df_provinsi["meninggal"] / df_provinsi["kasus_harian"]) * 100

st.dataframe(df_provinsi.style.format({
    "kasus_harian": "{:,}",
    "sembuh": "{:,}",
    "meninggal": "{:,}",
    "Tingkat Kesembuhan (%)": "{:.2f}%",
    "Rasio Kematian (%)": "{:.2f}%"
}))
