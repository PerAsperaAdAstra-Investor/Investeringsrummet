import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Mina investeringar")
st.title("📂 Mina Portföljer")

# --- Portföljdata ---
portfolios = {
    "Investmentbolagsportfölj": {
        "data": [
            {"id": "Investor", "label": "Investor",                     "value": 37, "color": "#f4a261"},
            {"id": "Lundbergsföretagen", "label": "Lundbergsföretagen", "value": 17, "color": "#e76f51"},
            {"id": "bure", "label": "Bure",                             "value": 9.7, "color": "#e9c46a"},
            {"id": "Latour", "label": "Latour",                         "value": 8, "color": "#2a9d8f", "pattern": "dots"},
            {"id": "Spiltan Invest", "label": "Spiltan Invest",         "value": 7.8, "color": "#264653", "pattern": "lines"},
            {"id": "Svolder", "label": "Svolder",                       "value": 6, "color": "#f4a261"},
            {"id": "Byggmästare AJA", "label": "Byggmästare AJA",       "value": 5, "color": "#e76f51"},
            {"id": "Creades", "label": "Creades",                       "value": 4, "color": "#e9c46a"},
            {"id": "Traction", "label": "Traction",                     "value": 4, "color": "#2a9d8f", "pattern": "dots"},
            {"id": "Öresund", "label": "Öresund",                       "value": 2.5, "color": "#264653", "pattern": "lines"},
            {"id": "Kinnevik", "label": "Kinnevik",                     "value": 2, "color": "#264653", "pattern": "lines"},
            {"id": "Flat Capital", "label": "Flat Capital",             "value": 1, "color": "#264653", "pattern": "lines"},
        ],
        "comment": "Denna portfölj fokuserar på substansrabatter och långsiktig tillväxt inom svenska investmentbolag."
    },
    "Kapitalförsäkring (utländska aktier)": {
        "data": [
            {"id": "Alphabet", "label": "Alphabet",                     "value": 20, "color": "#8ecae6"},
            {"id": "Microsoft", "label": "Microsoft",                   "value": 15, "color": "#219ebc"},
            {"id": "Amazon", "label": "Amazon",                         "value": 12, "color": "#023047"},
            {"id": "Berkshire Hathaway", "label": "Berkshire Hathaway", "value": 8, "color": "#ffb703"},
            {"id": "Freetrailer", "label": "Freetrailer",               "value": 5, "color": "#fb8500"},
            {"id": "Aker", "label": "Aker",                             "value": 5, "color": "#f4a261"},
            {"id": "Exor", "label": "Exor",                             "value": 4.5, "color": "#e76f51"},
            {"id": "Nvidia", "label": "Nvidia",                         "value": 4, "color": "#e9c46a"},
            {"id": "AMD", "label": "AMD",                               "value": 4, "color": "#2a9d8f"},
            {"id": "Kitron", "label": "Kitron",                         "value": 4, "color": "#264653"},
            {"id": "DNB Bank", "label": "DNB Bank",                     "value": 2, "color": "#023047"},
        ],
        "comment": "Tech-fokuserad portfölj som speglar global tillväxt och innovationskraft."
    },
    "Svensk aktieportfölj": {
        "data": [
            {"id": "Volvo", "label": "Volvo",                   "value": 25, "color": "#6a994e"},
            {"id": "Evolution", "label": "Evolution",           "value": 20, "color": "#a7c957"},
            {"id": "Dynavox group", "label": "Dynavox group",   "value": 15, "color": "#f2e8cf"},
            {"id": "RaySearch", "label": "RaySearch",           "value": 10.5, "color": "#bc4749"},
            {"id": "NP3", "label": "NP3",                       "value": 7, "color": "#9b2226"},
            {"id": "Addnode", "label": "Addnode",               "value": 5, "color": "#f4a261"},
            {"id": "Asker Healthcare", "label": "Asker Healthcare", "value": 5, "color": "#e76f51"},
            {"id": "Vitec", "label": "Vitec",                   "value": 4, "color": "#fb8500"},
            {"id": "Munters", "label": "Munters",               "value": 3.5, "color": "#2a9d8f", "pattern": "dots"},
        ],
        "comment": "Defensiv portfölj med stabila utdelningsaktier och exponering mot fastigheter och industri."
    }
}
modern_colors = ["#1b1f3b", "#2d3142", "#4f5d75", "#bfc0c0", "#ef8354"]

st.markdown("## Översikt")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Kommentar")
    st.write("Denna översikt visar hur det totala sparandet är fördelat mellan olika portföljer.")

with col2:
    st.markdown("Här är en översikt över hur stor andel varje portfölj utgör av det totala sparandet:")

    overview_labels = [
        "Investmentbolag", "Utländska Aktier", "Svenska Aktier", "Index-global","Index-OMXS30"]
    overview_values = [46, 15, 17, 13, 9]
    overview_colors = ["#1b1f3b", "#2d3142", "#4f5d75", "#a9a9a9", "#2d3142"]

    fig_overview, ax_overview = plt.subplots(figsize=(2.5, 2.5))
    fig_overview.patch.set_facecolor('#0e1117')
    ax_overview.set_facecolor('#0e1117')
    wedges, texts, autotexts = ax_overview.pie(
        overview_values,
        labels=overview_labels,
        autopct=lambda pct: f"{pct:.1f}%" if pct > 3 else "",
        colors=overview_colors,
        startangle=90,
        wedgeprops=dict(width=0.5)
    )
    for text in texts + autotexts:
        text.set_color('white')
        text.set_fontname("Times New Roman")
        text.set_fontsize(6)
        text.set_horizontalalignment("center")
        text.set_verticalalignment("center")
    ax_overview.axis("equal")
    st.pyplot(fig_overview)

st.markdown("---")

for name, content in portfolios.items():
    st.markdown(f"## {name}")
    col1, col2 = st.columns([2, 1])

    with col1:
        labels = [entry["label"] for entry in content["data"]]
        values = [entry["value"] for entry in content["data"]]
        colors = modern_colors[:len(values)]

        fig, ax = plt.subplots()
        fig.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#0e1117')
        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            autopct=lambda pct: f"{pct:.1f}%" if pct > 3 else "",
            colors=colors,
            startangle=90,
            wedgeprops=dict(width=0.5)
        )
        for text in texts + autotexts:
            text.set_color('white')
            text.set_fontname("Times New Roman")
            text.set_fontsize(8)
            text.set_horizontalalignment("center")
            text.set_verticalalignment("center")
        ax.axis("equal")
        st.pyplot(fig)

    with col2:
        st.markdown("### Kommentar")
        st.write(content["comment"])

    st.markdown("---")