# Bank Customer Churn Prediction — MLOps Assignment

An end-to-end machine learning application, built as part of the Cambridge
Infotech MLOps hands-on assignment, that predicts whether a bank customer
will churn (exit the bank). The project covers the full local MLOps
workflow: data collection, EDA, preprocessing, feature engineering, model
training, evaluation, hyperparameter tuning, model serialization, and
deployment through a Streamlit web app.

## Project Overview

- **Problem type:** Binary classification (churn vs. retained)
- **Target variable:** `Exited` (1 = customer churned, 0 = customer retained)
- **Models trained:** Logistic Regression, Decision Tree, Random Forest
- **Best model:** Random Forest, tuned with `GridSearchCV` (5-fold CV, F1-optimized)
- **Deployment:** Streamlit application (`app.py`)

## Dataset

- **Source:** [Churn Modelling Dataset — Kaggle](https://www.kaggle.com/datasets/shrutimechlearn/churn-modelling)
- **Description:** 10,000 bank customer records with demographic and
  account information (credit score, geography, gender, age, tenure,
  balance, number of products, credit card status, active member status,
  estimated salary) used to predict customer churn.
- **Target variable:** `Exited`

## Project Structure

```
MLOps Assignment/
├── data/
│   └── dataset.csv
├── models/
│   └── best_model.pkl
├── outputs/                  # EDA plots, confusion matrix, tuning comparison
├── src/
│   ├── eda.py                # Exploratory Data Analysis
│   ├── preprocess.py         # Data cleaning & preprocessing pipeline
│   ├── train.py               # Model training, comparison & tuning
│   └── evaluate.py           # Model evaluation & before/after tuning report
├── app.py                    # Streamlit application
├── requirements.txt
└── README.md
```

## Installation

1. Create and activate a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Training Instructions

Run the scripts from inside the `src/` folder in the following order:

```
cd src
python eda.py          # Generates EDA visualizations into outputs/
python preprocess.py   # Verifies the preprocessing pipeline
python train.py        # Trains, compares & tunes models, saves models/best_model.pkl
python evaluate.py     # Evaluates the saved model, saves confusion matrix & tuning comparison
```

## Running the Streamlit Application

From the project root:

```
streamlit run app.py
```

Then open the local URL shown in the terminal (typically
`http://localhost:8501`), fill in the customer details, and click
**Predict Churn** to see the prediction and confidence score.
