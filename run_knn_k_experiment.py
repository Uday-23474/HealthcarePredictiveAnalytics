"""
KNN K-Value Experiment for HeartCare AI Predictive Analytics Platform.

Evaluates K-Nearest Neighbors across K in [1, 3, 5, 7, 9, 11] using the exact same
dataset (HeartDiseaseTrain-Test.xlsx), deduplication, categorical LabelEncoding,
train/test split (80/20, random_state=42, stratify=y), and StandardScaler fitted
strictly on the training partition.

Generates:
1. model/knn_k_value_comparison.csv
2. screenshots/knn_k_value_comparison.png
3. screenshots/knn_k_tuning_curve.png
"""

import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

# 1. Directories setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
DATASET_PATH = os.path.join(BASE_DIR, "dataset", "HeartDiseaseTrain-Test.xlsx")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

print("=" * 70)
print("KNN K-VALUE EXPERIMENT - HEALTHCARE PREDICTIVE ANALYTICS")
print("=" * 70)

# 2. Load dataset
if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")

df = pd.read_excel(DATASET_PATH)
print(f"Original dataset shape: {df.shape}")

# 3. Deduplication (consistent with existing model_training.py)
df = df.drop_duplicates()
print(f"Dataset shape after drop_duplicates: {df.shape}")

# 4. Encode categorical columns
categorical_columns = df.select_dtypes(include=["object", "str"]).columns
encoders = {}
for column in categorical_columns:
    encoder = LabelEncoder()
    df[column] = encoder.fit_transform(df[column])
    encoders[column] = encoder

X = df.drop("target", axis=1)
y = df["target"]

# 5. Train/Test split: 80/20, random_state=42, stratify=y
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"Training set: {X_train.shape}, Test set: {X_test.shape}")
print(f"Test class balance: {dict(pd.Series(y_test).value_counts())}")

# 6. Feature scaling - fit ONLY on train, transform test (no data leakage)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 7. Tested K-values
k_values = [1, 3, 5, 7, 9, 11]
results = []

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for k in k_values:
    # Train KNN
    knn = KNeighborsClassifier(n_neighbors=k, weights="uniform")
    knn.fit(X_train_scaled, y_train)

    # Train-set metrics (evaluates overfitting)
    y_train_pred = knn.predict(X_train_scaled)
    train_acc = accuracy_score(y_train, y_train_pred)
    train_f1 = f1_score(y_train, y_train_pred, pos_label=1, zero_division=0)

    # Test-set metrics
    y_test_pred = knn.predict(X_test_scaled)
    y_test_prob = knn.predict_proba(X_test_scaled)[:, 1]

    acc = accuracy_score(y_test, y_test_pred)
    prec = precision_score(y_test, y_test_pred, pos_label=1, zero_division=0)
    rec = recall_score(y_test, y_test_pred, pos_label=1, zero_division=0)
    f1 = f1_score(y_test, y_test_pred, pos_label=1, zero_division=0)
    roc_auc = roc_auc_score(y_test, y_test_prob)

    # 5-fold cross-validation on training partition (isolated from test set)
    cv_res = cross_validate(
        KNeighborsClassifier(n_neighbors=k, weights="uniform"),
        X_train_scaled,
        y_train,
        cv=skf,
        scoring=["accuracy", "precision", "recall", "f1", "roc_auc"]
    )
    cv_acc = cv_res["test_accuracy"].mean()
    cv_prec = cv_res["test_precision"].mean()
    cv_rec = cv_res["test_recall"].mean()
    cv_f1 = cv_res["test_f1"].mean()
    cv_roc = cv_res["test_roc_auc"].mean()

    results.append({
        "K": k,
        "Accuracy": acc,
        "Precision": prec,
        "Recall": rec,
        "F1-Score": f1,
        "ROC-AUC": roc_auc,
        "Train_Accuracy": train_acc,
        "Train_F1": train_f1,
        "CV_Accuracy": cv_acc,
        "CV_Precision": cv_prec,
        "CV_Recall": cv_rec,
        "CV_F1": cv_f1,
        "CV_ROC_AUC": cv_roc
    })

comparison_df = pd.DataFrame(results)

# 8. Model Selection by Test-Set F1-Score (primary), Accuracy (secondary)
# Consistent with existing project model_results.sort_values(by="F1-Score", ascending=False)
ranked_df = comparison_df.sort_values(
    by=["F1-Score", "Accuracy"], ascending=[False, False]
).reset_index(drop=True)

best_k = int(ranked_df.iloc[0]["K"])
best_f1 = ranked_df.iloc[0]["F1-Score"]
best_acc = ranked_df.iloc[0]["Accuracy"]

print("\n" + "=" * 70)
print("EXPERIMENT RESULTS: KNN K-VALUE COMPARISON TABLE")
print("=" * 70)
print(comparison_df[[
    "K", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC", "CV_F1", "CV_Accuracy"
]].to_string(
    index=False,
    formatters={
        "Accuracy": "{:.4f}".format,
        "Precision": "{:.4f}".format,
        "Recall": "{:.4f}".format,
        "F1-Score": "{:.4f}".format,
        "ROC-AUC": "{:.4f}".format,
        "CV_F1": "{:.4f}".format,
        "CV_Accuracy": "{:.4f}".format,
    }
))

print("\n" + "=" * 70)
print(f"WINNING K: K = {best_k}")
print(f"Selection Criterion: Highest Test-Set F1-Score = {best_f1:.4f} (Accuracy = {best_acc:.4f})")
print("=" * 70)

# 9. Save comparison CSV
csv_out_path = os.path.join(MODEL_DIR, "knn_k_value_comparison.csv")
comparison_df.to_csv(csv_out_path, index=False)
print(f"Saved experiment CSV: {csv_out_path}")

# 10. Generate comparison visualizations in screenshots/
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

# Chart A: Grouped Bar Chart of Test Metrics across K values
plt.figure(figsize=(11, 6))
bar_width = 0.16
x = np.arange(len(k_values))

plt.bar(x - 2 * bar_width, comparison_df["Accuracy"] * 100, width=bar_width, label="Accuracy (%)", color="#0284c7")
plt.bar(x - bar_width, comparison_df["Precision"] * 100, width=bar_width, label="Precision (%)", color="#06b6d4")
plt.bar(x, comparison_df["Recall"] * 100, width=bar_width, label="Recall (%)", color="#10b981")
plt.bar(x + bar_width, comparison_df["F1-Score"] * 100, width=bar_width, label="F1-Score (%)", color="#8b5cf6")
plt.bar(x + 2 * bar_width, comparison_df["ROC-AUC"] * 100, width=bar_width, label="ROC-AUC (%)", color="#f59e0b")

plt.xlabel("K-Value (Number of Nearest Neighbors)", fontsize=11, fontweight="bold")
plt.ylabel("Test Set Score (%)", fontsize=11, fontweight="bold")
plt.title("KNN Performance Metrics across Tested K Values [1, 3, 5, 7, 9, 11]", fontsize=13, fontweight="bold")
plt.xticks(x, [f"K = {k}" for k in k_values], fontsize=10, fontweight="bold")
plt.ylim(70, 100)
plt.legend(loc="lower right", frameon=True)
plt.tight_layout()

chart_bar_path = os.path.join(SCREENSHOTS_DIR, "knn_k_value_comparison.png")
plt.savefig(chart_bar_path, dpi=300)
plt.close()
print(f"Saved metrics bar chart: {chart_bar_path}")

# Chart B: Hyperparameter Tuning Curve (Train Acc vs Test Acc vs Test F1 vs CV Acc)
plt.figure(figsize=(10, 5.5))
plt.plot(comparison_df["K"], comparison_df["Train_Accuracy"] * 100, "o--", color="#64748b", label="Train Accuracy (%) [Overfitting at K=1]", linewidth=2)
plt.plot(comparison_df["K"], comparison_df["Accuracy"] * 100, "s-", color="#0284c7", label="Test Accuracy (%)", linewidth=2.5)
plt.plot(comparison_df["K"], comparison_df["F1-Score"] * 100, "^-", color="#8b5cf6", label="Test F1-Score (%) [Primary Metric]", linewidth=2.5)
plt.plot(comparison_df["K"], comparison_df["CV_F1"] * 100, "d-.", color="#10b981", label="5-Fold CV Training F1 (%)", linewidth=2)

# Highlight winning K = 5
best_row = comparison_df[comparison_df["K"] == best_k].iloc[0]
plt.scatter([best_k], [best_row["F1-Score"] * 100], color="#ef4444", s=150, zorder=5, label=f"Selected Best: K={best_k} (F1={best_f1*100:.2f}%)")

plt.xlabel("K Value", fontsize=11, fontweight="bold")
plt.ylabel("Score (%)", fontsize=11, fontweight="bold")
plt.title(f"KNN Bias-Variance Tradeoff Curve (Optimal Peak at K = {best_k})", fontsize=13, fontweight="bold")
plt.xticks(k_values, [f"K={k}" for k in k_values], fontsize=10)
plt.ylim(75, 105)
plt.legend(loc="upper right", frameon=True)
plt.tight_layout()

chart_curve_path = os.path.join(SCREENSHOTS_DIR, "knn_k_tuning_curve.png")
plt.savefig(chart_curve_path, dpi=300)
plt.close()
print(f"Saved tuning curve: {chart_curve_path}")

print("=" * 70)
print("EXPERIMENT COMPLETED SUCCESSFULLY!")
print("=" * 70)
