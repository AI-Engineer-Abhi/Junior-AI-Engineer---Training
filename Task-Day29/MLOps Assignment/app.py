"""
app.py

Streamlit web application for the Bank Customer Churn Prediction project.

Loads the tuned Random Forest pipeline saved in models/best_model.pkl and
lets a user enter a customer's details to predict whether they will churn.
"""

import os
import time

import joblib
import pandas as pd
import streamlit as st

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "dataset.csv")

# ==========================================================
# Page Config
# ==========================================================

st.set_page_config(
    page_title="Bank Customer Churn Predictor",
    page_icon="\U0001F3E6",
    layout="centered",
)


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_dataset():
    return pd.read_csv(DATA_PATH)


model = load_model()
dataset = load_dataset()

# ==========================================================
# Sidebar
# ==========================================================

with st.sidebar:
    st.title("Bank Customer Churn Predictor")

    st.markdown(
        "An MLOps demo project that predicts whether a bank customer will "
        "churn (exit the bank), built with a scikit-learn pipeline and "
        "served through Streamlit."
    )

    st.header("Dataset Information")
    st.write(f"**Rows:** {dataset.shape[0]}")
    st.write(f"**Columns:** {dataset.shape[1]}")
    st.write("**Target:** Exited (1 = Churned, 0 = Retained)")

    with st.expander("View sample data"):
        st.dataframe(dataset.head())

    st.header("Model Information")
    st.write("**Algorithm:** Random Forest Classifier")
    st.write("**Tuning:** GridSearchCV (5-fold CV, F1-optimized)")
    st.write("**Pipeline:** Imputation -> Scaling / One-Hot Encoding -> Classifier")

# ==========================================================
# Main Page
# ==========================================================

st.title("Customer Churn Prediction")
st.write("Enter the customer's details below to predict churn risk.")

col1, col2 = st.columns(2)

with col1:
    credit_score = st.number_input(
        "Credit Score", min_value=300, max_value=900, value=650
    )
    geography = st.selectbox("Geography", sorted(dataset["Geography"].unique()))
    gender = st.selectbox("Gender", sorted(dataset["Gender"].unique()))
    age = st.number_input("Age", min_value=18, max_value=100, value=35)
    tenure = st.number_input(
        "Tenure (years with bank)", min_value=0, max_value=10, value=5
    )
    balance = st.number_input("Balance", min_value=0.0, value=50000.0, step=1000.0)

with col2:
    num_of_products = st.number_input("Number of Products", min_value=1, max_value=4, value=1)
    has_cr_card = st.selectbox("Has Credit Card", ["Yes", "No"])
    is_active_member = st.selectbox("Is Active Member", ["Yes", "No"])
    estimated_salary = st.number_input(
        "Estimated Salary", min_value=0.0, value=100000.0, step=1000.0
    )

st.divider()

predict_clicked = st.button("Predict Churn", type="primary")

if predict_clicked:
    with st.spinner("Running prediction..."):
        input_df = pd.DataFrame(
            [
                {
                    "CreditScore": credit_score,
                    "Geography": geography,
                    "Gender": gender,
                    "Age": age,
                    "Tenure": tenure,
                    "Balance": balance,
                    "NumOfProducts": num_of_products,
                    "HasCrCard": 1 if has_cr_card == "Yes" else 0,
                    "IsActiveMember": 1 if is_active_member == "Yes" else 0,
                    "EstimatedSalary": estimated_salary,
                }
            ]
        )

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0]
        confidence = probability[prediction] * 100

        time.sleep(0.3)

    st.subheader("Result")

    metric_col1, metric_col2 = st.columns(2)
    metric_col1.metric("Prediction", "Churn" if prediction == 1 else "Retained")
    metric_col2.metric("Confidence", f"{confidence:.2f}%")

    st.progress(int(confidence))

    if prediction == 1:
        st.warning("Prediction: This customer is likely to churn.")
    else:
        st.success("Prediction: This customer is likely to be retained.")

    with st.expander("View input data"):
        st.dataframe(input_df)
