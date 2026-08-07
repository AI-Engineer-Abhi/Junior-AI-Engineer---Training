"""
eda.py

Purpose:
Perform Exploratory Data Analysis (EDA) on the Bank Customer Churn dataset.

Outputs:
- Console summary
- Visualizations saved in the outputs/ folder
"""

import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "dataset.csv")

OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================================================
# Plot Style
# ==========================================================

sns.set_style("whitegrid")

# ==========================================================
# Load Dataset
# ==========================================================

df = pd.read_csv(DATA_PATH)

# ==========================================================
# Dataset Overview
# ==========================================================

print("=" * 70)
print("DATASET OVERVIEW")
print("=" * 70)

print(f"\nDataset Shape: {df.shape}")

print("\nColumn Names")
print(df.columns.tolist())

print("\nData Types")
print(df.dtypes)

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Records")
print(df.duplicated().sum())

print("\nStatistical Summary")
print(df.describe(include="all"))

# ==========================================================
# Univariate Analysis
# ==========================================================

print("\n" + "=" * 70)
print("UNIVARIATE ANALYSIS")
print("=" * 70)

# Target Distribution
plt.figure(figsize=(6, 4))

sns.countplot(data=df, x="Exited", hue="Exited", palette="viridis", legend=False)

plt.title("Customer Churn Distribution")
plt.xlabel("Exited")
plt.ylabel("Customer Count")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "target_distribution.png"))
plt.close()

# Numerical Features

numerical_columns = [
    "CreditScore",
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "EstimatedSalary",
]

for column in numerical_columns:
    plt.figure(figsize=(7, 4))

    sns.histplot(data=df, x=column, kde=True)

    plt.title(f"{column} Distribution")

    plt.tight_layout()

    plt.savefig(os.path.join(OUTPUT_DIR, f"{column}.png"))

    plt.close()

# Categorical Features

categorical_columns = ["Geography", "Gender"]

for column in categorical_columns:
    plt.figure(figsize=(6, 4))

    sns.countplot(data=df, x=column, palette="Set2", hue=column, legend=False)

    plt.title(f"{column} Distribution")

    plt.xticks(rotation=20)

    plt.tight_layout()

    plt.savefig(os.path.join(OUTPUT_DIR, f"{column}.png"))

    plt.close()

print("Univariate Analysis Completed.")

# ==========================================================
# Bivariate Analysis
# ==========================================================

print("\n" + "=" * 70)
print("BIVARIATE ANALYSIS")
print("=" * 70)

# Geography vs Churn

plt.figure(figsize=(8, 5))

sns.countplot(data=df, x="Geography", hue="Exited")

plt.title("Customer Churn by Geography")

plt.tight_layout()

plt.savefig(os.path.join(OUTPUT_DIR, "churn_by_geography.png"))

plt.close()

# Gender vs Churn

plt.figure(figsize=(6, 5))

sns.countplot(data=df, x="Gender", hue="Exited")

plt.title("Customer Churn by Gender")

plt.tight_layout()

plt.savefig(os.path.join(OUTPUT_DIR, "churn_by_gender.png"))

plt.close()

# Age vs Churn

plt.figure(figsize=(7, 5))

sns.boxplot(data=df, x="Exited", y="Age")

plt.title("Age vs Customer Churn")

plt.tight_layout()

plt.savefig(os.path.join(OUTPUT_DIR, "age_vs_churn.png"))

plt.close()

# Balance vs Churn

plt.figure(figsize=(7, 5))

sns.boxplot(data=df, x="Exited", y="Balance")

plt.title("Balance vs Customer Churn")

plt.tight_layout()

plt.savefig(os.path.join(OUTPUT_DIR, "balance_vs_churn.png"))

plt.close()

print("Bivariate Analysis Completed.")

# ==========================================================
# Correlation Analysis
# ==========================================================

print("\n" + "=" * 70)
print("CORRELATION ANALYSIS")
print("=" * 70)

plt.figure(figsize=(12, 8))

correlation_matrix = df.select_dtypes(include="number").corr()

sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)

plt.title("Correlation Matrix")

plt.tight_layout()

plt.savefig(os.path.join(OUTPUT_DIR, "correlation_matrix.png"))

plt.close()

print("Correlation Matrix Generated.")

# ==========================================================
# Outlier Analysis
# ==========================================================

print("\n" + "=" * 70)
print("OUTLIER ANALYSIS")
print("=" * 70)

outlier_columns = ["CreditScore", "Age", "Balance", "EstimatedSalary"]

for column in outlier_columns:
    plt.figure(figsize=(6, 4))

    sns.boxplot(data=df, y=column)

    plt.title(f"{column} Boxplot")

    plt.tight_layout()

    plt.savefig(os.path.join(OUTPUT_DIR, f"{column}_boxplot.png"))

    plt.close()

print("Outlier Analysis Completed.")

# ==========================================================
# Class Distribution
# ==========================================================

print("\n" + "=" * 70)
print("TARGET CLASS DISTRIBUTION")
print("=" * 70)

distribution = df["Exited"].value_counts(normalize=True) * 100

print(distribution)

# ==========================================================
# EDA Summary
# ==========================================================

print("\n" + "=" * 70)
print("EDA SUMMARY")
print("=" * 70)

print(f"Dataset Shape          : {df.shape}")
print(f"Missing Values         : {df.isnull().sum().sum()}")
print(f"Duplicate Records      : {df.duplicated().sum()}")

print("\nCategorical Features")
print(df.select_dtypes(include=["object", "string"]).columns.tolist())

print("\nNumerical Features")
print(df.select_dtypes(include=["number"]).columns.tolist())

print("\nTarget Column")
print("Exited")

print("\nIdentifier Columns")
print(["RowNumber", "CustomerId", "Surname"])

print("\nEDA Completed Successfully.")
print(f"\nAll visualizations saved to: {OUTPUT_DIR}")
