import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from utils.name_to_ticker import name_to_ticker
from forex_python.converter import CurrencyRates
#from yahooquery import Ticker as YQ_Ticker

# =============================================================================
# 📊 VÄRDERINGSKALKYLATOR
# ==============================================================================

c = CurrencyRates()

def convert(value, from_currency, to_currency="USD"):
    try:
        rate = c.get_rate(from_currency, to_currency)
        return value * rate
    except:
        return value

st.set_page_config(layout="wide")
st.title("Värderingskalkylator")
st.markdown(
    """
    <div style="background-color: #1e1e1e; padding: 1rem; border-radius: 8px;">
        <h4 style="color: white; margin-bottom: 0.5rem;">
            Välkommen till din professionella aktievärderare
            <span style="font-size: 1.2rem; cursor: help;" title="Här analyserar du bolag med hjälp av multipel- och DCF-värdering.">
                ℹ️
            </span>
        </h4>
        <p style="color: #cccccc;">
            Verktyget kombinerar data från YFinance med dina egna antaganden för att ge ett rättvist värde på aktien.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
# Skapa sökbar lista med format "Investor (INVE-B.ST)"
user_input = st.text_input("🔍 Sök bolag eller ticker")
if user_input.upper() in name_to_ticker.values():
    ticker = user_input.upper()
else:
    matches = [t for n, t in name_to_ticker.items() if user_input.lower() in n.lower()]
    if matches:
        ticker = matches[0]
    else:
        ticker = user_input.upper()
if ticker:
    stock = yf.Ticker(ticker)
    #yq_ticker = YQ_Ticker(ticker)
    try:
        info = stock.info
        earnings_date = info.get("earningsDate", None)
        currency = info.get("currency", "USD")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div style='background-color:#111; padding:1rem; border-radius:8px;'>", unsafe_allow_html=True)
            st.metric("Aktiepris", f"{info['currentPrice']} {info['currency']}")
            if earnings_date:
                st.caption(f"Senaste rapport: {earnings_date}")
            st.metric("Börsvärde", f"{round(info['marketCap'] / 1e9, 2)} B")
            st.metric("P/E", info.get("trailingPE", "-"))
            st.metric("Utdelning (%)", info.get("dividendYield", 0))
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div style='background-color:#111; padding:1rem; border-radius:8px;'>", unsafe_allow_html=True)
            st.metric("Sektor", info.get("sector", "-"))
            st.metric("Bransch", info.get("industry", "-"))
            st.metric("P/S", info.get("priceToSalesTrailing12Months", "-"))
            st.metric("Beta", info.get("beta", "-"))
            st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Fel vid hämtning: {e}")
    st.subheader(f"📈 {ticker} – Historisk prisutveckling")
    hist = stock.history(period="5y")
    if not hist.empty:
        fig_price, ax_price = plt.subplots(figsize=(10, 3))
        fig_price.patch.set_facecolor('#0e1117')
        ax_price.set_facecolor('#0e1117')
        ax_price.plot(hist.index, hist["Close"], color="skyblue", label="Pris")
        ax_price.set_title("Pris (5 år)", color="white")
        ax_price.tick_params(colors='white')
        ax_price.spines[:].set_color("white")
        ax_price.grid(True, linestyle='--', alpha=0.3)
        st.pyplot(fig_price)
    with st.expander("📊 Visa mer "):
        st.markdown("---")

        # Finansdata
        fin = stock.financials.T
        fin.index = pd.to_datetime(fin.index)

        revenue = fin["Total Revenue"] if "Total Revenue" in fin.columns else None
        net_income = fin["Net Income"] if "Net Income" in fin.columns else None
        gross_profit = fin["Gross Profit"] if "Gross Profit" in fin.columns else None
        operating_income = fin["Operating Income"] if "Operating Income" in fin.columns else None

        div = stock.dividends
        div_annual = div.resample("Y").sum() if not div.empty else None

        # Tre kolumner för att visa tre grafer sida vid sida
        col1, col2, col3 = st.columns(3)

        with col1:
            if revenue is not None and net_income is not None:
                fig1, ax1 = plt.subplots(figsize=(5, 3))
                fig1.patch.set_facecolor('#0e1117')
                ax1.set_facecolor('#0e1117')
                ax1.bar(revenue.index.year - 0.2, revenue.values / 1e9, width=0.4, label="Omsättning",
                        color="mediumseagreen")
                ax1.bar(net_income.index.year + 0.2, net_income.values / 1e9, width=0.4, label="Vinst",
                        color="gold")
                ax1.set_title(f"{ticker} – Omsättning & Vinst", color="white")
                ax1.set_ylabel("Miljarder", color="white")
                ax1.tick_params(colors='white')
                ax1.spines[:].set_color("white")
                ax1.legend()
                plt.rcParams["font.family"] = "Times New Roman"
                st.pyplot(fig1)

        with col2:
            if div_annual is not None:
                fig2, ax2 = plt.subplots(figsize=(5, 3))
                fig2.patch.set_facecolor('#0e1117')
                ax2.set_facecolor('#0e1117')
                ax2.bar(div_annual.index.year, div_annual.values, color="mediumslateblue")
                ax2.set_title(f"{ticker} – Utdelningar per år", color="white")
                ax2.set_ylabel("Per aktie", color="white")
                ax2.tick_params(colors='white')
                ax2.spines[:].set_color("white")
                st.pyplot(fig2)

        with col3:
            if gross_profit is not None and operating_income is not None:
                fig3, ax3 = plt.subplots(figsize=(5, 3))
                fig3.patch.set_facecolor('#0e1117')
                ax3.set_facecolor('#0e1117')
                ax3.plot(gross_profit.index.year, (gross_profit / revenue * 100), label="Bruttomarginal", color="skyblue")
                ax3.plot(operating_income.index.year, (operating_income / revenue * 100), label="Rörelsemarginal", color="orange")
                ax3.set_title("Marginaler (%)", color="white")
                ax3.set_ylabel("%", color="white")
                ax3.tick_params(colors='white')
                ax3.spines[:].set_color("white")
                ax3.legend()
                st.pyplot(fig3)

        # Nyckeltal från info eller balansräkning
        st.markdown("### 🔍 Nyckeltal")
        try:
            balance_sheet = stock.balance_sheet
            equity = balance_sheet.loc["Total Stockholder Equity"].iloc[0] if "Total Stockholder Equity" in balance_sheet.index else None
            total_assets = balance_sheet.loc["Total Assets"].iloc[0] if "Total Assets" in balance_sheet.index else None
            total_liabilities = balance_sheet.loc["Total Liab"].iloc[0] if "Total Liab" in balance_sheet.index else None
            capital_turnover = revenue.iloc[0] / total_assets if total_assets else None
            roe = net_income.iloc[0] / equity * 100 if equity else None
            roa = net_income.iloc[0] / total_assets * 100 if total_assets else None
            equity_ratio = equity / total_assets * 100 if equity and total_assets else None
            equity_per_share = equity / info.get("sharesOutstanding", 1) if equity else None
            dividend_yield = info.get("dividendYield") * 100 if info.get("dividendYield") else None

            col_a, col_b, col_c = st.columns(3)
            col_d, col_e, col_f = st.columns(3)

            st.markdown("<div style='background-color:#111; padding:1rem; border-radius:8px;'>", unsafe_allow_html=True)
            col_a.metric("Bruttomarginal", f"{(gross_profit.iloc[0] / revenue.iloc[0] * 100):.2f}%" if gross_profit is not None else "–")
            col_b.metric("Rörelsemarginal", f"{(operating_income.iloc[0] / revenue.iloc[0] * 100):.2f}%" if operating_income is not None else "–")
            col_c.metric("Kapitalomsättningshastighet", f"{capital_turnover:.2f}" if capital_turnover else "–")
            col_d.metric("Räntabilitet eget kapital (ROE)", f"{roe:.2f}%" if roe else "–")
            col_e.metric("Räntabilitet totalt kapital (ROA)", f"{roa:.2f}%" if roa else "–")
            col_f.metric("Soliditet", f"{equity_ratio:.2f}%" if equity_ratio else "–")
            st.metric("Eget kapital/aktie", f"{equity_per_share:.2f}" if equity_per_share else "–")
            st.metric("Direktavkastning", f"{dividend_yield:.2f}%" if dividend_yield else "–")
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.warning(f"Något gick fel vid beräkning av nyckeltal: {e}")
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1:
        try:
            ps = info.get("revenueGrowth", None)
            st.markdown("Omsättningstillväxt <span title='Hur mycket omsättningen ökat senaste 12 månaderna'>ℹ️</span>", unsafe_allow_html=True)
            st.metric("", f"{ps * 100:.2f}%" if ps else "–")
        except:
            st.markdown("Omsättningstillväxt <span title='Hur mycket omsättningen ökat senaste 12 månaderna'>ℹ️</span>", unsafe_allow_html=True)
            st.metric("", "–")

    with col_g2:
        try:
            fin = stock.financials
            revenue = fin.loc["Total Revenue"].iloc[0]
            net_income = fin.loc["Net Income"].iloc[0]
            margin = net_income / revenue
            st.markdown("Vinstmarginal <span title='Andel av omsättningen som blir vinst (netto)'>ℹ️</span>", unsafe_allow_html=True)
            st.metric("", f"{margin * 100:.2f}%")
        except:
            st.markdown("Vinstmarginal <span title='Andel av omsättningen som blir vinst (netto)'>ℹ️</span>", unsafe_allow_html=True)
            st.metric("", "–")

    with col_g3:
        try:
            pe = info.get("trailingPE", None)
            st.markdown("P/E multipel <span title='Pris/vinst-tal – hur många gånger årsvinsten du betalar för aktien'>ℹ️</span>", unsafe_allow_html=True)
            st.metric("", f"{pe:.2f}" if pe else "–")
        except:
            st.markdown("P/E multipel <span title='Pris/vinst-tal – hur många gånger årsvinsten du betalar för aktien'>ℹ️</span>", unsafe_allow_html=True)
            st.metric("", "–")
    # --- LAYOUT MED ANTAGANDEN ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='big-font'>Pessimistiskt scenario</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='big-font'>Medel (%)</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='big-font'>Optimistiskt scenario</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    # Kolumn 1
    with col1:
        rev_growth_low = st.number_input(
            "Omsättningstillväxt (%) - Låg 🔧",
            value=ps * 100 - 2,
            step=1.0,
            help="Din uppskattade tillväxt för ett pessimistiskt scenario."
        )
        profit_margin_low = st.number_input(
            "Vinstmarginal (%) - Låg 🔧",
            value=margin * 100 - 1,
            step=1.0,
            help="Din uppskattade vinstmarginal för ett pessimistiskt scenario."
        )
        pe_low = st.number_input(
            "P/E multipel - Låg 🔧",
            value=pe - 2,
            step=1.0,
            help="Din uppskattning av vilken P/E-multipel marknaden ger i ett pessimistiskt scenario."
        )

    # Kolumn 2
    with col2:
        rev_growth_mid = st.number_input(
            "Omsättningstillväxt (%) - Medel 🔧",
            value=ps * 100,
            step=1.0,
            help="Din uppskattade tillväxt i ett normalscenario."
        )
        profit_margin_mid = st.number_input(
            "Vinstmarginal (%) - Medel 🔧",
            value=margin * 100,
            step=1.0,
            help="Din uppskattade vinstmarginal i ett normalscenario."
        )
        pe_mid = st.number_input(
            "P/E multipel - Medel 🔧",
            value=pe,
            step=1.0,
            help="Din uppskattning av vilken P/E-multipel marknaden ger i ett normalscenario."
        )

    # Kolumn 3
    with col3:
        rev_growth_high = st.number_input(
            "Omsättningstillväxt (%) - Hög 🔧",
            value=ps * 100 + 2,
            step=1.0,
            help="Din uppskattade tillväxt för ett optimistiskt scenario."
        )
        profit_margin_high = st.number_input(
            "Vinstmarginal (%) - Hög 🔧",
            value=margin * 100 + 1,
            step=1.0,
            help="Din uppskattade vinstmarginal för ett optimistiskt scenario."
        )
        pe_high = st.number_input(
            "P/E multipel - Hög 🔧",
            value=pe + 3,
            step=1.0,
            help="Din uppskattning av vilken P/E-multipel marknaden ger i ett optimistiskt scenario."
        )

    # Liggande layout på två rader
    row1_col1, row1_col2 = st.columns([1, 1])
    with row1_col1:
        forecast_years = st.slider(
            "Antal år för prognos 🔧",
            1,
            20,
            10,
            help="Hur många år framåt du vill prognostisera tillväxt och vinst."
        )
    with row1_col2:
        req_col, info_col = st.columns([10, 1])
        with req_col:
            req_return = st.number_input(
                "Avkastningskrav (%) 🔧",
                value=9.0,
                step=1.0,
                help="Detta är den avkastning du kräver varje år. Ju högre krav, desto lägre blir nuvärdet av framtida vinster."
            )
        with info_col:
            st.markdown(
                "<span style='font-size: 20px; cursor: help;' title='Detta är den avkastning du kräver varje år. Ju högre krav, desto lägre blir nuvärdet av framtida vinster. Används för att diskontera framtida värde till idag.'>ℹ️</span>",
                unsafe_allow_html=True
            )

    # Gemensamt
    current_price = info.get("currentPrice", 100.0)
    sales = info.get("totalRevenue", 3e10) / 1e6
    shares_outstanding = info.get("sharesOutstanding", 1e9) / 1e6


    # --- VÄRDERINGSKALKYLATOR ---

    def intrinsic_value(growth, margin, pe, years, required_return):
        earnings = convert(sales, from_currency=currency, to_currency="USD") * ((1 + growth / 100) ** years) * (margin / 100)
        terminal_value = earnings * pe
        discount_factor = (1 + required_return / 100) ** years
        value = terminal_value / discount_factor
        # converted_value = convert(value, from_currency="USD", to_currency=currency)  # Already converted sales to USD above
        return value / shares_outstanding

    values = {
        "Låg": intrinsic_value(rev_growth_low, profit_margin_low, pe_low, forecast_years, req_return),
        "Medel": intrinsic_value(rev_growth_mid, profit_margin_mid, pe_mid, forecast_years, req_return),
        "Hög": intrinsic_value(rev_growth_high, profit_margin_high, pe_high, forecast_years, req_return)
    }

    years = forecast_years
    converted_current_price = convert(current_price, from_currency=currency, to_currency="USD")
    cpr = {k: ((v / converted_current_price) ** (1/years) - 1) * 100 for k, v in values.items()}

    returns = {k: ((v - converted_current_price) / converted_current_price * 100) for k, v in values.items()}

    def fmt(val):
        symbol = {"USD": "$", "SEK": "kr", "NOK": "kr", "DKK": "kr", "EUR": "€"}.get(currency, "")
        converted_val = convert(val, from_currency="USD", to_currency=currency)
        return f"{converted_val:.2f} {symbol}"

    # --- PRESENTATION ---
    st.markdown("---")
    st.subheader("Värderingsresultat")
    with st.expander("ℹ️ Hur fungerar detta?"):
        st.markdown("""
        Det här värdet är ett **estimerat pris per aktie** efter prognosperioden (t.ex. 10 år). 
        Det bygger på dina antaganden om tillväxt, vinstmarginal och vilken P/E-multipel marknaden kommer att ge bolaget då.
        
        Exempelvis betyder ett värde på *176 kr* att om bolaget växer enligt dina antaganden och marknaden värderar det enligt ditt P/E-tal, 
        så är 176 kr ett rimligt pris per aktie om 10 år.
        
        Den **årliga avkastningen (CPR)** visar vilken årlig avkastning detta motsvarar utifrån nuvarande aktiekurs.
        """)

    col_low, col_mid, col_high = st.columns(3)
    for col, label, key in zip(
        [col_low, col_mid, col_high],
        ["Lågt scenario", "Medel scenario", "Optimistiskt scenario"],
        ["Låg", "Medel", "Hög"]
    ):
        col.markdown("<div style='background-color:#111; padding:1rem; border-radius:8px;'>", unsafe_allow_html=True)
        col.metric(label, fmt(values[key]), f"{returns[key]:.2f}%")
        col.metric("Årlig avkastning (CPR)", f"{cpr[key]:.2f}%")
        col.markdown("</div>", unsafe_allow_html=True)

    # --- DCF ---
    st.markdown("---")
    st.subheader("📘 DCF-värdering (Diskonterade kassaflöden)")
    st.markdown("#### DCF-antaganden")
    st.caption("Värden nedan påverkar kassaflödesprognosen. De är **användarens egna inmatningar**.")

    st.markdown("#### Antaganden för DCF-scenarier")

    dcf_col1, dcf_col2, dcf_col3 = st.columns(3)
    with dcf_col1:
        fcf_growth_low = st.number_input("FCF-tillväxt (%) - Låg", value=4.0)
        fcf_margin_low = st.number_input("FCF-marginal (%) - Låg", value=8.0)
    with dcf_col2:
        fcf_growth_mid = st.number_input("FCF-tillväxt (%) - Medel", value=6.0)
        fcf_margin_mid = st.number_input("FCF-marginal (%) - Medel", value=10.0)
    with dcf_col3:
        fcf_growth_high = st.number_input("FCF-tillväxt (%) - Hög", value=8.0)
        fcf_margin_high = st.number_input("FCF-marginal (%) - Hög", value=12.0)

    terminal_growth = st.number_input(
        "Terminal tillväxt (%) 🔧",
        value=2.0,
        step=1.0,
        help="Antagen långsiktig tillväxttakt efter prognosperioden (terminal tillväxt)."
    )

    def dcf_value_calc(growth, margin):
        fcf = sales * margin / 100
        val = sum(
            fcf * ((1 + growth / 100) ** t) / ((1 + req_return / 100) ** t)
            for t in range(1, forecast_years + 1)
        )
        terminal = fcf * ((1 + growth / 100) ** forecast_years) * (1 + terminal_growth / 100) / (
            req_return / 100 - terminal_growth / 100)
        val += terminal / ((1 + req_return / 100) ** forecast_years)
        return val / shares_outstanding

    values_dcf = {
        "Låg": dcf_value_calc(fcf_growth_low, fcf_margin_low),
        "Medel": dcf_value_calc(fcf_growth_mid, fcf_margin_mid),
        "Hög": dcf_value_calc(fcf_growth_high, fcf_margin_high),
    }

    dcf_returns = {k: ((v - current_price) / current_price * 100) for k, v in values_dcf.items()}
    dcf_cpr = {k: ((v / current_price) ** (1/forecast_years) - 1) * 100 for k, v in values_dcf.items()}

    st.markdown("#### Resultat: DCF per scenario")
    col_low, col_mid, col_high = st.columns(3)
    for col, label, key in zip(
        [col_low, col_mid, col_high],
        ["Lågt scenario", "Medel scenario", "Optimistiskt scenario"],
        ["Låg", "Medel", "Hög"]
    ):
        col.markdown("<div style='background-color:#111; padding:1rem; border-radius:8px;'>", unsafe_allow_html=True)
        col.metric("DCF-värde per aktie", fmt(values_dcf[key]), f"{dcf_returns[key]:.2f}%")
        col.metric("Årlig avkastning (CPR)", f"{dcf_cpr[key]:.2f}%")
        col.markdown("</div>", unsafe_allow_html=True)

    st.caption(
        "Denna modell bygger på förenklade antaganden och tar inte hänsyn till balansräkning eller kassaflöden. Använd som ett verktyg, inte ett investeringsråd.")
