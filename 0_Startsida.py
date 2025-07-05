from stripe_utils import create_checkout_session
import streamlit as st
from PIL import Image
from datetime import datetime, timedelta

import streamlit as st
from firebase_config import auth


st.set_page_config(page_title="Investeringsrummet", layout="wide")

st.image("Assets/test.png", width=80)


# ------------------------
# Hero Section
# ------------------------
st.markdown("""
    <div style='text-align: center; padding-top: 30px;'>
        <h1 style='font-size: 3em;'>📈 Investeringsrummet</h1>
        <p style='font-size: 1.2em;'>Datadrivna aktievärderingar med hjälp av Multipel- och DCF-modeller</p>
""", unsafe_allow_html=True)


choice = st.radio("Login eller Registrera", ["Login", "Registrera"])

email = st.text_input("Email")
password = st.text_input("Lösenord", type="password")

if choice == "Registrera":
    if st.button("Registrera"):
        try:
            user = auth.create_user_with_email_and_password(email, password)
            st.success("Konto skapat! Du kan nu logga in.")
        except Exception as e:
            st.error(f"Fel vid registrering: {e}")
elif choice == "Login":
    if st.button("Logga in"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.success(f"Inloggad som {email}")
            st.session_state["user_logged_in"] = True
            st.session_state["user_email"] = email
            st.session_state["account_type"] = "free"
        except Exception as e:
            st.error(f"Fel vid inloggning: {e}")

# Hantera inloggningstillstånd via session_state
if 'user_logged_in' not in st.session_state:
    st.session_state['user_logged_in'] = False

if 'account_type' not in st.session_state:
    st.session_state['account_type'] = None

# Sätt kontotyp baserat på inloggning
if st.session_state.get('user_logged_in'):
    username = "david"

if 'analysis_log' not in st.session_state:
    st.session_state['analysis_log'] = []

if st.session_state.get('account_type') == 'premium':
    if st.button("🚀 Starta analys"):
        st.success("Analys startad!")
        st.markdown("Länk till analysverktyget...")
elif st.session_state.get('user_logged_in'):
    st.warning("🔒 Denna funktion är endast tillgänglig för Premium-användare.")
    if st.button("Uppgradera till Premium"):
        st.info("👉 Uppgraderingsfunktion kommer snart!")
else:
    st.warning("🔑 Logga in för att komma åt analysverktyget.")

st.markdown("""
    </div>
""", unsafe_allow_html=True)

if st.session_state.get("account_type") == "free":
    st.info("Du använder Gratismodellen – uppgradera för mer funktioner 🚀")
    if st.button("💳 Uppgradera till Premium"):
        checkout_url = create_checkout_session(st.session_state["user_email"])
        st.markdown(f"[👉 Klicka här för att betala via Stripe]({checkout_url})", unsafe_allow_html=True)

st.markdown("---")

st.success("🎯 Vill du komma igång direkt? Gå till 'Värderingskalkylator' i menyn till vänster för att starta din analys!")

# ------------------------
# Funktioner
# ------------------------
st.subheader("🧰 Funktioner")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    - 📊 Historiska nyckeltal från Yahoo Finance  
    - 📈 Interaktiva scenariomodeller  
    - 📁 Spara och öppna egna analyser
    """)
with col2:
    st.markdown("""
    - 💾 Exportera till PDF  
    - 🧠 Inbyggd DCF och multipelmodell  
    - 🧮 Egna antaganden och känslighetsanalys
    """)
with col3:
    st.markdown("""
    - 🔒 Din data är din  
    - 🔍 Transparens i datakällor  
    - 🧑‍💻 Byggd med Streamlit
    """)

# ------------------------
# Kontoerbjudanden
# ------------------------
st.markdown("""<h2 id='start-cta'>💼 Kontonivåer</h2>""", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.subheader("💎 Gratismodell")
    st.markdown("""
    ✅ Tillgång till alla verktyg (utom 'Min portfölj')  
    ✅ Export till PDF  
    ✅ Tillgång till historisk aktiedata
    """)
with col2:
    st.subheader("🚀 Premium")
    st.markdown("""
    ✅ Obegränsade analyser  
    ✅ Jämför flera bolag  
    ✅ Tillgång till alla framtida funktioner  
    ✅ Tillgång till 'Min portfölj'
    """)

if st.session_state.get('account_type') == 'premium':
    st.info("Du har **Premium**-åtkomst 🎉")
elif st.session_state.get('account_type') == 'free':
    st.info("Du använder **Gratismodellen** – uppgradera för mer funktioner 🚀")

st.success("🎁 Du får alltid 1 gratis analys varje månad! Logga bara in.")

# ------------------------
# Expanderbar FAQ
# ------------------------
st.markdown("---")
st.subheader("📘 Vanliga frågor")
with st.expander("🔍 Hur fungerar DCF-modellen?"):
    st.write("Vi estimerar framtida kassaflöden och diskonterar dem med ett avkastningskrav för att få ett nuvärde på aktien.")
with st.expander("📊 Vad innebär multipelvärdering?"):
    st.write("Vi jämför bolagets nyckeltal (P/E, EV/EBITDA m.fl.) mot branschsnitt för att uppskatta ett rimligt värde.")

# ------------------------
# Testimonials
# ------------------------
st.markdown("---")
st.subheader("💬 Vad våra användare säger")
col1, col2 = st.columns(2)
with col1:
    st.info("""_\"Jag gillar att kunna justera mina antaganden och direkt se påverkan – supersmidigt!\"_ – Anna, privatinvesterare""")
with col2:
    st.info("""_\"Känns proffsigt och samtidigt enkelt att komma igång med.\"_ – Erik, student""")

# ------------------------
# Avslut
# ------------------------
st.markdown("""
<div style='text-align: center; padding-top: 50px;'>
    <p>🧠 Vill du veta mer om hur våra modeller fungerar? <a href='https://example.com'>📘 Läs mer här</a></p>
</div>
""", unsafe_allow_html=True)

# ------------------------
# Andra verktyg på plattformen
# ------------------------
st.markdown("---")
st.subheader("🧰 Andra verktyg på plattformen")
st.markdown("""
- 🏗️ **Skapa Investmentbolagsportfölj**  
  Bygg din egen investmentbolagsportfölj baserat på aktuella innehav och viktningar.

- 📉 **Investmentbolag - Substansrabatt**  
  Jämför substansrabatter för svenska investmentbolag i realtid.

- 📊 **Min portfölj**  
  Få en översikt över dina egna innehav och analysera dem visuellt och historiskt.
""")

if st.session_state.get('user_logged_in'):
    st.markdown("- 📈 **Värderingskalkylator**  *(Premium)*  \n  Tillgång till DCF och multipelmodeller med egna antaganden.")
else:
    st.markdown("- 🔒 **Värderingskalkylator** *(Premium)*  \n  Logga in för att få tillgång till DCF och multipelmodeller.")

st.markdown("---")

st.markdown("testhhbhbhbhbhbhbhbhbhb.")
st.markdown("---")

st.markdown("🛠️ **Alla verktyg utom värderingskalkylatorn är gratis att använda!** Logga in för att låsa upp premiumfunktioner.")