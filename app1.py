# ROAD-SENTRY DASHBOARD
# Computer Vision Road Damage Detection

import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIG

st.set_page_config(
    page_title="ROAD-SENTRY Dashboard",
    page_icon="",
    layout="wide"
)

# COLOR PALETTE

ROAD_COLORS = [
    "#2563EB",  # Crack
    "#F59E0B",  # Pothole
    "#DC2626"   # Manhole
]

# STYLING

st.markdown("""
<style>

.main {
    background-color: #F8FAFC;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

h1 {
    color: #0F172A;
    font-weight: 700;
}

h2, h3 {
    color: #1E293B;
    font-weight: 600;
}

p {
    color: #475569;
}

[data-testid="stSidebar"] {
    background-color: #0F172A;
}

[data-testid="stSidebar"] * {
    color: white;
}

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 18px;
}

[data-testid="stDataFrame"] {
    border: 1px solid #E2E8F0;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# LOAD DATA

dataset_summary = pd.read_csv("dataset_summary.csv")
class_distribution = pd.read_csv("class_distribution.csv")
severity_distribution = pd.read_csv("severity_distribution.csv")
severity_class = pd.read_csv("severity_class.csv")
ab_testing = pd.read_csv("ab_testing_summary.csv")

# SIDEBAR

st.sidebar.markdown("""
## ROAD-SENTRY

Road Infrastructure Monitoring System
""")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Dataset Summary",
        "EDA",
        "Feature Engineering",
        "A/B Testing",
        "Business Questions",
        "Conclusion"
    ]
)

# OVERVIEW

if page == "Overview":

    st.title("ROAD-SENTRY")
    st.caption("Road Damage Detection and Infrastructure Monitoring Dashboard")

    st.divider()

    st.markdown("""
### Road Damage Detection using Computer Vision

ROAD-SENTRY merupakan sistem deteksi kerusakan jalan berbasis GIS dan
Computer Vision yang bertujuan membantu proses identifikasi kerusakan
jalan secara otomatis melalui analisis citra jalan.

Dashboard ini menampilkan hasil proses Data Science mulai dari:

- Data Wrangling
- Data Quality Assessment
- Exploratory Data Analysis (EDA)
- Feature Engineering
- A/B Testing
- Business Insight
""")

    st.divider()

    st.subheader("Dataset Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Images", "2,009")

    with col2:
        st.metric("Annotated Objects", "4,737")

    with col3:
        st.metric("Damage Classes", "3")

    with col4:
        st.metric("Data Quality Score", "100%")

# DATASET SUMMARY

elif page == "Dataset Summary":

    st.title("Dataset Summary")

    st.dataframe(dataset_summary, use_container_width=True)

    with st.container(border=True):
        st.subheader("Key Findings")
        st.write("""
Dataset terdiri dari 2009 citra jalan dengan total 4737 objek yang
terbagi ke dalam tiga kategori kerusakan: pothole, crack, dan manhole.
""")

# EDA

elif page == "EDA":

    st.title("Exploratory Data Analysis")

    fig = px.bar(
        class_distribution,
        x="Class",
        y="Count",
        text="Count",
        color="Class",
        color_discrete_sequence=ROAD_COLORS,
        title="Distribution of Road Damage Classes"
    )

    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.pie(
        class_distribution,
        names="Class",
        values="Count",
        color_discrete_sequence=ROAD_COLORS,
        title="Percentage Distribution of Classes"
    )

    st.plotly_chart(fig2, use_container_width=True)

    with st.container(border=True):
        st.subheader("Key Findings")
        st.write("""
Crack merupakan class yang paling dominan dengan total 2519 objek.

Pothole berada pada urutan kedua dengan 1261 objek.

Manhole merupakan class dengan jumlah objek paling sedikit yaitu 957 objek.
""")

# FEATURE ENGINEERING

elif page == "Feature Engineering":

    st.title("Feature Engineering")

    st.subheader("Bounding Box Statistics")

    bbox_df = pd.DataFrame({
        "Metric": ["Mean Area", "Median Area", "Maximum Area"],
        "Value": [0.019997, 0.007379, 0.916667]
    })

    st.dataframe(bbox_df, use_container_width=True)

    with st.container(border=True):
        st.subheader("Key Findings")
        st.write("""
Sebagian besar objek memiliki ukuran relatif kecil, namun terdapat
beberapa objek berukuran besar yang menyebabkan distribusi area menjadi
right-skewed.
""")

    st.subheader("Damage Severity Distribution")

    fig3 = px.pie(
        severity_distribution,
        names="Severity",
        values="Count",
        color_discrete_sequence=["#2563EB", "#F59E0B", "#DC2626"],
        title="Damage Severity Distribution"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Severity per Class")

    st.dataframe(severity_class, use_container_width=True)

    severity_long = severity_class.melt(
        id_vars="Severity",
        var_name="Class",
        value_name="Count"
    )

    fig4 = px.bar(
        severity_long,
        x="Severity",
        y="Count",
        color="Class",
        barmode="group",
        color_discrete_sequence=ROAD_COLORS,
        title="Severity Distribution by Class"
    )

    st.plotly_chart(fig4, use_container_width=True)

    with st.container(border=True):
        st.subheader("Key Findings")
        st.write("""
- Crack mendominasi kategori Large.
- Pothole dominan pada kategori Small dan Medium.
- Manhole hampir seluruhnya berada pada kategori Small dan Medium.
""")

# A/B TESTING

elif page == "A/B Testing":

    st.title("A/B Testing")

    st.dataframe(ab_testing, use_container_width=True)

    ab_long = ab_testing.melt(
        id_vars="Aspect",
        var_name="Experiment",
        value_name="Score"
    )

    fig5 = px.bar(
        ab_long,
        x="Aspect",
        y="Score",
        color="Experiment",
        barmode="group",
        color_discrete_sequence=["#2563EB", "#64748B"],
        title="Experiment A vs Experiment B"
    )

    st.plotly_chart(fig5, use_container_width=True)

    with st.container(border=True):
        st.subheader("Key Findings")
        st.write("""
Experiment A hanya menggunakan informasi class.

Experiment B menggunakan informasi class dan severity.

Hasil menunjukkan bahwa Feature Engineering menghasilkan insight yang
lebih kaya dan meningkatkan nilai analisis dataset.
""")

# BUSINESS QUESTIONS

elif page == "Business Questions":

    st.title("Business Questions")

    with st.container(border=True):
        st.subheader(
            "1. Bagaimana distribusi jenis kerusakan jalan pada dataset yang digunakan untuk pengembangan sistem ROAD-SENTRY?"
        )
        st.write("""
Hasil analisis menunjukkan bahwa Crack merupakan jenis kerusakan yang
paling dominan pada dataset, diikuti oleh Pothole dan Manhole.
""")

    with st.container(border=True):
        st.subheader(
            "2. Apakah dataset yang digunakan telah memenuhi kualitas data yang diperlukan untuk mendukung pengembangan model deteksi kerusakan jalan pada sistem ROAD-SENTRY?"
        )
        st.write("""
Berdasarkan proses Data Quality Assessment, tidak ditemukan missing image,
missing label, maupun corrupted image.
""")

    with st.container(border=True):
        st.subheader(
            "3. Apakah karakteristik dataset yang digunakan sudah memadai untuk diproses pada tahap pelatihan model AI ROAD-SENTRY?"
        )
        st.write("""
Dataset memiliki jumlah citra dan objek yang memadai, distribusi kelas
yang jelas, serta informasi tambahan berupa tingkat keparahan.
""")

# CONCLUSION

elif page == "Conclusion":

    st.title("Final Conclusion")

    with st.container(border=True):
        st.markdown("""
### Summary

1. Crack merupakan jenis kerusakan jalan yang paling dominan.

2. Dataset memiliki kualitas yang sangat baik tanpa missing image,
missing label, maupun corrupted image.

3. Feature Engineering menghasilkan informasi tingkat keparahan
kerusakan.

4. Dataset memadai untuk mendukung pelatihan model AI.

5. Dataset siap digunakan sebagai dasar pengembangan model Computer
Vision untuk deteksi kerusakan jalan.
""")

# FOOTER

st.markdown("---")

st.caption(
    "ROAD-SENTRY Dashboard | Data Science Project | Computer Vision Road Damage Detection"
)
