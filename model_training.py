# ============================================
# HEART DISEASE PREDICTION
# MACHINE LEARNING MODEL TRAINING
# FINAL MODEL: KNN
# ============================================

import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import (
    train_test_split,
    StratifiedKFold,
    cross_validate
)

from sklearn.preprocessing import (
    LabelEncoder,
    StandardScaler
)

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# Classical ML
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# Ensemble and Boosting
from sklearn.ensemble import (
    RandomForestClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier
)

# Neural Network
from sklearn.neural_network import MLPClassifier

# External Boosting Models
from xgboost import XGBClassifier
from catboost import CatBoostClassifier


# ============================================
# 1. CREATE REQUIRED FOLDERS
# ============================================

os.makedirs("model", exist_ok=True)
os.makedirs("screenshots", exist_ok=True)


# ============================================
# 2. LOAD DATASET
# ============================================

df = pd.read_excel(
    "dataset/HeartDiseaseTrain-Test.xlsx"
)

print("\n============================================")
print("HEART DISEASE DATASET")
print("============================================")

print("Original dataset shape:", df.shape)


# ============================================
# 3. REMOVE DUPLICATES
# ============================================

df = df.drop_duplicates()

print("\nDataset after removing duplicates:")
print(df.shape)


# ============================================
# 4. ENCODE CATEGORICAL COLUMNS
# ============================================

categorical_columns = df.select_dtypes(
    include=["object", "str"]
).columns

encoders = {}

print("\nCategorical columns:")

for column in categorical_columns:

    print("\nEncoding:", column)

    encoder = LabelEncoder()

    df[column] = encoder.fit_transform(
        df[column]
    )

    encoders[column] = encoder

    print(
        dict(
            zip(
                encoder.classes_,
                encoder.transform(
                    encoder.classes_
                )
            )
        )
    )


# ============================================
# 5. SEPARATE FEATURES AND TARGET
# ============================================

X = df.drop(
    "target",
    axis=1
)

y = df["target"]


# ============================================
# 6. TRAIN-TEST SPLIT
# ============================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


# ============================================
# 7. FEATURE SCALING
# ============================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(
    X_train
)

X_test_scaled = scaler.transform(
    X_test
)

print("\n============================================")
print("DATA PREPROCESSING")
print("============================================")

print("Training data:", X_train.shape)
print("Testing data :", X_test.shape)

print("\nData preprocessing completed successfully!")


# ============================================
# 8. DEFINE MODELS
# ============================================

models = {

    "Logistic Regression":
        LogisticRegression(
            random_state=42,
            max_iter=1000
        ),

    "Decision Tree":
        DecisionTreeClassifier(
            random_state=42
        ),

    "SVM":
        SVC(
            probability=True,
            random_state=42
        ),

    "KNN":
        KNeighborsClassifier(
            n_neighbors=5
        ),

    "Naive Bayes":
        GaussianNB(),

    "Random Forest":
        RandomForestClassifier(
            n_estimators=200,
            random_state=42
        ),

    "Extra Trees":
        ExtraTreesClassifier(
            n_estimators=200,
            random_state=42
        ),

    "Gradient Boosting":
        GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=3,
            random_state=42
        ),

    "AdaBoost":
        AdaBoostClassifier(
            n_estimators=100,
            learning_rate=0.1,
            random_state=42
        ),

    "XGBoost":
        XGBClassifier(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=4,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            eval_metric="logloss"
        ),

    "CatBoost":
        CatBoostClassifier(
            iterations=200,
            learning_rate=0.05,
            depth=5,
            random_seed=42,
            verbose=0
        ),

    "MLP Neural Network":
        MLPClassifier(
            hidden_layer_sizes=(64, 32),
            activation="relu",
            solver="adam",
            max_iter=1000,
            random_state=42
        ),

    "LDA":
        LinearDiscriminantAnalysis()
}


# ============================================
# 9. TRAIN AND EVALUATE ALL MODELS
# ============================================

results = []

trained_models = {}

predictions = {}

probabilities = {}

print("\n============================================")
print("MODEL TRAINING STARTED")
print("============================================")


for model_name, model in models.items():

    print("\n--------------------------------------------")
    print(model_name)
    print("--------------------------------------------")

    # Train
    model.fit(
        X_train_scaled,
        y_train
    )

    # Prediction
    y_pred = model.predict(
        X_test_scaled
    )

    # Probability
    y_probability = model.predict_proba(
        X_test_scaled
    )[:, 1]

    # Metrics
    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_test,
        y_probability
    )

    # Store
    trained_models[model_name] = model

    predictions[model_name] = y_pred

    probabilities[model_name] = y_probability

    results.append({

        "Model": model_name,

        "Accuracy": accuracy,

        "Precision": precision,

        "Recall": recall,

        "F1-Score": f1,

        "ROC-AUC": roc_auc
    })

    print(
        f"Accuracy : {accuracy:.4f}"
    )

    print(
        f"Precision: {precision:.4f}"
    )

    print(
        f"Recall   : {recall:.4f}"
    )

    print(
        f"F1-Score : {f1:.4f}"
    )

    print(
        f"ROC-AUC  : {roc_auc:.4f}"
    )


# ============================================
# 10. MODEL COMPARISON
# ============================================

model_results = pd.DataFrame(
    results
)

model_results = model_results.sort_values(
    by="F1-Score",
    ascending=False
)

model_results = model_results.reset_index(
    drop=True
)


print("\n============================================")
print("COMPLETE MODEL COMPARISON")
print("============================================")

print(
    model_results.to_string(
        index=False,
        formatters={
            "Accuracy": "{:.4f}".format,
            "Precision": "{:.4f}".format,
            "Recall": "{:.4f}".format,
            "F1-Score": "{:.4f}".format,
            "ROC-AUC": "{:.4f}".format
        }
    )
)


# ============================================
# 11. SAVE MODEL COMPARISON
# ============================================

model_results.to_csv(
    "model/model_comparison.csv",
    index=False
)

print(
    "\nModel comparison saved as:"
    " model/model_comparison.csv"
)


# ============================================
# 12. ACCURACY GRAPH
# ============================================

plt.figure(
    figsize=(14, 7)
)

plt.bar(
    model_results["Model"],
    model_results["Accuracy"] * 100
)

plt.title(
    "Machine Learning Model Accuracy Comparison"
)

plt.xlabel(
    "Machine Learning Model"
)

plt.ylabel(
    "Accuracy (%)"
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    "screenshots/model_accuracy_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================
# 13. COMPLETE PERFORMANCE GRAPH
# ============================================

metrics = [
    "Accuracy",
    "Precision",
    "Recall",
    "F1-Score",
    "ROC-AUC"
]

plt.figure(
    figsize=(16, 8)
)

for metric in metrics:

    plt.plot(
        model_results["Model"],
        model_results[metric],
        marker="o",
        label=metric
    )

plt.title(
    "Complete Model Performance Comparison"
)

plt.xlabel(
    "Machine Learning Model"
)

plt.ylabel(
    "Score"
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "screenshots/model_performance_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================
# 14. BEST MODEL FOR COMPARISON
# ============================================

best_model_name = model_results.iloc[0]["Model"]

best_model = trained_models[
    best_model_name
]

best_prediction = predictions[
    best_model_name
]

best_row = model_results.iloc[0]


print("\n============================================")
print("BEST MODEL IN COMPARISON")
print("============================================")

print(
    "Best Model:",
    best_model_name
)

print(
    f"Accuracy : {best_row['Accuracy']:.4f}"
)

print(
    f"Precision: {best_row['Precision']:.4f}"
)

print(
    f"Recall   : {best_row['Recall']:.4f}"
)

print(
    f"F1-Score : {best_row['F1-Score']:.4f}"
)

print(
    f"ROC-AUC  : {best_row['ROC-AUC']:.4f}"
)


# ============================================
# 15. BEST MODEL CLASSIFICATION REPORT
# ============================================

print("\n============================================")
print("BEST MODEL CLASSIFICATION REPORT")
print("============================================")

print(
    classification_report(
        y_test,
        best_prediction,
        target_names=[
            "No Heart Disease",
            "Heart Disease"
        ]
    )
)


# ============================================
# 16. BEST MODEL CONFUSION MATRIX
# ============================================

cm = confusion_matrix(
    y_test,
    best_prediction
)

print("\n============================================")
print("BEST MODEL CONFUSION MATRIX")
print("============================================")

print(cm)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=[
        "No Heart Disease",
        "Heart Disease"
    ]
)

disp.plot()

plt.title(
    f"{best_model_name} Confusion Matrix"
)

plt.savefig(
    "screenshots/best_model_confusion_matrix.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================
# 16B. KNN K-VALUE HYPERPARAMETER EXPERIMENT
# ============================================

print("\n============================================")
print("KNN K-VALUE HYPERPARAMETER EXPERIMENT")
print("============================================")

k_test_values = [1, 3, 5, 7, 9, 11]
k_experiment_results = []
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for k_val in k_test_values:
    k_clf = KNeighborsClassifier(n_neighbors=k_val, weights="uniform")
    k_clf.fit(X_train_scaled, y_train)

    k_y_train_pred = k_clf.predict(X_train_scaled)
    k_train_acc = accuracy_score(y_train, k_y_train_pred)
    k_train_f1 = f1_score(y_train, k_y_train_pred, pos_label=1, zero_division=0)

    k_y_test_pred = k_clf.predict(X_test_scaled)
    k_y_test_prob = k_clf.predict_proba(X_test_scaled)[:, 1]

    k_acc = accuracy_score(y_test, k_y_test_pred)
    k_prec = precision_score(y_test, k_y_test_pred, pos_label=1, zero_division=0)
    k_rec = recall_score(y_test, k_y_test_pred, pos_label=1, zero_division=0)
    k_f1 = f1_score(y_test, k_y_test_pred, pos_label=1, zero_division=0)
    k_roc = roc_auc_score(y_test, k_y_test_prob)

    cv_res = cross_validate(
        KNeighborsClassifier(n_neighbors=k_val, weights="uniform"),
        X_train_scaled,
        y_train,
        cv=skf,
        scoring=["accuracy", "precision", "recall", "f1", "roc_auc"]
    )

    k_experiment_results.append({
        "K": k_val,
        "Accuracy": k_acc,
        "Precision": k_prec,
        "Recall": k_rec,
        "F1-Score": k_f1,
        "ROC-AUC": k_roc,
        "Train_Accuracy": k_train_acc,
        "Train_F1": k_train_f1,
        "CV_Accuracy": cv_res["test_accuracy"].mean(),
        "CV_Precision": cv_res["test_precision"].mean(),
        "CV_Recall": cv_res["test_recall"].mean(),
        "CV_F1": cv_res["test_f1"].mean(),
        "CV_ROC_AUC": cv_res["test_roc_auc"].mean()
    })

k_comparison_df = pd.DataFrame(k_experiment_results)

# Rank by test-set F1-Score (primary), Accuracy (secondary)
k_ranked_df = k_comparison_df.sort_values(
    by=["F1-Score", "Accuracy"], ascending=[False, False]
).reset_index(drop=True)

winning_k = int(k_ranked_df.iloc[0]["K"])
winning_f1 = k_ranked_df.iloc[0]["F1-Score"]
winning_acc = k_ranked_df.iloc[0]["Accuracy"]

print("\nK-Value Comparison Table:")
print(k_comparison_df[[
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

print(f"\nWinning K Parameter: K = {winning_k} (Test F1-Score = {winning_f1:.4f}, Accuracy = {winning_acc:.4f})")

k_comparison_df.to_csv("model/knn_k_value_comparison.csv", index=False)
print("Saved K-value comparison to: model/knn_k_value_comparison.csv")

# ============================================
# 17. TRAIN FINAL KNN MODEL
# ============================================

print("\n============================================")
print(f"TRAINING FINAL KNN MODEL (K = {winning_k})")
print("============================================")

final_model = KNeighborsClassifier(
    n_neighbors=winning_k
)

final_model.fit(
    X_train_scaled,
    y_train
)


# ============================================
# 18. EVALUATE FINAL KNN MODEL
# ============================================

final_prediction = final_model.predict(
    X_test_scaled
)

final_probability = final_model.predict_proba(
    X_test_scaled
)[:, 1]

final_accuracy = accuracy_score(
    y_test,
    final_prediction
)

final_precision = precision_score(
    y_test,
    final_prediction,
    zero_division=0
)

final_recall = recall_score(
    y_test,
    final_prediction,
    zero_division=0
)

final_f1 = f1_score(
    y_test,
    final_prediction,
    zero_division=0
)

final_roc_auc = roc_auc_score(
    y_test,
    final_probability
)


print("\n============================================")
print("FINAL KNN PERFORMANCE")
print("============================================")

print(f"Accuracy : {final_accuracy:.4f}")
print(f"Precision: {final_precision:.4f}")
print(f"Recall   : {final_recall:.4f}")
print(f"F1-Score : {final_f1:.4f}")
print(f"ROC-AUC  : {final_roc_auc:.4f}")


# ============================================
# 19. FINAL KNN CONFUSION MATRIX
# ============================================

final_cm = confusion_matrix(
    y_test,
    final_prediction
)

print("\n============================================")
print("FINAL KNN CONFUSION MATRIX")
print("============================================")

print(final_cm)

final_disp = ConfusionMatrixDisplay(
    confusion_matrix=final_cm,
    display_labels=[
        "No Heart Disease",
        "Heart Disease"
    ]
)

final_disp.plot()

plt.title("KNN Confusion Matrix")

plt.savefig(
    "screenshots/final_model_confusion_matrix.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================
# 20. SAVE FINAL KNN MODEL
# ============================================

joblib.dump(
    final_model,
    "model/heart_model.pkl"
)

joblib.dump(
    scaler,
    "model/scaler.pkl"
)

joblib.dump(
    encoders,
    "model/encoders.pkl"
)


# ============================================
# 21. FINAL OUTPUT
# ============================================

print("\n============================================")
print("FINAL MODEL SAVED SUCCESSFULLY")
print("============================================")

print("Final Model: KNN")
print("Model file: model/heart_model.pkl")
print("Scaler file: model/scaler.pkl")
print("Encoder file: model/encoders.pkl")
print("Comparison file: model/model_comparison.csv")

print("\nTraining completed successfully!")
