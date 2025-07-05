import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.ibindex_mock import MOCK_DATA

# =============================================================================
# 📊 INVESTMENTBOLAGSPORTFÖLJ
# ==============================================================================

st.title("Simulator av investmentbolags-portfölj")

st.write("Ange andel i (%) av varje investmentbolag för se viktningen av alla underliggande tillgångar:")

user_weights = {}
total_sum = 0

for bolag in MOCK_DATA:
    col1, col2 = st.columns([1, 1])  # eller justera till [2,1] om du vill ha mer plats för namn
    with col1:
        st.markdown(f"<div style='margin-top: 8px'>{bolag}</div>", unsafe_allow_html=True)
    with col2:
        vikt = st.number_input(
            label=" ",  # tom label = ingen labelrad visas
            min_value=0.0,
            max_value=100.0,
            step=1.0,
            key=bolag,
            label_visibility="collapsed"  # viktig!
        )
    user_weights[bolag] = vikt / 100
    total_sum += vikt

if st.button("Skapa portfölj"):

    if total_sum == 0:
        st.warning("Du måste ange minst en andel.")
    else:
        combined_holdings = {}
        total_discount = 0
        total_fee = 0

        for bolag, vikt in user_weights.items():
            if vikt > 0:
                data = MOCK_DATA[bolag]
                for innehav, andel in data["holdings"].items():
                    combined_holdings[innehav] = combined_holdings.get(innehav, 0) + andel * vikt
                total_discount += data["discount"] * vikt
                total_fee += data.get("fee", 0) * vikt

        # Skapa DataFrame för diagram
        df = pd.DataFrame.from_dict(combined_holdings, orient="index", columns=["Vikt"])
        df["Vikt"] = df["Vikt"] / sum(df["Vikt"])  # normalisera till 100%
        df = df[df["Vikt"] > 0]  # ta bort negativa värden om några
        df = df.sort_values("Vikt", ascending=False)

        plt.rcParams["font.family"] = "Times New Roman"


        # Funktion för att dölja små värden
        def autopct_format(pct):
            return f"{pct:.1f}%" if pct >= 0.5 else ""


        labels = [name if weight >= 1 else "" for name, weight in zip(df.index, df["Vikt"])]

        # Visa cirkeldiagram med modern och mörkare färgschema
        colors = [
            "#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51",
            "#6a4c93", "#4a5759", "#6e44ff", "#b388eb", "#9c89b8"
        ]
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(
            df["Vikt"],
            labels=df.index,
            autopct=autopct_format,
            startangle=90,
            colors=colors,
            textprops=dict(color="white", fontsize=10)
        )
        for text in texts:
            text.set_fontname("Times New Roman")
        for autotext in autotexts:
            autotext.set_fontname("Times New Roman")
            autotext.set_color("white")
            autotext.set_fontsize(10)
            autotext.set_horizontalalignment('center')
        ax.axis("equal")
        fig.patch.set_facecolor("none")
        st.pyplot(fig)

        # Visa substansrabatt
        st.markdown(f"### Genomsnittlig substansrabatt: **{total_discount:.2f}%**")
        # Visa förvaltningsavgift:
        st.markdown(f"### Genomsnittlig förvaltningsavgift: **{total_fee:.2f}%**")

        st.dataframe(df.style.format({"Vikt": "{:.2%}"}))