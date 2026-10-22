import streamlit as st
import requests
import psycopg2
import pandas as pd
API_URL = "http://127.0.0.1:8000"
# ============================================================
# LoanGuard — Intelligent Loan Default Risk Assessment
# Frontend only: Streamlit UI + existing FastAPI /predict API
# ============================================================
st.set_page_config(
    page_title="LoanGuard | Risk Assessment",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)
# ============================================================
# Global Styling
# ============================================================
st.markdown(
    """
    <style>
    /* ---------- App background ---------- */
    .stApp {
        background: #f4f7fb;
    }
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }
    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background: #0f172a;
        border-right: 1px solid #1e293b;
    }
    [data-testid="stSidebar"] * {
        color: #e5e7eb;
    }
    .brand {
        padding: 10px 4px 22px 4px;
        border-bottom: 1px solid #243047;
        margin-bottom: 22px;
    }
    .brand-title {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #ffffff;
    }
    .brand-subtitle {
        font-size: 13px;
        color: #94a3b8;
        margin-top: 4px;
    }

    .side-section {
        color: #64748b;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin: 22px 0 9px;
    }

    .system-card {
        background: #172033;
        border: 1px solid #26334a;
        border-radius: 12px;
        padding: 14px;
        margin-top: 8px;
    }

    .system-row {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        padding: 5px 0;
        font-size: 12px;
    }

    .system-label {
        color: #94a3b8;
    }

    .system-value {
        color: #e2e8f0;
        font-weight: 600;
        text-align: right;
    }

    /* ---------- Typography ---------- */
    .page-title {
        font-size: 38px;
        font-weight: 800;
        color: #111827;
        letter-spacing: -1.2px;
        margin-bottom: 2px;
    }

    .page-subtitle {
        color: #64748b;
        font-size: 16px;
        margin-bottom: 22px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 750;
        color: #111827;
        margin: 4px 0 3px;
    }

    .section-subtitle {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 16px;
    }

    /* ---------- Cards ---------- */
    .status-card,
    .metric-card,
    .info-card,
    .result-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04);
    }

    .status-card {
        min-height: 82px;
    }

    .status-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #22c55e;
        margin-right: 8px;
        box-shadow: 0 0 0 4px rgba(34,197,94,0.12);
    }

    .status-title {
        color: #334155;
        font-size: 15px;
        font-weight: 700;
    }

    .status-subtitle {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 7px;
    }

    .metric-label {
        color: #64748b;
        font-size: 13px;
        font-weight: 600;
    }

    .metric-value {
        color: #111827;
        font-size: 27px;
        font-weight: 800;
        margin-top: 7px;
    }

    .metric-helper {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 4px;
    }

    .form-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 22px 24px 12px;
        margin-bottom: 18px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.035);
    }

    .form-card-title {
        color: #172033;
        font-size: 18px;
        font-weight: 750;
        margin-bottom: 3px;
    }

    .form-card-subtitle {
        color: #94a3b8;
        font-size: 12px;
        margin-bottom: 13px;
    }

    /* ---------- Streamlit widgets ---------- */
    div[data-testid="stNumberInput"] label,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stSlider"] label {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }

    div[data-testid="stButton"] > button {
        border-radius: 12px;
        border: 0;
        min-height: 52px;
        font-size: 16px;
        font-weight: 750;
        background: #172554;
        color: white;
        box-shadow: 0 5px 14px rgba(23,37,84,0.18);
        transition: all 0.15s ease;
    }

    div[data-testid="stButton"] > button:hover {
        background: #1e3a8a;
        border: 0;
        color: white;
    }

    /* ---------- Risk result ---------- */
    .risk-banner {
        border-radius: 14px;
        padding: 16px 20px;
        font-size: 16px;
        font-weight: 750;
        margin: 10px 0 18px;
    }

    .risk-high {
        background: #fff1f2;
        border: 1px solid #fecdd3;
        color: #be123c;
    }

    .risk-medium {
        background: #fffbeb;
        border: 1px solid #fde68a;
        color: #b45309;
    }

    .risk-low {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        color: #15803d;
    }

    .disclaimer {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 14px;
        padding: 15px 18px;
        color: #1d4ed8;
        font-size: 13px;
        line-height: 1.55;
    }

    .placeholder-card {
        background: #ffffff;
        border: 1px dashed #cbd5e1;
        border-radius: 16px;
        padding: 28px;
        text-align: center;
        color: #64748b;
    }

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        padding: 24px 0 4px;
    }

    /* Hide Streamlit menu/footer chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Helper Functions
# ============================================================

def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div class="brand">
                <div class="brand-title">🏦 LoanGuard</div>
                <div class="brand-subtitle">Intelligent Loan Risk Platform</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="side-section">Navigation</div>', unsafe_allow_html=True)

        page = st.radio(
            "Navigation",
            [
                "📊 Dashboard",
                "🏠 Risk Assessment",
                "📈 Financial Analysis",
                "🧠 Model Explainability",
                "📋 Application History",
            ],
            label_visibility="collapsed",
        )

        st.markdown('<div class="side-section">ML System</div>', unsafe_allow_html=True)

        st.markdown(
            """
            <div class="system-card">
                <div class="system-row">
                    <span class="system-label">Algorithm</span>
                    <span class="system-value">XGBoost</span>
                </div>
                <div class="system-row">
                    <span class="system-label">Task</span>
                    <span class="system-value">Binary Classification</span>
                </div>
                <div class="system-row">
                    <span class="system-label">Output</span>
                    <span class="system-value">Default Probability</span>
                </div>
                <div class="system-row">
                    <span class="system-label">Backend</span>
                    <span class="system-value">FastAPI</span>
                </div>
                <div class="system-row">
                    <span class="system-label">Frontend</span>
                    <span class="system-value">Streamlit</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="margin-top:24px;color:#64748b;font-size:11px;line-height:1.5;">
            Educational ML risk assessment platform.<br>
            Not a substitute for a real lending decision.
            </div>
            """,
            unsafe_allow_html=True,
        )

    return page


def render_header():
    st.markdown(
        '<div class="page-title">LoanGuard</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Intelligent Loan Default Risk Assessment</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3)

    status = [
        ("Model Ready", "XGBoost model loaded"),
        ("XGBoost Engine", "Binary classification"),
        ("API Service", "FastAPI prediction endpoint"),
    ]

    for col, (title, subtitle) in zip(cols, status):
        with col:
            st.markdown(
                f"""
                <div class="status-card">
                    <div>
                        <span class="status-dot"></span>
                        <span class="status-title">{title}</span>
                    </div>
                    <div class="status-subtitle">{subtitle}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")


def form_card_title(icon, title, subtitle):
    st.markdown(
        f"""
        <div class="form-card-title">{icon} {title}</div>
        <div class="form-card-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def render_applicant_form():
    st.markdown(
        '<div class="section-title">👤 Applicant Information</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">Provide applicant information to generate a preliminary ML-based risk assessment.</div>',
        unsafe_allow_html=True,
    )

    # ---------- Personal profile ----------
    with st.container():
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        form_card_title(
            "👤",
            "Personal Profile",
            "Basic household and demographic information",
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            age = st.number_input(
                "Age (years)",
                min_value=18,
                max_value=80,
                value=30,
                step=1,
            )

        with c2:
            children = st.number_input(
                "Number of Children",
                min_value=0,
                max_value=20,
                value=0,
                step=1,
            )

        with c3:
            family_members = st.number_input(
                "Family Members",
                min_value=1,
                max_value=20,
                value=2,
                step=1,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Financial profile ----------
    with st.container():
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        form_card_title(
            "💰",
            "Financial Profile",
            "Income, requested credit and repayment burden",
        )

        c1, c2 = st.columns(2)

        with c1:
            income = st.number_input(
                "Annual Income (₹)",
                min_value=0.0,
                value=180000.0,
                step=10000.0,
            )

            credit_amount = st.number_input(
                "Requested Credit Amount (₹)",
                min_value=0.0,
                value=500000.0,
                step=10000.0,
            )

        with c2:
            annuity = st.number_input(
                "Loan Annuity (₹)",
                min_value=0.0,
                value=25000.0,
                step=1000.0,
            )

            goods_price = st.number_input(
                "Goods Price (₹)",
                min_value=0.0,
                value=450000.0,
                step=10000.0,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Employment profile ----------
    with st.container():
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        form_card_title(
            "💼",
            "Employment Profile",
            "Income source, employment duration and occupation",
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            income_type = st.selectbox(
                "Income Type",
                [
                    "Working",
                    "Commercial associate",
                    "Pensioner",
                    "State servant",
                    "Student",
                    "Businessman",
                    "Maternity leave",
                    "Unemployed",
                ],
            )

        with c2:
            employment_years = st.number_input(
                "Employment Duration (years)",
                min_value=0.0,
                max_value=50.0,
                value=5.0,
                step=0.5,
            )

        with c3:
            occupation = st.selectbox(
                "Occupation",
                [
                    "Laborers",
                    "Sales staff",
                    "Core staff",
                    "Managers",
                    "Drivers",
                    "High skill tech staff",
                    "Medicine staff",
                    "Accountants",
                    "Security staff",
                    "Cooking staff",
                    "Private service staff",
                    "Cleaning staff",
                    "Low-skill Laborers",
                    "Secretaries",
                    "Waiters/barmen staff",
                    "Realty agents",
                    "HR staff",
                    "IT staff",
                ],
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Assets & housing ----------
    with st.container():
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        form_card_title(
            "🏠",
            "Assets & Housing",
            "Ownership and residential information",
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            housing_type = st.selectbox(
                "Housing Type",
                [
                    "House / apartment",
                    "With parents",
                    "Municipal apartment",
                    "Rented apartment",
                    "Office apartment",
                    "Co-op apartment",
                ],
            )

        with c2:
            owns_car = st.selectbox(
                "Owns Car",
                ["No", "Yes"],
            )

        with c3:
            owns_property = st.selectbox(
                "Owns Property",
                ["Yes", "No"],
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Credit profile ----------
    with st.container():
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        form_card_title(
            "📊",
            "Credit Profile",
            "External credit indicators and regional risk information",
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            ext_source_2 = st.slider(
                "External Credit Score 2",
                min_value=0.0,
                max_value=1.0,
                value=0.50,
                step=0.01,
            )

        with c2:
            ext_source_3 = st.slider(
                "External Credit Score 3",
                min_value=0.0,
                max_value=1.0,
                value=0.50,
                step=0.01,
            )

        with c3:
            region_rating = st.selectbox(
                "Region Rating",
                [1, 2, 3],
                index=1,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    return {
        "age": age,
        "children": children,
        "family_members": family_members,
        "income": income,
        "credit_amount": credit_amount,
        "annuity": annuity,
        "goods_price": goods_price,
        "income_type": income_type,
        "employment_years": employment_years,
        "occupation": occupation,
        "housing_type": housing_type,
        "owns_car": owns_car,
        "owns_property": owns_property,
        "ext_source_2": ext_source_2,
        "ext_source_3": ext_source_3,
        "region_rating": region_rating,
    }


def render_financial_metrics(data):
    income = data["income"]
    credit = data["credit_amount"]
    annuity = data["annuity"]
    family = data["family_members"]

    credit_income = credit / income if income > 0 else 0
    annuity_income = annuity / income if income > 0 else 0

    st.markdown(
        '<div class="section-title">📐 Live Financial Metrics</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle">Key financial ratios update automatically as applicant information changes.</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3)

    metrics = [
        (
            "Credit / Income",
            f"{credit_income:.2f}×",
            "Requested credit relative to annual income",
        ),
        (
            "Annuity / Income",
            f"{annuity_income:.2%}",
            "Annualized repayment burden",
        ),
        (
            "Household Dependents",
            str(max(0, family - 1)),
            "Family members excluding primary applicant",
        ),
    ]

    for col, (label, value, helper) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-helper">{helper}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    return credit_income, annuity_income


def build_api_payload(data):
    """
    Map the friendly Streamlit fields to the existing Home Credit
    feature names expected by the FastAPI prediction endpoint.

    The existing API remains unchanged.
    """
    return {
        "AMT_INCOME_TOTAL": data["income"],
        "AMT_CREDIT": data["credit_amount"],
        "AMT_ANNUITY": data["annuity"],
        "CNT_CHILDREN": data["children"],
        "CNT_FAM_MEMBERS": data["family_members"],
        "AMT_GOODS_PRICE": data["goods_price"],
        "DAYS_BIRTH": -int(data["age"] * 365),
        "DAYS_EMPLOYED": -int(data["employment_years"] * 365),
        "NAME_INCOME_TYPE": data["income_type"],
        "OCCUPATION_TYPE": data["occupation"],
        "NAME_HOUSING_TYPE": data["housing_type"],
        "FLAG_OWN_CAR": "Y" if data["owns_car"] == "Yes" else "N",
        "FLAG_OWN_REALTY": "Y" if data["owns_property"] == "Yes" else "N",
        "EXT_SOURCE_2": data["ext_source_2"],
        "EXT_SOURCE_3": data["ext_source_3"],
        "REGION_RATING_CLIENT": data["region_rating"],
    }


def render_prediction_result(result, data):
    probability = float(result["default_probability"])
    prediction = int(result["default_prediction"])
    risk_level = result["risk_level"]

    st.markdown('<div class="section-title">🎯 Risk Assessment Result</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Model-generated estimate from the existing XGBoost prediction service.</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3)

    with cols[0]:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="metric-label">Default Probability</div>
                <div class="metric-value">{probability:.2%}</div>
                <div class="metric-helper">Estimated repayment difficulty</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with cols[1]:
        prediction_text = "Default Risk" if prediction == 1 else "No Default Risk"
        st.markdown(
            f"""
            <div class="result-card">
                <div class="metric-label">Prediction</div>
                <div class="metric-value" style="font-size:24px;">{prediction_text}</div>
                <div class="metric-helper">Binary model output</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with cols[2]:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="metric-label">Risk Level</div>
                <div class="metric-value" style="font-size:24px;">{risk_level}</div>
                <div class="metric-helper">Based on current API thresholding</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    st.progress(max(0.0, min(1.0, probability)))
    st.caption(f"Estimated probability of repayment difficulty: {probability:.2%}")

    if risk_level == "High Risk":
        st.markdown(
            '<div class="risk-banner risk-high">🔴 HIGH RISK — Additional assessment is recommended.</div>',
            unsafe_allow_html=True,
        )
    elif risk_level == "Medium Risk":
        st.markdown(
            '<div class="risk-banner risk-medium">🟠 MEDIUM RISK — Further applicant assessment is recommended.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="risk-banner risk-low">🟢 LOW RISK — The model estimates a relatively lower probability of repayment difficulty.</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">📋 Application Summary</div>', unsafe_allow_html=True)
    st.write("")

    summary = [
        ("Annual Income", f"₹{data['income']:,.0f}"),
        ("Credit Amount", f"₹{data['credit_amount']:,.0f}"),
        ("Loan Annuity", f"₹{data['annuity']:,.0f}"),
        ("Children", str(data["children"])),
    ]

    cols = st.columns(4)

    for col, (label, value) in zip(cols, summary):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value" style="font-size:22px;">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    st.markdown(
        """
        <div class="disclaimer">
        <strong>ⓘ Important:</strong> This is a preliminary machine-learning
        assessment for educational and demonstration purposes. A lending
        decision should not be based solely on this prediction.
        </div>
        """,
        unsafe_allow_html=True,
    )


def call_prediction_api(data):
    payload = build_api_payload(data)

    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=payload,
            timeout=30,
        )

        if response.status_code == 200:
            return response.json(), None

        return None, f"API returned HTTP {response.status_code}: {response.text}"

    except requests.exceptions.ConnectionError:
        return None, "Could not connect to FastAPI. Make sure the API is running on port 8000."

    except requests.exceptions.Timeout:
        return None, "The API request timed out. Please try again."

    except requests.exceptions.RequestException as exc:
        return None, f"Request error: {exc}"


def render_dashboard():
    st.markdown('<div class="section-title">📊 Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">LoanGuard overview and ML system status.</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    dashboard_items = [
        ("🤖", "Prediction Engine", "XGBoost", "Active"),
        ("⚡", "API Layer", "FastAPI", "Ready"),
        ("🖥️", "User Interface", "Streamlit", "Active"),
    ]

    for col, (icon, label, value, status) in zip(
        [c1, c2, c3], dashboard_items
    ):
        with col:
            st.markdown(
                f"""
                <div class="info-card">
                    <div style="font-size:28px;">{icon}</div>
                    <div style="font-size:13px;color:#64748b;margin-top:10px;">{label}</div>
                    <div style="font-size:23px;font-weight:800;color:#111827;margin-top:4px;">{value}</div>
                    <div style="font-size:12px;color:#16a34a;margin-top:7px;">● {status}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    st.markdown(
        """
        <div class="info-card">
            <div class="section-title">About LoanGuard</div>
            <p style="color:#64748b;line-height:1.7;">
            LoanGuard is an ML-powered educational risk assessment platform.
            It uses a trained XGBoost classifier to estimate the probability
            of repayment difficulty and presents the result through a
            FastAPI-backed Streamlit interface.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_financial_analysis(data=None):
    st.markdown('<div class="section-title">📈 Financial Analysis</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Financial indicators calculated from the current application.</div>',
        unsafe_allow_html=True,
    )

    if data is None:
        st.markdown(
            """
            <div class="placeholder-card">
                <div style="font-size:32px;">📊</div>
                <h3 style="color:#334155;">No application loaded</h3>
                <p>Complete a risk assessment to populate the financial analysis.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    income = data["income"]
    credit = data["credit_amount"]
    annuity = data["annuity"]

    c1, c2, c3, c4 = st.columns(4)

    values = [
        ("Annual Income", f"₹{income:,.0f}"),
        ("Loan Amount", f"₹{credit:,.0f}"),
        ("Credit / Income", f"{credit/income:.2f}×" if income else "N/A"),
        ("Annuity / Income", f"{annuity/income:.2%}" if income else "N/A"),
    ]

    for col, (label, value) in zip([c1, c2, c3, c4], values):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value" style="font-size:21px;">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    st.markdown(
        """
        <div class="placeholder-card">
            <div style="font-size:30px;">📉</div>
            <h3 style="color:#334155;">Analytics layer ready</h3>
            <p>
            This section is structured for future financial charts and
            PostgreSQL-backed application analytics.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_explainability():
    st.markdown('<div class="section-title">🧠 Model Explainability</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Understand which features can influence the model prediction.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="placeholder-card">
            <div style="font-size:38px;">🧠</div>
            <h3 style="color:#334155;">SHAP Explainability</h3>
            <p>
            SHAP analysis has already been completed as part of the ML workflow.
            This Streamlit section is reserved for integrating the generated
            feature-importance and individual explanation visualizations.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_db_connection():
    """Connect Streamlit to PostgreSQL."""
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="loan_default_db",
        user="loan_user",
        password="loan_password"
    )


def render_history():
    """Display real loan application history from PostgreSQL."""

    st.markdown(
        """
        <div class="section-title">
            Application History
        </div>
        <div class="section-subtitle">
            Previously assessed loan applications and their risk predictions
        </div>
        """,
        unsafe_allow_html=True
    )

    # Refresh button
    if st.button("🔄 Refresh History"):
        st.rerun()

    connection = None

    try:
        connection = get_db_connection()

        query = """
            SELECT
                id,
                application_timestamp,
                annual_income,
                requested_credit,
                default_prediction,
                default_probability,
                risk_level
            FROM applications
            ORDER BY id DESC
        """

        history_df = pd.read_sql_query(
            query,
            connection
        )

        # No records
        if history_df.empty:
            st.info(
                "No loan applications have been assessed yet."
            )
            return

        # ---------------------------------
        # Filters
        # ---------------------------------

        st.markdown("### Filters")

        col1, col2 = st.columns(2)

        with col1:

            risk_options = [
                "All",
                "High Risk",
                "Medium Risk",
                "Low Risk"
            ]

            selected_risk = st.selectbox(
                "Risk Level",
                risk_options
            )

        with col2:

            prediction_options = [
                "All",
                0,
                1
            ]

            selected_prediction = st.selectbox(
                "Prediction",
                prediction_options
            )

        # Apply risk filter
        filtered_df = history_df.copy()

        if selected_risk != "All":

            filtered_df = filtered_df[
                filtered_df["risk_level"] == selected_risk
            ]

        # Apply prediction filter
        if selected_prediction != "All":

            filtered_df = filtered_df[
                filtered_df["default_prediction"]
                == selected_prediction
            ]

        # ---------------------------------
        # Format columns
        # ---------------------------------

        display_df = filtered_df.copy()

        display_df["application_timestamp"] = pd.to_datetime(
            display_df["application_timestamp"]
        ).dt.strftime(
            "%d %b %Y, %I:%M %p"
        )

        display_df["annual_income"] = (
            display_df["annual_income"]
            .apply(lambda x: f"₹{x:,.0f}" if pd.notna(x) else "—")
        )

        display_df["requested_credit"] = (
            display_df["requested_credit"]
            .apply(lambda x: f"₹{x:,.0f}" if pd.notna(x) else "—")
        )

        display_df["default_probability"] = (
            display_df["default_probability"]
            .apply(lambda x: f"{x:.1%}" if pd.notna(x) else "—")
        )

        display_df["default_prediction"] = (
            display_df["default_prediction"]
            .map({
                0: "No Default",
                1: "Default Risk"
            })
        )

        display_df = display_df.rename(
            columns={
                "id": "Application ID",
                "application_timestamp": "Date / Time",
                "annual_income": "Income",
                "requested_credit": "Credit Amount",
                "default_prediction": "Prediction",
                "default_probability": "Default Probability",
                "risk_level": "Risk Level"
            }
        )

        # ---------------------------------
        # Display
        # ---------------------------------

        st.dataframe(
            display_df[
                [
                    "Application ID",
                    "Date / Time",
                    "Income",
                    "Credit Amount",
                    "Default Probability",
                    "Prediction",
                    "Risk Level"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        # ---------------------------------
        # Summary metrics
        # ---------------------------------

        st.markdown("### History Summary")

        metric1, metric2, metric3, metric4 = st.columns(4)

        with metric1:
            st.metric(
                "Total Applications",
                len(filtered_df)
            )

        with metric2:
            high_risk_count = (
                filtered_df["risk_level"]
                .eq("High Risk")
                .sum()
            )

            st.metric(
                "High Risk",
                int(high_risk_count)
            )

        with metric3:
            default_count = (
                filtered_df["default_prediction"]
                .eq(1)
                .sum()
            )

            st.metric(
                "Default Predictions",
                int(default_count)
            )

        with metric4:
            if len(filtered_df) > 0:

                avg_probability = (
                    filtered_df["default_probability"]
                    .mean()
                )

                st.metric(
                    "Avg. Default Probability",
                    f"{avg_probability:.1%}"
                )

    except Exception as error:

        st.error(
            f"Unable to load application history: {error}"
        )

    finally:

        if connection:
            connection.close()

# ============================================================
# Application
# ============================================================

page = render_sidebar()

# Keep latest applicant data/results across Streamlit reruns.
if "applicant_data" not in st.session_state:
    st.session_state.applicant_data = None

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None


if page == "📊 Dashboard":
    render_header()
    render_dashboard()

elif page == "🏠 Risk Assessment":
    render_header()

    data = render_applicant_form()
    render_financial_metrics(data)

    st.write("")

    if st.button("🔍  Assess Loan Risk", use_container_width=True):
        with st.spinner("Analyzing applicant with the XGBoost model..."):
            result, error = call_prediction_api(data)

        if error:
            st.error(error)
        else:
            st.success("Risk assessment completed successfully.")
            st.session_state.applicant_data = data
            st.session_state.prediction_result = result

    if st.session_state.prediction_result is not None:
        st.write("")
        render_prediction_result(
            st.session_state.prediction_result,
            st.session_state.applicant_data,
        )

elif page == "📈 Financial Analysis":
    render_header()
    render_financial_analysis(st.session_state.applicant_data)

elif page == "🧠 Model Explainability":
    render_header()
    render_explainability()

elif page == "📋 Application History":
    render_header()
    render_history()


# ============================================================
# Footer
# ============================================================

st.markdown(
    """
    <div class="footer">
        LoanGuard • XGBoost + FastAPI + Streamlit<br>
        ML-powered Loan Default Risk Assessment • Educational Demonstration
    </div>
    """,
    unsafe_allow_html=True,
)
