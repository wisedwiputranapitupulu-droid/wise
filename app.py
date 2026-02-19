import streamlit as st
import random
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta

# ==============================
# KONFIGURASI HALAMAN
# ==============================
st.set_page_config(
    page_title="Simulasi Piket IT Del",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Simulasi Sistem Piket IT Del")
st.caption("Monte Carlo Simulation • Interactive Dashboard • Real-time Analysis")

# ==============================
# SIDEBAR PARAMETER
# ==============================
st.sidebar.title("⚙ Pengaturan")

JUMLAH_MEJA = st.sidebar.slider("Jumlah Meja", 10, 100, 60)
MAHASISWA_PER_MEJA = st.sidebar.slider("Mahasiswa per Meja", 1, 5, 3)
JAM_MULAI = st.sidebar.slider("Jam Mulai", 5, 9, 7)

TOTAL_OMPRENG = JUMLAH_MEJA * MAHASISWA_PER_MEJA

JUMLAH_SIMULASI = st.sidebar.slider(
    "Jumlah Monte Carlo Simulation",
    50, 500, 200
)

kecepatan = st.sidebar.slider(
    "Kecepatan Animasi",
    0.0, 0.05, 0.005
)

st.sidebar.divider()

st.sidebar.metric("Total Ompreng", TOTAL_OMPRENG)

# ==============================
# METRICS UTAMA
# ==============================
col1, col2, col3, col4 = st.columns(4)

col1.metric("🍱 Total Ompreng", TOTAL_OMPRENG)
col2.metric("🪑 Meja", JUMLAH_MEJA)
col3.metric("👨‍🎓 Mahasiswa", TOTAL_OMPRENG)
col4.metric("🕐 Jam Mulai", f"{JAM_MULAI}:00")

st.divider()

# ==============================
# FUNGSI SIMULASI
# ==============================
def simulasi_detail():

    waktu_total = 0
    data = []

    # Isi lauk
    for i in range(TOTAL_OMPRENG):
        w = random.uniform(30, 60)
        waktu_total += w
        data.append(["Isi Lauk", waktu_total/60])

    # Angkat ompreng
    sisa = TOTAL_OMPRENG
    while sisa > 0:

        angkut = random.randint(4, 7)
        w = random.uniform(20, 60)

        waktu_total += w
        data.append(["Angkat Ompreng", waktu_total/60])

        sisa -= angkut

    # Tambah nasi
    for i in range(TOTAL_OMPRENG):
        w = random.uniform(30, 60)
        waktu_total += w
        data.append(["Tambah Nasi", waktu_total/60])

    df = pd.DataFrame(data, columns=["Tahap", "Waktu"])

    return waktu_total/60, df


# ==============================
# BUTTON SIMULASI
# ==============================
if st.button("🚀 Jalankan Simulasi"):

    progress = st.progress(0)
    status = st.empty()

    for i in range(100):
        progress.progress(i+1)
        status.text(f"Memproses simulasi {i+1}%")
        time.sleep(0.005)

    total_waktu, df = simulasi_detail()

    selesai = datetime(2024,1,1,JAM_MULAI,0,0) + timedelta(minutes=total_waktu)

    efisiensi = max(0, 100 - total_waktu/300*100)

    # ==============================
    # HASIL UTAMA
    # ==============================
    st.subheader("📊 Hasil Utama")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total waktu", f"{total_waktu:.2f} menit")
    c2.metric("Jam selesai", selesai.strftime("%H:%M"))
    c3.metric("Efisiensi", f"{efisiensi:.1f}%")
    c4.metric("Ompreng diproses", TOTAL_OMPRENG)

    # ==============================
    # GAUGE
    # ==============================
    st.subheader("⚡ Gauge Efisiensi")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=efisiensi,
        title={'text': "Efisiensi (%)"},
        gauge={'axis': {'range': [0, 100]}}
    ))

    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # MONTE CARLO REALTIME
    # ==============================
    st.subheader("📊 Monte Carlo Simulation")

    hasil = []

    chart = st.empty()

    for i in range(JUMLAH_SIMULASI):

        hasil.append(simulasi_detail()[0])

        fig_temp = px.line(
            x=range(len(hasil)),
            y=hasil,
            title="Realtime Simulation"
        )

        chart.plotly_chart(fig_temp, use_container_width=True)

        time.sleep(kecepatan)

    # ==============================
    # HISTOGRAM
    # ==============================
    st.subheader("Histogram")

    fig_hist = px.histogram(
        hasil,
        nbins=30,
        title="Distribusi Waktu"
    )

    st.plotly_chart(fig_hist, use_container_width=True)

    # ==============================
    # BOXPLOT
    # ==============================
    st.subheader("Boxplot Analisis")

    fig_box = px.box(
        hasil,
        title="Analisis Statistik"
    )

    st.plotly_chart(fig_box, use_container_width=True)

    # ==============================
    # STATISTIK
    # ==============================
    st.subheader("Statistik")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Mean", f"{np.mean(hasil):.2f}")
    c2.metric("Min", f"{np.min(hasil):.2f}")
    c3.metric("Max", f"{np.max(hasil):.2f}")
    c4.metric("Std Dev", f"{np.std(hasil):.2f}")

    # ==============================
    # TIMELINE
    # ==============================
    st.subheader("Timeline")

    fig_line = px.line(
        df,
        y="Waktu",
        color="Tahap"
    )

    st.plotly_chart(fig_line, use_container_width=True)

    # ==============================
    # AREA CHART
    # ==============================
    st.subheader("Progress Kumulatif")

    df["Step"] = range(len(df))

    fig_area = px.area(
        df,
        x="Step",
        y="Waktu",
        color="Tahap"
    )

    st.plotly_chart(fig_area, use_container_width=True)

    # ==============================
    # PIE
    # ==============================
    st.subheader("Distribusi Tahap")

    tahap = df["Tahap"].value_counts()

    fig_pie = px.pie(
        values=tahap.values,
        names=tahap.index,
        hole=0.4
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    # ==============================
    # PROGRESS BAR TIAP TAHAP
    # ==============================
    st.subheader("Progress Tahap")

    total = len(df)

    for t in tahap.index:

        persen = tahap[t] / total

        st.write(t)

        st.progress(persen)

    # ==============================
    # DOWNLOAD DATA
    # ==============================
    st.subheader("Download Data")

    csv = df.to_csv(index=False)

    st.download_button(
        "Download CSV",
        csv,
        "hasil_simulasi.csv",
        "text/csv"
    )

    # ==============================
    # PERFORMANCE SCORE
    # ==============================
    st.subheader("Performance Score")

    score = max(0, 100 - np.mean(hasil)/3)

    st.progress(score/100)

    st.metric("Score", f"{score:.1f}/100")

    # ==============================
    # STATUS
    # ==============================
    st.subheader("Status Sistem")

    avg = np.mean(hasil)

    if avg < 240:
        st.success("✅ Sistem Sangat Efisien")

    elif avg < 300:
        st.warning("⚠ Sistem Cukup Efisien")

    else:
        st.error("❌ Sistem Tidak Efisien")

    st.balloons()
