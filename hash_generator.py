import streamlit_authenticator as stauth

# Ersätt '123' med ditt riktiga lösenord
hashed_passwords = stauth.Hasher(['123']).generate()
print(hashed_passwords)