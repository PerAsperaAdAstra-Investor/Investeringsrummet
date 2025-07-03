import streamlit as st
from PIL import Image
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

name, authentication_status, username = authenticator.login("Logga in", "sidebar")

if authentication_status == False:
    st.error("Fel användarnamn eller lösenord")
if authentication_status == None:
    st.warning("Vänligen logga in för att använda alla funktioner")

st.set_page_config(page_title="Investeringsrummet", layout="wide")

# ------------------------
# Hero Section
# ------------------------
st.markdown("""
    <div style='text-align: center; padding-top: 30px;'>
        <h1 style='font-size: 3em;'>📈 Investeringsrummet</h1>
        <p style='font-size: 1.2em;'>Datadrivna aktievärderingar med hjälp av Multipel- och DCF-modeller</p>
        <a href='#start-cta'>
            <button style='font-size: 1.1em; padding: 10px 25px; background-color: #0072E3; color: white; border: none; border-radius: 5px;'>🚀 Starta din första analys</button>
        </a>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

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
    ✅ 1 gratis analys per vecka  
    ✅ Tillgång till historisk data  
    ✅ Export till PDF
    """)
with col2:
    st.subheader("🚀 Premium")
    st.markdown("""
    ✅ Obegränsade analyser  
    ✅ Jämför flera bolag  
    ✅ Tillgång till alla framtida funktioner
    """)

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

if authentication_status:
    st.markdown("- 📈 **Värderingskalkylator**  *(Premium)*  \n  Tillgång till DCF och multipelmodeller med egna antaganden.")
else:
    st.markdown("- 🔒 **Värderingskalkylator** *(Premium)*  \n  Logga in för att få tillgång till DCF och multipelmodeller.")

st.markdown("---")
st.markdown("🛠️ **Alla verktyg utom värderingskalkylatorn är gratis att använda!** Logga in för att låsa upp premiumfunktioner.")
