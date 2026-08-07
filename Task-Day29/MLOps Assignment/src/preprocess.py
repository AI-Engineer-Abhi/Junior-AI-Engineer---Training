"""
preprocess.py

Purpose:
Prepare the dataset for machine learning.

Responsibilities:
1. Load dataset
2. Clean data
3. Feature engineering
4. Build preprocessing pipeline
"""

import os

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "dataset.csv")


# ==========================================================
# Load Dataset
# ==========================================================


def load_data():
    """
    Load the dataset.
    """

    df = pd.read_csv(DATA_PATH)

    return df


# ==========================================================
# Data Cleaning
# ==========================================================


def clean_data(df):
    """
    Clean the dataset.
    """

    # Remove duplicate records
    df = df.drop_duplicates()

    # Remove identifier columns
    columns_to_drop = ["RowNumber", "CustomerId", "Surname"]

    df = df.drop(columns=columns_to_drop)

    return df


# ==========================================================
# Features and Target
# ==========================================================


def split_features_target(df):
    """
    Split dataset into features and target.
    """

    X = df.drop("Exited", axis=1)

    y = df["Exited"]

    return X, y


# ==========================================================
# Build Preprocessing Pipeline
# ==========================================================


def build_preprocessor(X):
    """
    Create preprocessing pipeline.
    """

    categorical_features = X.select_dtypes(
        include=["object", "string"]
    ).columns.tolist()

    numerical_features = X.select_dtypes(include=["number"]).columns.tolist()

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("numerical", numeric_pipeline, numerical_features),
            ("categorical", categorical_pipeline, categorical_features),
        ]
    )

    return preprocessor


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PREPROCESSING DATA")
    print("=" * 60)

    df = load_data()

    print(f"Original Dataset Shape : {df.shape}")

    df = clean_data(df)

    print(f"Dataset Shape After Cleaning : {df.shape}")

    X, y = split_features_target(df)

    preprocessor = build_preprocessor(X)

    print("\nCategorical Features")

    print(X.select_dtypes(include=["object", "string"]).columns.tolist())

    print("\nNumerical Features")

    print(X.select_dtypes(include=["number"]).columns.tolist())

    print("\nPreprocessing Pipeline Created Successfully.")
