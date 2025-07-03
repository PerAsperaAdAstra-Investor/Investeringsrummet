
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from utils.name_to_ticker import name_to_ticker
from forex_python.converter import CurrencyRates
#from yahooquery import Ticker as YQ_Ticker
from firebase_config import auth

# Inloggning med Pyrebase
if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    with st.form("login"):
        email = st.text_input("Email")
        password = st.text_input("Lösenord", type="password")
        submit = st.form_submit_button("Logga in")

        if submit:
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.user = user
                st.success("Inloggad!")
                st.experimental_rerun()
            except:
                st.error("Fel email eller lösenord.")
    st.stop()

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
            st.markdown(
                f"""
                <div style='background-color:#111; padding:0.5rem 1rem; border-radius:6px; font-size:0.85rem; color:white'>
                    <b>Aktiepris:</b> {info['currentPrice']} {info['currency']}<br>
                    <b>Börsvärde:</b> {round(info['marketCap'] / 1e9, 1)} B<br>
                    <b>P/E:</b> {info.get("trailingPE", "-")}<br>
                    <b>Utdelning:</b> {round(info.get("dividendYield", 0) * 100, 2)}%
                </div>
                """, unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div style='background-color:#111; padding:0.5rem 1rem; border-radius:6px; font-size:0.85rem; color:white'>
                    <b>Sektor:</b> {info.get("sector", "-")}<br>
                    <b>Bransch:</b> {info.get("industry", "-")}<br>
                    <b>P/S:</b> {round(info.get("priceToSalesTrailing12Months", 0), 2)}<br>
                    <b>Beta:</b> {info.get("beta", "-")}
                </div>
                """, unsafe_allow_html=True
            )
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
                # Ensure full 10-year historical data (not just tail of available data)
                # Get last 10 years by sorting and slicing, keeping alignment
                revenue_sorted = revenue.sort_index()
                net_income_sorted = net_income.sort_index()
                if len(revenue_sorted) >= 10 and len(net_income_sorted) >= 10:
                    years = revenue_sorted.index.year[-10:]
                    revenue_vals = (revenue_sorted / 1e9).values[-10:]
                    net_income_vals = (net_income_sorted / 1e9).values[-10:]
                else:
                    years = revenue_sorted.index.year
                    revenue_vals = (revenue_sorted / 1e9).values
                    net_income_vals = (net_income_sorted / 1e9).values
                fig1 = go.Figure()
                fig1.add_trace(go.Bar(
                    x=years - 0.2, y=revenue_vals, name="Omsättning", marker_color='mediumseagreen',
                    hovertemplate='Omsättning: %{y:.2f} Mdr<br>År: %{x}<extra></extra>'
                ))
                fig1.add_trace(go.Bar(
                    x=years + 0.2, y=net_income_vals, name="Vinst", marker_color='gold',
                    hovertemplate='Vinst: %{y:.2f} Mdr<br>År: %{x}<extra></extra>'
                ))
                fig1.update_layout(
                    title=f"{ticker} – Omsättning & Vinst (senaste 10 åren)",
                    barmode='group',
                    plot_bgcolor='#0e1117',
                    paper_bgcolor='#0e1117',
                    font_color='white',
                    yaxis_title="Miljarder",
                    hovermode='x unified'
                )
                st.plotly_chart(fig1, use_container_width=True)

        with col2:
            if div_annual is not None:
                div_annual_sorted = div_annual.sort_index()
                years_div = div_annual_sorted.index.year[-10:] if len(div_annual_sorted) >= 10 else div_annual_sorted.index.year
                div_vals = div_annual_sorted.values[-10:] if len(div_annual_sorted) >= 10 else div_annual_sorted.values
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(
                    x=years_div,
                    y=div_vals,
                    marker_color='mediumslateblue',
                    hoverinfo='y',
                    hovertemplate='Utdelning: %{y:.2f}<br>År: %{x}<extra></extra>',
                    name="Utdelning"
                ))
                fig2.update_layout(
                    title=f"{ticker} – Utdelningar per år",
                    plot_bgcolor='#0e1117',
                    paper_bgcolor='#0e1117',
                    font_color='white',
                    yaxis_title="Per aktie",
                    hovermode='x unified'
                )
                st.plotly_chart(fig2, use_container_width=True)

        with col3:
            if gross_profit is not None and operating_income is not None and revenue is not None:
                gross_margin = (gross_profit / revenue * 100).sort_index()
                operating_margin = (operating_income / revenue * 100).sort_index()
                # Use only last 10 years if possible
                if len(gross_margin) >= 10:
                    years_marg = gross_margin.index.year[-10:]
                    gross_vals = gross_margin.values[-10:]
                else:
                    years_marg = gross_margin.index.year
                    gross_vals = gross_margin.values
                if len(operating_margin) >= 10:
                    operating_vals = operating_margin.values[-10:]
                else:
                    operating_vals = operating_margin.values
                fig3 = go.Figure()
                fig3.add_trace(go.Scatter(
                    x=years_marg, y=gross_vals, mode='lines+markers',
                    name="Bruttomarginal", line=dict(color="skyblue"),
                    hovertemplate='Bruttomarginal: %{y:.2f}%<br>År: %{x}<extra></extra>'
                ))
                fig3.add_trace(go.Scatter(
                    x=years_marg, y=operating_vals, mode='lines+markers',
                    name="Rörelsemarginal", line=dict(color="orange"),
                    hovertemplate='Rörelsemarginal: %{y:.2f}%<br>År: %{x}<extra></extra>'
                ))
                fig3.update_layout(
                    title="Marginaler (%)",
                    plot_bgcolor='#0e1117',
                    paper_bgcolor='#0e1117',
                    font_color='white',
                    yaxis_title="%",
                    hovermode='x unified'
                )
                st.plotly_chart(fig3, use_container_width=True)

        # --- Kassaflödesanalys ---
        st.markdown("### 💰 Kassaflödesanalys")

        cashflow = stock.cashflow.T
        cashflow.index = pd.to_datetime(cashflow.index)

        if not cashflow.empty:
            operating_cf = cashflow["Total Cash From Operating Activities"] if "Total Cash From Operating Activities" in cashflow.columns else None
            investing_cf = cashflow["Total Cashflows From Investing Activities"] if "Total Cashflows From Investing Activities" in cashflow.columns else None
            capex = cashflow["Capital Expenditures"] if "Capital Expenditures" in cashflow.columns else None

            if operating_cf is not None and capex is not None:
                free_cf = operating_cf + capex  # capex är negativt

                # Justera till 10 senaste år
                operating_cf = operating_cf.sort_index()
                investing_cf = investing_cf.sort_index()
                free_cf = free_cf.sort_index()

                years_cf = operating_cf.index.year[-10:] if len(operating_cf) >= 10 else operating_cf.index.year
                op_vals = (operating_cf / 1e9).values[-10:] if len(operating_cf) >= 10 else (operating_cf / 1e9).values
                invest_vals = (investing_cf / 1e9).values[-10:] if len(investing_cf) >= 10 else (investing_cf / 1e9).values
                free_vals = (free_cf / 1e9).values[-10:] if len(free_cf) >= 10 else (free_cf / 1e9).values

                fig_cf = go.Figure()
                fig_cf.add_trace(go.Bar(
                    x=years_cf,
                    y=op_vals,
                    name="Operativt kassaflöde",
                    marker_color="lightgreen",
                    hovertemplate="Operativt: %{y:.2f} Mdr<br>År: %{x}<extra></extra>"
                ))
                fig_cf.add_trace(go.Bar(
                    x=years_cf,
                    y=invest_vals,
                    name="Investeringskassaflöde",
                    marker_color="tomato",
                    hovertemplate="Investering: %{y:.2f} Mdr<br>År: %{x}<extra></extra>"
                ))
                fig_cf.add_trace(go.Scatter(
                    x=years_cf,
                    y=free_vals,
                    mode="lines+markers",
                    name="Fritt kassaflöde",
                    line=dict(color="gold"),
                    hovertemplate="Fritt: %{y:.2f} Mdr<br>År: %{x}<extra></extra>"
                ))
                fig_cf.update_layout(
                    title="Kassaflöden (Miljarder)",
                    barmode="group",
                    plot_bgcolor="#0e1117",
                    paper_bgcolor="#0e1117",
                    font_color="white",
                    yaxis_title="Mdr",
                    hovermode="x unified"
                )
                st.plotly_chart(fig_cf, use_container_width=True)

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
    ticker_a = ticker.replace("-B", "-A")
    ticker_b = ticker
    stock_a = yf.Ticker(ticker_a)
    stock_b = yf.Ticker(ticker_b)

    shares_a = stock_a.info.get("sharesOutstanding", 0)
    shares_b = stock_b.info.get("sharesOutstanding", 0)

    # Om båda är 0 (fel i API), fallback till original
    if shares_a == 0 and shares_b == 0:
        shares_outstanding = info.get("sharesOutstanding", 1e9) / 1e6
    else:
        shares_outstanding = (shares_a + shares_b) / 1e6  # i miljoner


    # --- VÄRDERINGSKALKYLATOR ---

    def intrinsic_value(growth, margin, pe, years, required_return):
        # Steg 1: Prognostisera framtida omsättning
        future_sales = convert(sales, from_currency=currency, to_currency="USD") * ((1 + growth / 100) ** years)
        future_earnings = future_sales * (margin / 100)

        # Steg 2: Terminalvärde = framtida vinst * multipel
        terminal_value = future_earnings * pe

        # Steg 3: Diskontera terminalvärdet till idag
        discount_factor = (1 + required_return / 100) ** years
        discounted_terminal_value = terminal_value / discount_factor

        # Steg 4: Värde per aktie
        per_share_value = discounted_terminal_value / shares_outstanding

        # DEBUG OUTPUT
        return per_share_value

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
