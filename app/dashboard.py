

# import streamlit as st
# import requests

# st.set_page_config(
#     page_title="Credit Risk PD",
#     page_icon="💳",
#     layout="centered"
# )

# st.title("💳 Credit Risk PD Scorecard")
# st.write("Probability of Default Prediction")

# st.subheader("Applicant Information")

# credit_history = st.number_input(
#     "Credit History (Years)",
#     min_value=0.0,
#     value=15.0
# )

# utilization = st.number_input(
#     "Credit Utilization",
#     min_value=0.0,
#     max_value=1.0,
#     value=0.15
# )

# dti = st.number_input(
#     "Debt-to-Income Ratio",
#     min_value=0.0,
#     max_value=1.0,
#     value=0.20
# )

# employment = st.number_input(
#     "Employment Length (Years)",
#     min_value=0.0,
#     value=10.0
# )

# income = st.number_input(
#     "Monthly Income",
#     min_value=0.0,
#     value=100000.0
# )

# delinq_30 = st.number_input(
#     "30-Day Delinquencies",
#     min_value=0,
#     value=0
# )

# delinq_60 = st.number_input(
#     "60-Day Delinquencies",
#     min_value=0,
#     value=0
# )

# delinq_90 = st.number_input(
#     "90-Day Delinquencies",
#     min_value=0,
#     value=0
# )


# if st.button("Predict Credit Risk"):

#     data = {
#         "Credit_History_Years": credit_history,
#         "Credit_Utilization": utilization,
#         "Debt_to_Income": dti,
#         "Employment_Length_Years": employment,
#         "Monthly_Income": income,
#         "Number_of_Delinquencies_30": delinq_30,
#         "Number_of_Delinquencies_60": delinq_60,
#         "Number_of_Delinquencies_90": delinq_90
#     }

#     try:

#         response = requests.post(
#             "http://127.0.0.1:8000/predict",
#             json=data
#         )

#         response.raise_for_status()

#         result = response.json()

#         st.subheader("Prediction Result")

#         st.metric(
#             "Probability of Default",
#             f"{result['PD'] * 100:.2f}%"
#         )

#         st.metric(
#             "Credit Score",
#             result["Score"]
#         )

#         st.metric(
#             "Risk Band",
#             result["Risk_Band"]
#         )

#     except requests.exceptions.RequestException as e:

#         st.error(
#             "Unable to connect to the Credit Risk API. "
#             "Make sure FastAPI is running."
#         )

#         st.error(str(e))


import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="DV | Credit Risk PD Scorecard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* =========================
       MAIN BACKGROUND
       ========================= */

    .stApp {
        background: #071c20;
        color: #f5f7f8;
    }

    [data-testid="stSidebar"] {
        background: #06171a;
        border-right: 1px solid #17383d;
    }

    [data-testid="stSidebar"] * {
        color: #dcebed;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1600px;
    }


    /* =========================
       DV LOGO
       ========================= */

    .dv-logo {
        font-size: 42px;
        font-weight: 900;
        letter-spacing: 3px;
        color: #ffffff;
        margin-bottom: 0px;
    }

    .dv-subtitle {
        color: #58d6ca;
        font-size: 13px;
        letter-spacing: 2px;
        font-weight: 700;
    }


    /* =========================
       HEADER
       ========================= */

    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: white;
        margin-bottom: 3px;
    }

    .main-subtitle {
        color: #91aeb2;
        font-size: 15px;
        margin-bottom: 25px;
    }


    /* =========================
       CARDS
       ========================= */

    .card {
        background: linear-gradient(
            145deg,
            #102d32,
            #0b2428
        );

        border: 1px solid #1b4247;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 18px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    }

    .card-title {
        font-size: 15px;
        font-weight: 700;
        color: #8faeb2;
        margin-bottom: 8px;
    }

    .card-value {
        font-size: 30px;
        font-weight: 800;
        color: white;
    }

    .card-small {
        color: #6e9297;
        font-size: 12px;
        margin-top: 5px;
    }


    /* =========================
       KPI CARDS
       ========================= */

    .kpi {
        background: linear-gradient(
            135deg,
            #12383d,
            #0b2529
        );

        border: 1px solid #1c4c52;
        border-radius: 16px;
        padding: 20px;
        height: 125px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.20);
    }

    .kpi-label {
        color: #8baeb2;
        font-size: 13px;
        font-weight: 600;
    }

    .kpi-value {
        color: white;
        font-size: 28px;
        font-weight: 800;
        margin-top: 8px;
    }


    /* =========================
       RESULT CARDS
       ========================= */

    .result-card {
        background: linear-gradient(
            135deg,
            #123d40,
            #0b292d
        );

        border: 1px solid #286268;
        border-radius: 18px;
        padding: 24px;
        text-align: center;
        min-height: 145px;
    }

    .result-label {
        color: #91b3b6;
        font-size: 13px;
        font-weight: 600;
    }

    .result-value {
        font-size: 34px;
        font-weight: 900;
        color: white;
        margin-top: 12px;
    }


    /* =========================
       SECTION HEADERS
       ========================= */

    .section-title {
        font-size: 21px;
        font-weight: 800;
        color: white;
        margin-top: 15px;
        margin-bottom: 15px;
    }


    /* =========================
       RISK BADGES
       ========================= */

    .risk-low {
        display: inline-block;
        background: #123d32;
        color: #55e6b0;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 800;
    }

    .risk-medium {
        display: inline-block;
        background: #453817;
        color: #f3d36b;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 800;
    }

    .risk-high {
        display: inline-block;
        background: #472b1f;
        color: #ff9b68;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 800;
    }

    .risk-very-high {
        display: inline-block;
        background: #461d27;
        color: #ff7185;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 800;
    }


    /* =========================
       BUTTON
       ========================= */

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 48px;
        border: none;

        background: linear-gradient(
            90deg,
            #28b8aa,
            #54dfcf
        );

        color: #062023;
        font-size: 15px;
        font-weight: 900;

        transition: 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(50,210,195,0.25);
    }


    /* =========================
       INPUTS
       ========================= */

    div[data-baseweb="input"] {
        background: #0c2529;
        border-radius: 10px;
    }

    div[data-baseweb="input"] input {
        color: white;
    }


    /* =========================
       TABS
       ========================= */

    button[data-baseweb="tab"] {
        color: #8eabad;
        font-weight: 700;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #54dfcf;
    }


    /* =========================
       EXPANDERS
       ========================= */

    .streamlit-expanderHeader {
        background: #0d292e;
        border-radius: 12px;
        color: white;
        font-weight: 700;
    }


    /* =========================
       SIDEBAR NAV
       ========================= */

    .side-nav {
        padding: 12px;
        margin: 5px 0;
        border-radius: 10px;
        color: #8faeb2;
        font-weight: 600;
    }

    .side-nav:hover {
        background: #123439;
        color: #54dfcf;
    }


    /* =========================
       FOOTER
       ========================= */

    .footer {
        text-align: center;
        color: #58777b;
        padding: 30px;
        font-size: 12px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "applicant_data" not in st.session_state:
    st.session_state.applicant_data = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="dv-logo">DV</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dv-subtitle">ZEN SCORE</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        '<div class="side-nav">📊 Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="side-nav">👤 Applicant Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="side-nav">📄 Credit Report</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="side-nav">📈 Risk Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="side-nav">🎯 Action Plan</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="side-nav">⚙️ Settings</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.caption("Credit Risk Analytics")
    st.caption("PD Scorecard v1.0")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">Credit Risk PD Scorecard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'Probability of Default Prediction & Risk Analysis'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# KPI CARDS
# ============================================================

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown("""
    <div class="kpi">
        <div class="kpi-label">MODEL</div>
        <div class="kpi-value">PD Scorecard</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown("""
    <div class="kpi">
        <div class="kpi-label">PREDICTION TYPE</div>
        <div class="kpi-value">Probability</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown("""
    <div class="kpi">
        <div class="kpi-label">SCORECARD</div>
        <div class="kpi-value">WOE + Score</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    current_pd = st.session_state.prediction["PD"] * 100 \
        if st.session_state.prediction else 0

    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-label">CURRENT PD</div>
        <div class="kpi-value">{current_pd:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👤 Applicant",
    "🎯 Results",
    "📊 Risk Analysis",
    "🔎 Feature Impact",
    "📄 Credit Report"
])


# ============================================================
# TAB 1 - APPLICANT
# ============================================================

with tab1:

    st.markdown(
        '<div class="section-title">Applicant Information</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            '<div class="card-title">Credit Profile</div>',
            unsafe_allow_html=True
        )

        credit_history = st.number_input(
            "Credit History (Years)",
            min_value=0.0,
            value=15.0,
            step=0.5
        )

        utilization = st.number_input(
            "Credit Utilization",
            min_value=0.0,
            max_value=1.0,
            value=0.15,
            step=0.01,
            format="%.2f"
        )

        dti = st.number_input(
            "Debt-to-Income Ratio",
            min_value=0.0,
            max_value=1.0,
            value=0.20,
            step=0.01,
            format="%.2f"
        )

        employment = st.number_input(
            "Employment Length (Years)",
            min_value=0.0,
            value=10.0,
            step=0.5
        )

    with col2:

        st.markdown(
            '<div class="card-title">Financial & Delinquency Profile</div>',
            unsafe_allow_html=True
        )

        income = st.number_input(
            "Monthly Income",
            min_value=0.0,
            value=100000.0,
            step=5000.0
        )

        delinq_30 = st.number_input(
            "30-Day Delinquencies",
            min_value=0,
            value=0,
            step=1
        )

        delinq_60 = st.number_input(
            "60-Day Delinquencies",
            min_value=0,
            value=0,
            step=1
        )

        delinq_90 = st.number_input(
            "90-Day Delinquencies",
            min_value=0,
            value=0,
            step=1
        )

    st.markdown("<br>", unsafe_allow_html=True)

    predict_col, space = st.columns([1, 2])

    with predict_col:

        predict_button = st.button(
            "🚀 Predict Credit Risk",
            use_container_width=True
        )

    # ========================================================
    # API CALL
    # ========================================================

    if predict_button:

        data = {
            "Credit_History_Years": credit_history,
            "Credit_Utilization": utilization,
            "Debt_to_Income": dti,
            "Employment_Length_Years": employment,
            "Monthly_Income": income,
            "Number_of_Delinquencies_30": delinq_30,
            "Number_of_Delinquencies_60": delinq_60,
            "Number_of_Delinquencies_90": delinq_90
        }

        try:

            with st.spinner("Running credit risk model..."):

                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    json=data,
                    timeout=30
                )

            response.raise_for_status()

            result = response.json()

            st.session_state.prediction = result
            st.session_state.applicant_data = data

            st.success("Credit risk prediction completed successfully!")

        except requests.exceptions.RequestException as e:

            st.error(
                "Unable to connect to the Credit Risk API."
            )

            st.code(str(e))


# ============================================================
# GET STORED RESULT
# ============================================================

result = st.session_state.prediction
data = st.session_state.applicant_data


# ============================================================
# TAB 2 - RESULTS
# ============================================================

with tab2:

    st.markdown(
        '<div class="section-title">Credit Risk Result</div>',
        unsafe_allow_html=True
    )

    if result is None:

        st.info(
            "Enter applicant information and click "
            "**Predict Credit Risk** to generate the score."
        )

    else:

        pd_value = float(result.get("PD", 0))
        score = result.get("Score", "N/A")
        risk_band = result.get("Risk_Band", "Unknown")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">
                    PROBABILITY OF DEFAULT
                </div>
                <div class="result-value">
                    {pd_value * 100:.2f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c2:

            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">
                    CREDIT SCORE
                </div>
                <div class="result-value">
                    {score}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with c3:

            st.markdown(f"""
            <div class="result-card">
                <div class="result-label">
                    RISK BAND
                </div>
                <div class="result-value">
                    {risk_band}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ====================================================
        # PD DONUT
        # ====================================================

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:

            fig = go.Figure(
                go.Pie(
                    labels=["Default Risk", "Non-Default"],
                    values=[
                        pd_value,
                        max(0, 1 - pd_value)
                    ],
                    hole=0.72,
                    textinfo="percent",
                    marker=dict(
                        line=dict(
                            color="#071c20",
                            width=3
                        )
                    )
                )
            )

            fig.update_layout(
                title="Default vs Non-Default Probability",
                title_font=dict(color="white", size=18),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                showlegend=True,
                height=350,
                margin=dict(t=60, b=20, l=20, r=20)
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ====================================================
        # RISK BAND DONUT
        # ====================================================

        with chart_col2:

            if pd_value < 0.05:
                band_values = [1, 0, 0, 0]
                labels = [
                    "Low Risk",
                    "Moderate Risk",
                    "High Risk",
                    "Very High Risk"
                ]

            elif pd_value < 0.15:
                band_values = [0, 1, 0, 0]
                labels = [
                    "Low Risk",
                    "Moderate Risk",
                    "High Risk",
                    "Very High Risk"
                ]

            elif pd_value < 0.30:
                band_values = [0, 0, 1, 0]
                labels = [
                    "Low Risk",
                    "Moderate Risk",
                    "High Risk",
                    "Very High Risk"
                ]

            else:
                band_values = [0, 0, 0, 1]
                labels = [
                    "Low Risk",
                    "Moderate Risk",
                    "High Risk",
                    "Very High Risk"
                ]

            fig2 = go.Figure(
                go.Pie(
                    labels=labels,
                    values=band_values,
                    hole=0.72,
                    textinfo="label",
                    marker=dict(
                        line=dict(
                            color="#071c20",
                            width=3
                        )
                    )
                )
            )

            fig2.update_layout(
                title="Applicant Risk Band",
                title_font=dict(color="white", size=18),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                height=350,
                margin=dict(t=60, b=20, l=20, r=20)
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )


# ============================================================
# TAB 3 - RISK ANALYSIS
# ============================================================

with tab3:

    st.markdown(
        '<div class="section-title">Risk Analysis</div>',
        unsafe_allow_html=True
    )

    if result is None:

        st.info("Run a prediction first.")

    else:

        pd_value = float(result.get("PD", 0))
        risk_band = result.get("Risk_Band", "Unknown")

        # ----------------------------------------------------
        # RISK INTERPRETATION
        # ----------------------------------------------------

        with st.expander(
            "🔍 Risk Interpretation",
            expanded=True
        ):

            if pd_value < 0.05:

                st.success(
                    f"The applicant has a relatively low "
                    f"predicted probability of default: "
                    f"**{pd_value * 100:.2f}%**."
                )

            elif pd_value < 0.15:

                st.warning(
                    f"The applicant falls into a moderate-risk "
                    f"profile with a PD of "
                    f"**{pd_value * 100:.2f}%**."
                )

            elif pd_value < 0.30:

                st.warning(
                    f"The applicant shows elevated credit risk. "
                    f"Predicted PD is "
                    f"**{pd_value * 100:.2f}%**."
                )

            else:

                st.error(
                    f"The applicant shows high predicted default "
                    f"risk with a PD of "
                    f"**{pd_value * 100:.2f}%**."
                )

        # ----------------------------------------------------
        # KEY FACTORS
        # ----------------------------------------------------

        with st.expander(
            "📌 Key Risk Factors",
            expanded=True
        ):

            if data:

                factors = []

                if data["Credit_Utilization"] > 0.30:
                    factors.append(
                        "High credit utilization"
                    )

                if data["Debt_to_Income"] > 0.40:
                    factors.append(
                        "High debt-to-income ratio"
                    )

                if data["Number_of_Delinquencies_30"] > 0:
                    factors.append(
                        "30-day delinquency present"
                    )

                if data["Number_of_Delinquencies_60"] > 0:
                    factors.append(
                        "60-day delinquency present"
                    )

                if data["Number_of_Delinquencies_90"] > 0:
                    factors.append(
                        "90-day delinquency present"
                    )

                if data["Employment_Length_Years"] < 2:
                    factors.append(
                        "Short employment history"
                    )

                if data["Credit_History_Years"] < 2:
                    factors.append(
                        "Limited credit history"
                    )

                if len(factors) == 0:

                    st.success(
                        "No major rule-based risk indicators "
                        "were identified from the supplied inputs."
                    )

                else:

                    for factor in factors:
                        st.write("🔴", factor)


        # ----------------------------------------------------
        # RECOMMENDATIONS
        # ----------------------------------------------------

        with st.expander(
            "💡 Recommendations"
        ):

            st.write(
                "• Review applicant credit utilization."
            )

            st.write(
                "• Assess debt-to-income exposure."
            )

            st.write(
                "• Review historical delinquency behavior."
            )

            st.write(
                "• Validate income and employment stability."
            )

            st.write(
                "• Combine the scorecard result with "
                "business credit policy before final approval."
            )


# ============================================================
# TAB 4 - FEATURE IMPACT
# ============================================================

with tab4:

    st.markdown(
        '<div class="section-title">Applicant Feature Indicators</div>',
        unsafe_allow_html=True
    )

    if data is None:

        st.info("Run a prediction first.")

    else:

        st.caption(
            "These visualizations show the applicant's input "
            "indicators. They are not model feature-importance "
            "values unless your model/API explicitly provides "
            "feature importance."
        )

        # ----------------------------------------------------
        # UTILIZATION
        # ----------------------------------------------------

        st.markdown("### Credit Utilization")

        st.progress(
            min(
                max(data["Credit_Utilization"], 0.0),
                1.0
            )
        )

        st.write(
            f"{data['Credit_Utilization'] * 100:.2f}%"
        )

        # ----------------------------------------------------
        # DTI
        # ----------------------------------------------------

        st.markdown("### Debt-to-Income Ratio")

        st.progress(
            min(
                max(data["Debt_to_Income"], 0.0),
                1.0
            )
        )

        st.write(
            f"{data['Debt_to_Income'] * 100:.2f}%"
        )

        # ----------------------------------------------------
        # EMPLOYMENT
        # ----------------------------------------------------

        st.markdown("### Employment Length")

        employment_pct = min(
            data["Employment_Length_Years"] / 20,
            1
        )

        st.progress(employment_pct)

        st.write(
            f"{data['Employment_Length_Years']:.1f} years"
        )

        # ----------------------------------------------------
        # CREDIT HISTORY
        # ----------------------------------------------------

        st.markdown("### Credit History")

        history_pct = min(
            data["Credit_History_Years"] / 30,
            1
        )

        st.progress(history_pct)

        st.write(
            f"{data['Credit_History_Years']:.1f} years"
        )

        # ----------------------------------------------------
        # DELINQUENCIES BAR CHART
        # ----------------------------------------------------

        st.markdown("### Delinquency Profile")

        delinquency_df = pd.DataFrame({
            "Delinquency": [
                "30 Days",
                "60 Days",
                "90 Days"
            ],
            "Count": [
                data["Number_of_Delinquencies_30"],
                data["Number_of_Delinquencies_60"],
                data["Number_of_Delinquencies_90"]
            ]
        })

        fig = px.bar(
            delinquency_df,
            x="Delinquency",
            y="Count",
            text="Count"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            height=350
        )

        fig.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# TAB 5 - CREDIT REPORT
# ============================================================

with tab5:

    st.markdown(
        '<div class="section-title">Applicant Credit Report</div>',
        unsafe_allow_html=True
    )

    if data is None:

        st.info("Run a prediction first.")

    else:

        report_df = pd.DataFrame({
            "Credit Attribute": [
                "Credit History",
                "Credit Utilization",
                "Debt-to-Income",
                "Employment Length",
                "Monthly Income",
                "30-Day Delinquencies",
                "60-Day Delinquencies",
                "90-Day Delinquencies"
            ],

            "Value": [
                f"{data['Credit_History_Years']:.1f} Years",
                f"{data['Credit_Utilization'] * 100:.2f}%",
                f"{data['Debt_to_Income'] * 100:.2f}%",
                f"{data['Employment_Length_Years']:.1f} Years",
                f"₹{data['Monthly_Income']:,.0f}",
                data["Number_of_Delinquencies_30"],
                data["Number_of_Delinquencies_60"],
                data["Number_of_Delinquencies_90"]
            ]
        })

        st.dataframe(
            report_df,
            use_container_width=True,
            hide_index=True
        )

        # ----------------------------------------------------
        # ACCORDION
        # ----------------------------------------------------

        with st.expander(
            "📋 Credit Profile Details",
            expanded=True
        ):

            c1, c2 = st.columns(2)

            with c1:

                st.write(
                    "**Credit History:**",
                    f"{data['Credit_History_Years']:.1f} years"
                )

                st.write(
                    "**Employment:**",
                    f"{data['Employment_Length_Years']:.1f} years"
                )

                st.write(
                    "**Monthly Income:**",
                    f"₹{data['Monthly_Income']:,.0f}"
                )

            with c2:

                st.write(
                    "**Credit Utilization:**",
                    f"{data['Credit_Utilization'] * 100:.2f}%"
                )

                st.write(
                    "**DTI:**",
                    f"{data['Debt_to_Income'] * 100:.2f}%"
                )

                st.write(
                    "**Total Delinquencies:**",
                    (
                        data["Number_of_Delinquencies_30"]
                        + data["Number_of_Delinquencies_60"]
                        + data["Number_of_Delinquencies_90"]
                    )
                )


# ============================================================
# MODEL INFORMATION
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

with st.expander(
    "⚙️ Model Information"
):

    st.write(
        "**Model:** Credit Risk PD Scorecard"
    )

    st.write(
        "**Target:** Probability of Default"
    )

    st.write(
        "**Scorecard Approach:** WOE / Scorecard"
    )

    st.write(
        "**Backend:** FastAPI"
    )

    st.write(
        "**Frontend:** Streamlit"
    )

    st.write(
        "**Prediction Endpoint:** `/predict`"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    DV • Zen Score • Credit Risk Analytics<br>
    Probability of Default Scorecard
</div>
""", unsafe_allow_html=True)
