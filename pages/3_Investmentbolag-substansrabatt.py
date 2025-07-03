import streamlit as st

st.title("📉 Substansrabatter för investmentbolag")

from utils.ibindex_mock import MOCK_DATA  # säkerställ att denna fil är uppdaterad
    # Färgsättning av rabatt/premium
import streamlit as st

st.subheader("📊 Substansrabatter & Förvaltningsavgifter")

    # Headerrad
cols = st.columns([3, 2, 2])
cols[0].markdown("**Bolagsnamn**")
cols[1].markdown("**Substansrabatt**")
cols[2].markdown("**Förvaltningsavgift**")

# Data
for name, info in MOCK_DATA.items():
    discount = info.get("discount")
    fee = info.get("fee")  # kräver att du lagt till 'fee' i MOCK_DATA

        # Färgkodning
    if discount is not None:
        discount_color = "green" if discount > 0 else "red"
        formatted_discount = f"<span style='color:{discount_color}'>{discount:.1f} %</span>"
    else:
        formatted_discount = "–"

    formatted_fee = f"{fee:.2f} %" if fee is not None else "–"

    cols = st.columns([3, 2, 2])
    cols[0].markdown(name)
    cols[1].markdown(formatted_discount, unsafe_allow_html=True)
    cols[2].markdown(formatted_fee)


st.markdown("---")
st.markdown("### 📊 Vill du bygga en egen investmentbolagsportfölj?")
if st.button("Gå till portföljsidan"):
    st.session_state.page = "Investmentbolagsportfölj"
