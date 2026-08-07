"""
evaluate.py

Purpose:
Evaluate the saved best model on the test split and report classification
metrics, a confusion matrix, and a before/after hyperparameter tuning
comparison.
"""

import os

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from preprocess import build_preprocessor, clean_data, load_data, split_features_target
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_DIR = os.path.join(BASE_DIR, "models")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pkl")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================================================
# Load Dataset (identical split used in train.py)
# ==========================================================

df = load_data()
df = clean_data(df)
X, y = split_features_target(df)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# ==========================================================
# Load Saved (Tuned) Model
# ==========================================================

print("=" * 60)
print("MODEL EVALUATION")
print("=" * 60)

best_pipeline = joblib.load(MODEL_PATH)

tuned_predictions = best_pipeline.predict(X_test)

tuned_accuracy = accuracy_score(y_test, tuned_predictions)
tuned_precision = precision_score(y_test, tuned_predictions)
tuned_recall = recall_score(y_test, tuned_predictions)
tuned_f1 = f1_score(y_test, tuned_predictions)

print("\nTuned Model Performance")
print(f"Accuracy : {tuned_accuracy:.4f}")
print(f"Precision: {tuned_precision:.4f}")
print(f"Recall   : {tuned_recall:.4f}")
print(f"F1 Score : {tuned_f1:.4f}")

print("\nClassification Report")
print(classification_report(y_test, tuned_predictions))

# ==========================================================
# Confusion Matrix
# ==========================================================

cm = confusion_matrix(y_test, tuned_predictions)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm, display_labels=["Retained", "Churned"]
)
disp.plot(cmap="Blues", values_format="d")
plt.title("Confusion Matrix - Tuned Model")
plt.tight_layout()

confusion_matrix_path = os.path.join(OUTPUT_DIR, "confusion_matrix.png")
plt.savefig(confusion_matrix_path)
plt.close()

print(f"\nConfusion matrix saved to {confusion_matrix_path}")

# ==========================================================
# Before vs After Tuning Comparison
#
# Re-fit an untuned Random Forest (default hyperparameters) on the same
# split to compare against the tuned model saved by train.py.
# ==========================================================

print("\n" + "=" * 60)
print("BEFORE vs AFTER HYPERPARAMETER TUNING")
print("=" * 60)

preprocessor = build_preprocessor(X)

baseline_pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(random_state=42)),
    ]
)
baseline_pipeline.fit(X_train, y_train)
baseline_predictions = baseline_pipeline.predict(X_test)

baseline_accuracy = accuracy_score(y_test, baseline_predictions)
baseline_f1 = f1_score(y_test, baseline_predictions)

comparison_df = pd.DataFrame(
    [
        {
            "Stage": "Before Tuning (default params)",
            "Accuracy": baseline_accuracy,
            "F1 Score": baseline_f1,
        },
        {
            "Stage": "After Tuning (GridSearchCV)",
            "Accuracy": tuned_accuracy,
            "F1 Score": tuned_f1,
        },
    ]
)

print(comparison_df)

comparison_path = os.path.join(OUTPUT_DIR, "tuning_comparison.csv")
comparison_df.to_csv(comparison_path, index=False)

print(f"\nTuning comparison saved to {comparison_path}")
print("\nEvaluation Completed Successfully.")
