import streamlit as st
from PyPDF2 import PdfReader
import openai


def show_case_coach():
    st.title("📚 Business Case Solver")

    st.markdown("Ladda upp ett case eller börja direkt med våra guider.")

    uploaded_file = st.file_uploader("Ladda upp ett case (PDF eller textfil)", type=["pdf", "txt"])

    case_text = ""

    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            reader = PdfReader(uploaded_file)
            case_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif uploaded_file.type == "text/plain":
            case_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type in ["application/xml", "application/octet-stream"]:
            import urllib.request
            import xml.etree.ElementTree as ET
            content = uploaded_file.read().decode("utf-8")
            try:
                tree = ET.fromstring(content)
                url = tree.findtext(".//string")
                with urllib.request.urlopen(url) as response:
                    case_text = response.read().decode("utf-8")
            except Exception as e:
                case_text = f"Kunde inte läsa innehållet från länk: {e}"

        st.subheader("📄 Utdrag från ditt case:")
        st.write(case_text[:1500] + "..." if len(case_text) > 1500 else case_text)

        # AI-analys/Case-lösning
        if st.button("🧠 Lös mitt case med AI"):
            with st.spinner("AI analyserar caset..."):
                system_prompt = """
                Du är en affärsstrategisk expert med lång erfarenhet av case-lösning på toppnivå, likt McKinsey, Bain eller BCG.

                Analysobjektet är ett business case (se texten nedan). Du ska göra följande i strukturerade steg:

                1. 📄 SAMMANFATTNING:
                Vad handlar caset om? Vad är huvudfrågan? Sammanfatta kort (max 5 meningar).

                2. 🔍 INSIGHTS (marknadsanalys + företag):
                Gör en djupgående analys av branschen och företaget. Använd uppdaterad data och ange tydliga källor (ex. IEA, PwC, McKinsey, Statista).
                - Vilka trender driver industrin?
                - Hur ser konkurrenssituationen ut?
                - Vilka är de största möjligheterna/hoten?
                - Hur är företagets nuvarande position?

                3. 🧠 STRATEGY:
                Föreslå en tydlig strategisk lösning på caset baserat på företagsanalysen och externa faktorer. Använd gärna Porter's Value Chain eller Business Model Canvas.

                4. 🛠️ IMPLEMENTATION:
                - Tidsplan steg-för-steg
                - Nyckelresurser
                - Riskanalys och mitigering

                5. 📈 IMPACT:
                Estimera finansiell påverkan (EBIT, tillväxt etc.) samt mjuk påverkan (branding, kundnöjdhet, hållbarhet). Kvantifiera om möjligt.
                """

                user_message = f"Casetext:\n{case_text}"

                from openai import OpenAI
                from decouple import config
                client = OpenAI(api_key=config("OPENAI_API_KEY"))

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.5,
                )

                ai_output = response.choices[0].message.content
                st.markdown("## 🧠 AI Case-lösning:")
                st.markdown(ai_output)

show_case_coach()