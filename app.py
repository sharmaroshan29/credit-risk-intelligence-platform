import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import joblib


# Page setting
with st.sidebar:
    st.title("🏦 Credit Risk")
    st.markdown("---")
    st.subheader("Navigation")

    page = st.radio(
        "",
        [
            "📊 Risk Assessment",
            "📋 Customer Risk Report",
            "📈 Model Insights"
        ]
    )
    st.markdown("---")
    st.subheader("Model Information")
    st.metric(
        "ROC-AUC",
        "0.87"
    )
    st.metric(
        "Threshold",
        "0.20"
    )

    st.markdown("---")

    st.caption(
        "AI-Powered Credit Risk Assessment"
    )

st.set_page_config(
    page_title="Credit Risk Intelligence Plateform",
    page_icon="🏦",
    layout="wide"
)


# Loading the model

model = joblib.load("models/loan_default_xgb.pkl")

# Layout

st.title("🏦 Credit Risk Intelligence Plateform")
st.markdown("""
            AI - Powered Loan Default Prediction using XGBoost
""")

# st.success("Model Loaded Successfully")
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label = "Model",
        value="XGBoost"
    )
with col2:
    st.metric(
        label="AUC Score",
        value="0.87"
    )

with col3:
    st.metric(
        label = "Threshold",
        value="0.20"
    )


st.divider()
st.subheader("👤 Borrower Profile")

col1, col2 = st.columns(2)

with col1:

    name = st.text_input(
        "Name",
        max_chars= 50
    )

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=35
    )

    dependents = st.number_input(
        "Number Of Dependents",
        min_value=0,
        value=0
    )

    open_credit_lines = st.number_input(
        "Open Credit Lines",
        min_value=0,
        value=5
    )

    


with col2:

    monthly_income = st.number_input(
        "Monthly Income",
        min_value= 0.0,
        value= 50000.0
    )

    debt_ratio = st.number_input(
        "Debt Ratio",
        min_value=0.0,
        value=0.5
    )

    real_estate_loans = st.number_input(
        "Real Estate Loans",
        min_value=0,
        value=1
    )

    revolving_utilization = st.slider(
        "Credit Utilization",
        min_value = 0.0,
        max_value=2.0,
        value=0.5

    )

st.subheader("💰 Financial Health")

late1, late2, late3 = st.columns(3)

with late1:

    late_30 = st.number_input(
            "30-59 Days Late",
            min_value = 0,
            value = 0
        )

with late2:

    late_60 = st.number_input(
            "60-89 Days Late",
            min_value = 0,
            value=0
            )
        
with late3:

    late_90 = st.number_input(
            "90+ Days Late",
            min_value= 0,
            value=0
        )
        
feature_names = ['RevolvingUtilizationOfUnsecuredLines',
 'age',
 'NumberOfTime30-59DaysPastDueNotWorse',
 'DebtRatio',
 'MonthlyIncome',
 'NumberOfOpenCreditLinesAndLoans',
 'NumberOfTimes90DaysLate',
 'NumberRealEstateLoansOrLines',
 'NumberOfTime60-89DaysPastDueNotWorse',
 'NumberOfDependents',
 'DebtIncomeRatio',
 'Totallatepayments']




predict_button = st.button(
    "🔍 Assess credit Risk"
   
)

if predict_button:
    st.write("Name:", name)
    st.write("Age:", age)
    st.write("Income:", monthly_income)
    st.write("Debt Ratio:", debt_ratio)
    total_late_payments = (late_30 + late_60 + late_90)
    debt_income_ratio = (debt_ratio*monthly_income)
    st.write("Total Late Payments:", total_late_payments)
    st.write("Debt Income Ratio:", debt_income_ratio)

    risk_factor = []
    if total_late_payments >= 5:
        risk_factor.append("Multiple late payments detected")
    if debt_ratio > 1:
        risk_factor.append("High debt ratio")
    if monthly_income < 20000:
        risk_factor.append("Low monthly income")
    if revolving_utilization > 0.8:
        risk_factor.append("High credit utilization")
  
    
    input_df = pd.DataFrame({
    'RevolvingUtilizationOfUnsecuredLines': [revolving_utilization],
    'age': [age],
    'NumberOfTime30-59DaysPastDueNotWorse': [late_30],
    'DebtRatio': [debt_ratio],
    'MonthlyIncome': [monthly_income],
    'NumberOfOpenCreditLinesAndLoans': [open_credit_lines],
    'NumberOfTimes90DaysLate': [late_90],
    'NumberRealEstateLoansOrLines': [real_estate_loans],
    'NumberOfTime60-89DaysPastDueNotWorse': [late_60],
    'NumberOfDependents': [dependents],
    'DebtIncomeRatio': [debt_income_ratio],
    'Totallatepayments': [total_late_payments]
    })

    probability = model.predict_proba(input_df)[0][1]
    if probability >= 0.8:
        recommendation = """Reject application or perform detailed review"""
    elif probability >= 0.4:
        recommendation = "Manual Verification recommended"
    else:
        recommendation = "Suitable candidate for loan approval"

    st.session_state["probability"] = probability
    st.session_state["recommendation"] = recommendation
    st.session_state["risk_factor"] = risk_factor

    st.session_state["age"] = age
    st.session_state["monthly_income"] = monthly_income
    st.session_state["debt_ratio"] = debt_ratio
    st.session_state["total_late_payments"] = total_late_payments
    st.session_state["name"] = name

    fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=probability * 100,

        title={
            'text': "Default Probability"
        },

        gauge={
            'axis': {
                'range': [0, 100]
            },

            'bar': {
                'color': "darkred"
            },

            'steps': [
                {'range': [0, 20], 'color': "lightgreen"},
                {'range': [20, 40], 'color': "yellow"},
                {'range': [40, 60], 'color': "orange"},
                {'range': [60, 100], 'color': "red"}
            ]
        }
    )
)
    # Threshold set to 0.2
    best_threshold = 0.2
    prediction = (probability >= best_threshold)
    
    
    st.divider()
    st.subheader("📊 Risk Assessment Result")

    # st.metric(
    #     "Default Probability",
    #     f"{probability*100:.2f}%"
    # )

    left, right = st.columns([2,1])

    with left:
        st.plotly_chart(
        fig,
        use_container_width=True
    )
        
    with right:
        st.metric(
            "Default Probability",
            f"{probability*100:.2f}%"
        )

        st.metric(
            "Threshold",
            "20%"
        )

    if probability < 0.2:
        st.success("🟢 Very Low Risk")

    elif probability < 0.4:
        st.info("🔵 Low Risk")

    elif probability < 0.6:
        st.warning("🟡 Medium Risk")

    elif probability < 0.8:
        st.warning("🟠 High Risk")

    else:
        st.error("🔴 Very High Risk")

    if prediction:
        st.error(
            "⚠ High Probability of Default"

        )

    else:
        st.success(
            "✅ Low Probability of Default"
        )



elif page == "📈 Model Insights":

    st.title("📈 Model Insights")
    st.markdown(
        "Understand how the model makes predictions."
    )
    st.divider()
    st.subheader("Model Performance")
    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric(
            "ROC-AUC",
            "0.87"
        )

    with col2:
        st.metric(
            "Model",
            "XGBoost"
        )

    with col3:
        st.metric(
            "Threshold",
            "0.20"
        )
    st.divider()
    st.subheader("📊 Feature Importance")

    st.image(
        "assets/feature_importance.png",
        use_container_width=True
    )
    
    st.divider()
    st.subheader("🔍 SHAP Explainability")
    st.image(
        "assets/shape_summary.png",
        use_container_width=True
    )

    st.markdown("""
                ### Key Insights

                - Total Late Payments is the strongest predictor of default.
                - Higher Credit Utilization increases default risk.
                - Frequent late payments significantly impact risk.
                - Higher income generally reduces default probability.
                - Age contributes moderately to prediction outcomes.


                """)

    

elif page == "📋 Customer Risk Report":
    st.title("📋 Customer Risk Report")

    if "probability" not in st.session_state:
        st.warning(
            "Please generate a prediction first from the Risk Assessment page."
        )
    else:
        st.subheader("📌 Executive Summary")
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("👤 Borrower Snapshot")
            st.write(
                f"Name: {st.session_state['name']}"
            )

            st.write(
            f"Age: {st.session_state['age']}"
            )

            st.write(
                f"Monthly Income: ₹{st.session_state['monthly_income']:,.0f}"
            )

            st.write(
                f"Debt Ratio: {st.session_state['debt_ratio']}"
            )

            st.write(
                f"Total Late Payments: {st.session_state['total_late_payments']}"
            )

        with col2:
            st.subheader("Key Risk Drivers")
            if st.session_state['probability'] <= 0.2:
                st.info("No such risk involved")
            else:
                for factor in st.session_state["risk_factor"]:
                    st.warning(factor)
        
        with col3:
            st.subheader("💡 Recommendation")
            st.info(
                st.session_state["recommendation"]
            )

        st.divider()
        st.subheader("📝 Executive Narrative")
        summary = f"""
        The customer exhibits a default probability of
        {st.session_state['probability']*100:.2f}%.

        Based on the configured threshold of 20%,
        the applicant has been classified as
        {'High Risk' if st.session_state['probability'] > 0.2 else 'Low Risk'}.

        The assessment indicates that repayment behaviour,
        debt burden and income profile were significant
        contributors to the final decision.
        """

        st.text_area(
            "Report Summary",
            summary,
            height=320
        )