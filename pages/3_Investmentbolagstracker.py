import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from utils.name_to_ticker import name_to_ticker
from utils.ibindex_mock import MOCK_DATA
st.title("📉 Investmentbolagstracker")
st.set_page_config(layout="wide")
# Kompakt översiktstabell
st.markdown("## 📋 Översikt")
overview_data = []
for name, info in MOCK_DATA.items():
    discount = info.get("discount")
    fee = info.get("fee")
    overview_data.append((name, discount, fee))

overview_df = pd.DataFrame(overview_data, columns=["Bolag", "Substansrabatt (%)", "Förvaltningsavgift (%)"])
overview_df = overview_df.sort_values("Bolag")

# Visa tabellen i vänsterspalten
col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        <style>
            .element-container:has(.stDataFrame) {
                max-width: 100% !important;
                width: 100% !important;
                margin-left: 0 !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.dataframe(
        overview_df.style.format({
            "Substansrabatt (%)": "{:.1f} %",
            "Förvaltningsavgift (%)": "{:.2f} %"
        }),
        use_container_width=True
    )
with col2:
    st.image("Assets/Investor.png", width=150)
    st.image("Assets/Lundberg.png", width=150)
    st.image("Assets/Latour.jpg", width=150)
    st.image("Assets/Bure.png", width=150)



market_caps = {}
for name, ticker in name_to_ticker.items():
    try:
        data = yf.Ticker(ticker).info
        market_caps[name] = data.get("marketCap", None)
    except Exception:
        market_caps[name] = None

from utils.ibindex_mock import MOCK_DATA  # säkerställ att denna fil är uppdaterad

col1, col2 = st.columns(2)
with col1:
    st.subheader("🧾 Detaljerad översikt per bolag")
    for name, info in MOCK_DATA.items():
        with st.expander(name):
            discount = info.get("discount")
            fee = info.get("fee")
            mcap = market_caps.get(name)
            holdings = info.get("holdings", {})

            st.markdown(f"- **Substansrabatt:** {discount:.1f}%")
            st.markdown(f"- **Förvaltningsavgift:** {fee:.2f}%")
            if mcap:
                st.markdown(f"- **Börsvärde:** {mcap / 1e9:.2f} miljarder SEK")

            if holdings:
                df = pd.DataFrame(holdings.items(), columns=["Innehav", "Andel (%)"])
                fig = px.pie(df, names="Innehav", values="Andel (%)", title="Innehavsfördelning")
                st.plotly_chart(fig, use_container_width=True)


st.subheader("📊 Jämförelse av substansrabatter")
bar_data = {
    name: info.get("discount", 0)
    for name, info in MOCK_DATA.items()
    if info.get("discount") is not None
}
bar_df = pd.DataFrame(bar_data.items(), columns=["Bolag", "Substansrabatt"])
fig_bar = px.bar(bar_df, x="Bolag", y="Substansrabatt", color="Substansrabatt", title="Substansrabatt per bolag")
st.plotly_chart(fig_bar, use_container_width=True)

st.subheader("📈 Aktiekurser")
selected = st.multiselect("Välj bolag att visa", options=list(name_to_ticker.keys()))
if selected:
    df_prices = pd.DataFrame()
    for name in selected:
        try:
            ticker = name_to_ticker[name]
            hist = yf.Ticker(ticker).history(period="5y")["Close"]
            df_prices[name] = hist
        except:
            continue
    if not df_prices.empty:
        st.line_chart(df_prices)

st.markdown("---")
st.markdown("### 📊 Vill du bygga en egen investmentbolagsportfölj?")
if st.button("Gå till portföljsidan"):
    st.session_state.page = "Investmentbolagsportfölj"
