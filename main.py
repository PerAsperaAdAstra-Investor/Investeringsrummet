
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Ladda config
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initiera autentisering
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

# Inloggning
name, authentication_status, username = authenticator.login("Logga in", location="sidebar")

if authentication_status is False:
    st.error("Fel användarnamn eller lösenord")
elif authentication_status is None:
    st.warning("Ange användarnamn och lösenord")
elif authentication_status:
    authenticator.logout("Logga ut", "sidebar")
    st.success(f"Välkommen {name}!")
    st.markdown("Navigera med menyn till vänster för att använda appens funktioner.")