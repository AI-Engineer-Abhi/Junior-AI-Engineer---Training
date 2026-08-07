"""
train.py

Purpose:
Train multiple machine learning models,
compare their performance,
perform hyperparameter tuning,
and save the best model.
"""

import os

import joblib
import pandas as pd
from preprocess import build_preprocessor, clean_data, load_data, split_features_target
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)

# ==========================================================
# Load Dataset
# ==========================================================

df = load_data()

df = clean_data(df)

X, y = split_features_target(df)

# ==========================================================
# Train Test Split
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# ==========================================================
# Preprocessor
# ==========================================================

preprocessor = build_preprocessor(X)

# ==========================================================
# Models
# ==========================================================

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(random_state=42),
}

results = []

best_model = None
best_pipeline = None
best_f1 = 0

print("=" * 60)
print("MODEL TRAINING")
print("=" * 60)

# ==========================================================
# Train Models
# ==========================================================

for name, model in models.items():
    pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", model)])

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(y_test, predictions)

    recall = recall_score(y_test, predictions)

    f1 = f1_score(y_test, predictions)

    results.append(
        {
            "Model": name,
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1 Score": f1,
        }
    )

    print(f"\n{name}")

    print(f"Accuracy : {accuracy:.4f}")

    print(f"Precision: {precision:.4f}")

    print(f"Recall   : {recall:.4f}")

    print(f"F1 Score : {f1:.4f}")

    if f1 > best_f1:
        best_f1 = f1

        best_model = name

        best_pipeline = pipeline

# ==========================================================
# Comparison Table
# ==========================================================

print("\n" + "=" * 60)

print("MODEL COMPARISON")

print("=" * 60)

results_df = pd.DataFrame(results)

print(results_df)

print("\nBest Model:", best_model)

# ==========================================================
# Hyperparameter Tuning
# ==========================================================

print("\n" + "=" * 60)

print("GRID SEARCH")

print("=" * 60)

if best_model == "Random Forest":
    parameter_grid = {
        "classifier__n_estimators": [100, 200],
        "classifier__max_depth": [5, 10, None],
        "classifier__min_samples_split": [2, 5],
    }

elif best_model == "Decision Tree":
    parameter_grid = {
        "classifier__max_depth": [3, 5, 10, None],
        "classifier__min_samples_split": [2, 5, 10],
    }

else:
    parameter_grid = {"classifier__C": [0.1, 1, 10]}

if best_pipeline is None:
    raise RuntimeError("No valid model pipeline was selected.")

grid_search = GridSearchCV(
    estimator=best_pipeline, param_grid=parameter_grid, cv=5, scoring="f1", n_jobs=-1
)

grid_search.fit(X_train, y_train)

print("\nBest Parameters")

print(grid_search.best_params_)

print("\nBest Cross Validation F1")

print(grid_search.best_score_)

# ==========================================================
# Save Model
# ==========================================================

model_path = os.path.join(MODEL_DIR, "best_model.pkl")

joblib.dump(grid_search.best_estimator_, model_path)

print("\nBest model saved successfully.")

print(model_path)
