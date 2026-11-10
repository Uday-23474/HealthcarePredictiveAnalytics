"""HeartCare AI: Enterprise Clinical Decision Support & Predictive Analytics Platform.

Serves the front end with full machine learning inference, multi-model consensus,
MySQL persistence, Explainable AI (XAI), What-If simulation, and benchmark studio.
"""

import math
import os
import io
import csv
import random
import json
from datetime import datetime, timedelta

import joblib
import pandas as pd
import numpy as np
import mysql.connector
from flask import (
    Flask, abort, redirect, render_template, request,
    url_for, jsonify, Response
)

import sys

FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
if FRONTEND_DIR not in sys.path:
    sys.path.insert(0, FRONTEND_DIR)

from form_spec import GROUPS, display_rows, iter_fields, validate

# --------------------------------------------------------------------------
# Paths & ML Model Initialization
# --------------------------------------------------------------------------
BASE_DIR = os.path.dirname(FRONTEND_DIR)
MODEL_DIR = os.path.join(BASE_DIR, "model")
KNN_PATH = os.path.join(MODEL_DIR, "heart_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
ENCODERS_PATH = os.path.join(MODEL_DIR, "encoders.pkl")
ENSEMBLE_PATH = os.path.join(MODEL_DIR, "ensemble_models.pkl")
BENCHMARK_PATH = os.path.join(MODEL_DIR, "model_comparison.csv")
KNN_K_COMP_PATH = os.path.join(MODEL_DIR, "knn_k_value_comparison.csv")

# Load primary KNN model, scaler, and label encoders
try:
    model = joblib.load(KNN_PATH)
    scaler = joblib.load(SCALER_PATH)
    encoders = joblib.load(ENCODERS_PATH)
    print("=" * 60)
    print("HeartCare AI - ML Models & Preprocessing Engines Loaded")
    print(f"Primary KNN Model: {KNN_PATH}")
    print(f"Scaler:           {SCALER_PATH}")
    print(f"Encoders:         {ENCODERS_PATH}")
except Exception as e:
    raise RuntimeError(f"Failed to load core ML models: {e}")

# Load or initialize multi-model ensemble
try:
    if os.path.exists(ENSEMBLE_PATH):
        ensemble_models = joblib.load(ENSEMBLE_PATH)
        print(f"Multi-Model Ensemble loaded: {list(ensemble_models.keys())}")
    else:
        ensemble_models = {"KNN (Primary)": model}
except Exception as e:
    print("Ensemble loading note:", e)
    ensemble_models = {"KNN (Primary)": model}

# --------------------------------------------------------------------------
# MySQL Database Configuration
# --------------------------------------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "64647",
    "database": "healthcare_predictive_analytics"
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# In-memory fallback if MySQL is ever temporarily unavailable
_MEM_RECORDS = []

# Flask App setup
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "heartcare-ai-clinical-platform-key")

# Risk bands
LOW_MAX = 30.0
HIGH_MIN = 60.0

def risk_level(probability):
    if probability < LOW_MAX:
        return "Low"
    if probability >= HIGH_MIN:
        return "High"
    return "Moderate"


# --------------------------------------------------------------------------
# Field Normalization & Clinical Mapping
# --------------------------------------------------------------------------
def map_frontend_to_clinical(v):
    """
    Maps frontend form values to the exact 13 features expected by
    the trained Scaler and Encoders.
    """
    vessels_raw = str(v.get("vessels") or v.get("vessels_colored_by_flourosopy") or "Zero")
    thal_raw = str(v.get("thalassemia") or "Normal")
    if "revers" in thal_raw.lower():
        thal_cleaned = "Reversable Defect"
    elif "fixed" in thal_raw.lower():
        thal_cleaned = "Fixed Defect"
    else:
        thal_cleaned = "Normal"

    fbs_raw = str(v.get("fasting_blood_sugar") or "Lower than 120 mg/ml")
    if "greater" in fbs_raw.lower() or ">" in fbs_raw:
        fbs_cleaned = "Greater than 120 mg/ml"
    else:
        fbs_cleaned = "Lower than 120 mg/ml"

    return {
        "age": int(v["age"]),
        "sex": str(v["sex"]),
        "chest_pain_type": str(v["chest_pain_type"]),
        "resting_blood_pressure": float(v.get("resting_bp") or v.get("resting_blood_pressure") or 120),
        "cholestoral": float(v.get("cholesterol") or v.get("cholestoral") or 200),
        "fasting_blood_sugar": fbs_cleaned,
        "rest_ecg": str(v.get("rest_ecg") or "Normal"),
        "Max_heart_rate": float(v.get("max_heart_rate") or v.get("Max_heart_rate") or 140),
        "exercise_induced_angina": str(v.get("exercise_angina") or v.get("exercise_induced_angina") or "No"),
        "oldpeak": float(v.get("oldpeak") or 0.0),
        "slope": str(v.get("slope") or "Upsloping"),
        "vessels_colored_by_flourosopy": vessels_raw,
        "thalassemia": thal_cleaned
    }


# --------------------------------------------------------------------------
# Explainable AI (XAI) & Clinical Recommendations
# --------------------------------------------------------------------------
def evaluate_clinical_insights(data, probability, risk_str):
    flags = []
    recs = []

    # 1. Blood Pressure
    try:
        bp = float(data.get("resting_blood_pressure", 0))
        if bp >= 140:
            flags.append(f"Stage 2 Hypertension ({bp} mmHg - Elevated systemic vascular resistance)")
        elif bp >= 130:
            flags.append(f"Stage 1 Hypertension ({bp} mmHg - Moderate cardiovascular strain)")
    except Exception:
        pass

    # 2. Serum Cholesterol
    try:
        chol = float(data.get("cholestoral", 0))
        if chol >= 240:
            flags.append(f"Hypercholesterolemia ({chol} mg/dL - High atherogenic plaque risk)")
        elif chol >= 200:
            flags.append(f"Borderline High Cholesterol ({chol} mg/dL)")
    except Exception:
        pass

    # 3. Fasting Blood Sugar
    fbs = str(data.get("fasting_blood_sugar", ""))
    if "greater" in fbs.lower():
        flags.append("Elevated Fasting Blood Glucose (>120 mg/dL - Diabetic cardiovascular comorbidity)")

    # 4. Oldpeak ST Depression
    try:
        oldpeak = float(data.get("oldpeak", 0))
        if oldpeak >= 2.0:
            flags.append(f"Marked ST Depression ({oldpeak} mm - High correlation with myocardial ischemia)")
        elif oldpeak >= 1.0:
            flags.append(f"Abnormal ST Depression ({oldpeak} mm - Electrocardiographic sign of cardiac strain)")
    except Exception:
        pass

    # 5. Maximum Heart Rate
    try:
        max_hr = float(data.get("Max_heart_rate", 0))
        if max_hr < 115:
            flags.append(f"Reduced Maximum Exercise Heart Rate ({max_hr} bpm - Chronotropic incompetence marker)")
    except Exception:
        pass

    # 6. Fluoroscopy Vessels
    vessels = str(data.get("vessels_colored_by_flourosopy", "")).strip().lower()
    if vessels in ["one", "two", "three", "1", "2", "3"]:
        flags.append(f"Fluoroscopy Vessel Occlusion ({data.get('vessels_colored_by_flourosopy')} vessel(s) detected)")

    # Recommendations
    prob_val = float(probability or 0)
    if risk_str == "High" or prob_val >= HIGH_MIN:
        recs.append("Immediate comprehensive evaluation with a board-certified cardiologist.")
        recs.append("Schedule 12-lead ECG and comprehensive Transthoracic Echocardiogram (TTE).")
        recs.append("Evaluate necessity for diagnostic Coronary Angiography or stress imaging.")
        recs.append("Initiate therapeutic lifestyle changes: strict dietary sodium reduction (<2g/day) and cardiac Mediterranean diet.")
        recs.append("Avoid heavy isometric or sudden anaerobic exertion pending clinical clearance.")
    elif risk_str == "Moderate" or prob_val >= LOW_MAX:
        recs.append("Schedule preventative cardiovascular examination with primary care physician within 30 days.")
        recs.append("Engage in 30 minutes of moderate aerobic exercise 5 days/week (brisk walking, cycling).")
        recs.append("Adopt dietary lipid management: increase dietary fiber and reduce saturated fats.")
        recs.append("Conduct weekly home blood pressure tracking and repeat fasting lipid panel in 90 days.")
    else:
        recs.append("Maintain active cardiovascular wellness routine (>150 minutes moderate exercise per week).")
        recs.append("Continue balanced Mediterranean-style, whole-foods nutrition.")
        recs.append("Schedule annual routine preventative screening and vitals check.")

    return flags, recs


def evaluate_ensemble(input_scaled):
    votes = {}
    detected_count = 0
    total_models = len(ensemble_models)

    for name, m in ensemble_models.items():
        try:
            pred = int(m.predict(input_scaled)[0])
            prob = float(m.predict_proba(input_scaled)[0][1] * 100)
            verdict = "Heart Disease Detected" if pred == 1 else "No Heart Disease Detected"
            if pred == 1:
                detected_count += 1
            votes[name] = {
                "prediction": verdict,
                "is_detected": bool(pred == 1),
                "probability": round(prob, 1)
            }
        except Exception:
            pass

    consensus_percent = round((detected_count / (total_models or 1)) * 100, 1)

    if detected_count == total_models:
        consensus_status = "Unanimous Consensus (High Risk)"
    elif detected_count == 0:
        consensus_status = "Unanimous Consensus (Clear / Normal)"
    elif detected_count >= 2:
        consensus_status = "Majority Agreement (Elevated Risk)"
    else:
        consensus_status = "Minority Indication (Observation Advised)"

    return {
        "models": votes,
        "detected_count": detected_count,
        "total_models": total_models,
        "consensus_percent": consensus_percent,
        "consensus_status": consensus_status
    }


# --------------------------------------------------------------------------
# SWAP 1 of 4: Real Machine Learning Inference Engine
# --------------------------------------------------------------------------
def run_model(v):
    """
    Executes trained preprocessing and KNN inference.
    Returns (prediction, probability, outcome_details).
    """
    c = map_frontend_to_clinical(v)

    # Encode categorical features
    sex_enc = encoders["sex"].transform([c["sex"]])[0]
    cp_enc = encoders["chest_pain_type"].transform([c["chest_pain_type"]])[0]
    fbs_enc = encoders["fasting_blood_sugar"].transform([c["fasting_blood_sugar"]])[0]
    ecg_enc = encoders["rest_ecg"].transform([c["rest_ecg"]])[0]
    exang_enc = encoders["exercise_induced_angina"].transform([c["exercise_induced_angina"]])[0]
    slope_enc = encoders["slope"].transform([c["slope"]])[0]
    vessels_enc = encoders["vessels_colored_by_flourosopy"].transform([c["vessels_colored_by_flourosopy"]])[0]
    thal_enc = encoders["thalassemia"].transform([c["thalassemia"]])[0]

    input_df = pd.DataFrame([{
        "age": c["age"],
        "sex": sex_enc,
        "chest_pain_type": cp_enc,
        "resting_blood_pressure": c["resting_blood_pressure"],
        "cholestoral": c["cholestoral"],
        "fasting_blood_sugar": fbs_enc,
        "rest_ecg": ecg_enc,
        "Max_heart_rate": c["Max_heart_rate"],
        "exercise_induced_angina": exang_enc,
        "oldpeak": c["oldpeak"],
        "slope": slope_enc,
        "vessels_colored_by_flourosopy": vessels_enc,
        "thalassemia": thal_enc
    }])

    input_scaled = scaler.transform(input_df)

    pred = int(model.predict(input_scaled)[0])
    prob = round(float(model.predict_proba(input_scaled)[0][1] * 100), 1)
    risk_str = risk_level(prob)

    ensemble = evaluate_ensemble(input_scaled)
    flags, recs = evaluate_clinical_insights(c, prob, risk_str)

    # Calculate fluoroscopy count for heart SVG
    v_map = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4}
    v_count = v_map.get(c["vessels_colored_by_flourosopy"], 0)

    outcome = {
        "prediction": pred,
        "probability": prob,
        "risk": risk_str,
        "patient": c,
        "v_count": v_count,
        "ensemble": ensemble,
        "risk_factors": flags,
        "recommendations": recs
    }

    return pred, prob, outcome


# --------------------------------------------------------------------------
# SWAP 2, 3 and 4 of 4: Real MySQL Storage with Fallback
# --------------------------------------------------------------------------
def save_prediction(values, prediction, probability, outcome=None):
    """Inserts patient and prediction into MySQL, returning the record ID."""
    c = map_frontend_to_clinical(values)
    risk_str = risk_level(probability)

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO patients (
                age, sex, chest_pain_type, resting_blood_pressure,
                cholestoral, fasting_blood_sugar, rest_ecg, max_heart_rate,
                exercise_induced_angina, oldpeak, slope,
                vessels_colored_by_flourosopy, thalassemia
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            c["age"], c["sex"], c["chest_pain_type"], c["resting_blood_pressure"],
            c["cholestoral"], c["fasting_blood_sugar"], c["rest_ecg"], c["Max_heart_rate"],
            c["exercise_induced_angina"], c["oldpeak"], c["slope"],
            c["vessels_colored_by_flourosopy"], c["thalassemia"]
        ))
        patient_id = cur.lastrowid

        pred_result_text = "Heart Disease Detected" if prediction == 1 else "No Heart Disease Detected"
        cur.execute("""
            INSERT INTO predictions (
                patient_id, prediction_result, probability, risk_level
            ) VALUES (%s, %s, %s, %s)
        """, (
            patient_id, pred_result_text, probability, f"{risk_str} Risk"
        ))
        conn.commit()
        cur.close()
        conn.close()
        return patient_id

    except Exception as err:
        print("MySQL Insert fallback to memory:", err)
        record_id = len(_MEM_RECORDS) + 1
        _MEM_RECORDS.append({
            "id": record_id,
            "created_at": datetime.now(),
            "inputs": values,
            "clinical": c,
            "prediction": prediction,
            "probability": probability,
            "risk": risk_str,
            "outcome": outcome
        })
        return record_id


def get_prediction(record_id):
    """Retrieves one record by patient_id from MySQL or memory."""
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT p.*, pr.prediction_result, pr.probability, pr.risk_level, pr.predicted_at
            FROM patients p
            JOIN predictions pr ON p.patient_id = pr.patient_id
            WHERE p.patient_id = %s
        """, (record_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            pred_int = 1 if "Heart Disease Detected" in str(row["prediction_result"]) else 0
            prob_float = float(row["probability"])
            risk_clean = str(row["risk_level"]).replace(" Risk", "")

            # Reconstruct inputs dictionary for frontend templates
            frontend_inputs = {
                "age": row["age"],
                "sex": row["sex"],
                "chest_pain_type": row["chest_pain_type"],
                "resting_bp": row["resting_blood_pressure"],
                "cholesterol": row["cholestoral"],
                "fasting_blood_sugar": row["fasting_blood_sugar"],
                "rest_ecg": row["rest_ecg"],
                "max_heart_rate": row["max_heart_rate"],
                "exercise_angina": row["exercise_induced_angina"],
                "oldpeak": row["oldpeak"],
                "slope": row["slope"],
                "vessels": row["vessels_colored_by_flourosopy"],
                "thalassemia": row["thalassemia"]
            }

            # Evaluate XAI and ensemble for full telemetry
            _, _, outcome = run_model(frontend_inputs)

            return {
                "id": row["patient_id"],
                "created_at": row["predicted_at"] or datetime.now(),
                "inputs": frontend_inputs,
                "clinical": map_frontend_to_clinical(frontend_inputs),
                "prediction": pred_int,
                "probability": prob_float,
                "risk": risk_clean,
                "outcome": outcome
            }

    except Exception as err:
        print("MySQL Get note:", err)

    # Check memory fallback
    for r in _MEM_RECORDS:
        if r["id"] == record_id:
            return r
    return None


def list_predictions():
    """Retrieves all predictions from MySQL (newest first) or memory fallback."""
    records = []
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT p.*, pr.prediction_result, pr.probability, pr.risk_level, pr.predicted_at
            FROM patients p
            JOIN predictions pr ON p.patient_id = pr.patient_id
            ORDER BY pr.predicted_at DESC
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        for row in rows:
            pred_int = 1 if "Heart Disease Detected" in str(row["prediction_result"]) else 0
            prob_float = float(row["probability"])
            risk_clean = str(row["risk_level"]).replace(" Risk", "")
            records.append({
                "id": row["patient_id"],
                "created_at": row["predicted_at"] or datetime.now(),
                "inputs": {
                    "age": row["age"],
                    "sex": row["sex"],
                    "chest_pain_type": row["chest_pain_type"],
                    "resting_bp": row["resting_blood_pressure"],
                    "cholesterol": row["cholestoral"],
                    "fasting_blood_sugar": row["fasting_blood_sugar"],
                    "rest_ecg": row["rest_ecg"],
                    "max_heart_rate": row["max_heart_rate"],
                    "exercise_angina": row["exercise_induced_angina"],
                    "oldpeak": row["oldpeak"],
                    "slope": row["slope"],
                    "vessels": row["vessels_colored_by_flourosopy"],
                    "thalassemia": row["thalassemia"]
                },
                "prediction": pred_int,
                "probability": prob_float,
                "risk": risk_clean
            })
        if records:
            return records
    except Exception as err:
        print("MySQL List note:", err)

    return sorted(_MEM_RECORDS, key=lambda r: r["created_at"], reverse=True)


# --------------------------------------------------------------------------
# Template Helpers & Context Processors
# --------------------------------------------------------------------------
@app.template_filter("fmt_dt")
def fmt_dt(value):
    if isinstance(value, str):
        return value
    return value.strftime("%d %b %Y, %H:%M")


@app.context_processor
def inject_globals():
    return {
        "low_max": LOW_MAX,
        "high_min": HIGH_MIN,
        "current_year": datetime.now().year
    }


# --------------------------------------------------------------------------
# Application Routes
# --------------------------------------------------------------------------
@app.route("/")
def home():
    return redirect(url_for("predict"))


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        values, errors = validate(request.form)
        if not errors:
            prediction, probability, outcome = run_model(values)
            record_id = save_prediction(values, prediction, probability, outcome)
            return redirect(url_for("result", record_id=record_id))
        return render_template(
            "predict.html",
            groups=GROUPS,
            form=request.form,
            errors=errors
        ), 422

    return render_template("predict.html", groups=GROUPS, form={}, errors={})


@app.route("/result/<int:record_id>")
def result(record_id):
    record = get_prediction(record_id)
    if record is None:
        abort(404)
    return render_template(
        "result.html",
        rec=record,
        outcome=record.get("outcome", {}),
        rows=display_rows(record["inputs"])
    )


@app.route("/history")
def history():
    records = list_predictions()
    total = len(records)
    stats = {
        "total": total,
        "average": round(sum(r["probability"] for r in records) / total, 1) if total else 0,
        "high": sum(1 for r in records if r["risk"] == "High"),
    }
    return render_template("history.html", records=records, stats=stats)


@app.route("/dashboard")
def dashboard():
    records = list_predictions()
    total = len(records)

    risk = {"Low": 0, "Moderate": 0, "High": 0}
    bins = [0] * 10
    by_sex = {"Male": [0, 0], "Female": [0, 0]}  # [disease, none]

    for r in records:
        r_tier = r.get("risk", "Low")
        if r_tier in risk:
            risk[r_tier] += 1
        b_idx = min(int(r["probability"] // 10), 9)
        bins[b_idx] += 1
        s = r["inputs"].get("sex", "Male")
        if s in by_sex:
            by_sex[s][0 if r["prediction"] == 1 else 1] += 1

    dash = {
        "total": total,
        "disease": sum(1 for r in records if r["prediction"] == 1),
        "average": round(sum(r["probability"] for r in records) / total, 1) if total else 0,
        "high": risk["High"],
        "risk": risk,
        "histogram": bins,
        "low_max": LOW_MAX,
        "high_min": HIGH_MIN,
    }
    sex_rows = [
        {"label": s, "disease": d, "none": n, "total": d + n}
        for s, (d, n) in by_sex.items()
    ]
    return render_template("dashboard.html", dash=dash, sex_rows=sex_rows, recent=records[:10])


# --------------------------------------------------------------------------
# Advanced Clinical Modules: Simulator, Benchmarks, Reports & CSV
# --------------------------------------------------------------------------
@app.route("/simulator")
def simulator():
    return render_template("simulator.html")


@app.route("/api/simulate", methods=["POST"])
def api_simulate():
    try:
        data = request.get_json(force=True)
        _, prob, outcome = run_model(data)
        return jsonify({
            "status": "success",
            "prediction": outcome["prediction"],
            "result": "Heart Disease Detected" if outcome["prediction"] == 1 else "No Heart Disease Detected",
            "probability": prob,
            "risk_tier": outcome["risk"],
            "v_count": outcome["v_count"]
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/analytics")
def analytics_studio():
    try:
        # 1. 13-Model Benchmarking Data
        if os.path.exists(BENCHMARK_PATH):
            df = pd.read_csv(BENCHMARK_PATH)
            df = df.sort_values(by="Accuracy", ascending=False)
            models_data = df.to_dict(orient="records")
        else:
            models_data = []
        models_json = json.dumps(models_data)

        # 2. Genuine KNN K-Value Experiment Data (K = 1, 3, 5, 7, 9, 11)
        if os.path.exists(KNN_K_COMP_PATH):
            k_df = pd.read_csv(KNN_K_COMP_PATH)
        else:
            k_df = pd.DataFrame([
                {"K": 1, "Accuracy": 0.8197, "Precision": 0.8667, "Recall": 0.7879, "F1-Score": 0.8254, "ROC-AUC": 0.8225, "Train_Accuracy": 1.0, "CV_F1": 0.8058, "CV_Accuracy": 0.7923},
                {"K": 3, "Accuracy": 0.8689, "Precision": 0.8788, "Recall": 0.8788, "F1-Score": 0.8788, "ROC-AUC": 0.8934, "Train_Accuracy": 0.8921, "CV_F1": 0.8310, "CV_Accuracy": 0.8174},
                {"K": 5, "Accuracy": 0.8852, "Precision": 0.8824, "Recall": 0.9091, "F1-Score": 0.8955, "ROC-AUC": 0.9037, "Train_Accuracy": 0.8797, "CV_F1": 0.8412, "CV_Accuracy": 0.8256},
                {"K": 7, "Accuracy": 0.8525, "Precision": 0.8529, "Recall": 0.8788, "F1-Score": 0.8657, "ROC-AUC": 0.9053, "Train_Accuracy": 0.8589, "CV_F1": 0.8351, "CV_Accuracy": 0.8174},
                {"K": 9, "Accuracy": 0.8033, "Precision": 0.8000, "Recall": 0.8485, "F1-Score": 0.8235, "ROC-AUC": 0.8869, "Train_Accuracy": 0.8589, "CV_F1": 0.8425, "CV_Accuracy": 0.8257},
                {"K": 11, "Accuracy": 0.8197, "Precision": 0.8056, "Recall": 0.8788, "F1-Score": 0.8406, "ROC-AUC": 0.8804, "Train_Accuracy": 0.8382, "CV_F1": 0.8550, "CV_Accuracy": 0.8381}
            ])

        k_data = k_df.to_dict(orient="records")
        k_json = json.dumps(k_data)
        # Winning model selection rule: Primary=Test F1-Score, Secondary=Test Accuracy
        best_k_row = max(k_data, key=lambda x: (x.get("F1-Score", 0), x.get("Accuracy", 0)))

        return render_template(
            "analytics.html",
            models_data=models_data,
            models_json=models_json,
            k_data=k_data,
            k_json=k_json,
            best_k=best_k_row
        )
    except Exception as e:
        return render_template(
            "analytics.html",
            models_data=[],
            models_json="[]",
            k_data=[],
            k_json="[]",
            best_k={"K": 5, "F1-Score": 0.8955, "Accuracy": 0.8852, "Precision": 0.8824, "Recall": 0.9091, "ROC-AUC": 0.9037},
            error=str(e)
        )


@app.route("/patient-report/<int:record_id>")
def patient_report(record_id):
    rec = get_prediction(record_id)
    if not rec:
        abort(404)
    # Format for report.html compatibility
    c = rec.get("clinical") or map_frontend_to_clinical(rec["inputs"])
    c["patient_id"] = record_id
    c["prediction_result"] = "Heart Disease Detected" if rec["prediction"] == 1 else "No Heart Disease Detected"
    c["probability"] = rec["probability"]
    c["risk_level"] = f"{rec['risk']} Risk"
    c["predicted_at"] = rec["created_at"]
    return render_template("report.html", patient=c)


@app.route("/export-history")
def export_history():
    records = list_predictions()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Record ID", "Date", "Age", "Sex", "Chest Pain Type",
        "Resting BP (mmHg)", "Cholesterol (mg/dL)", "Max Heart Rate (bpm)",
        "Prediction Result", "Risk Probability (%)", "Risk Level"
    ])
    for r in records:
        inp = r["inputs"]
        writer.writerow([
            r["id"],
            r["created_at"].strftime("%Y-%m-%d %H:%M:%S") if hasattr(r["created_at"], "strftime") else str(r["created_at"]),
            inp.get("age"), inp.get("sex"), inp.get("chest_pain_type"),
            inp.get("resting_bp"), inp.get("cholesterol"), inp.get("max_heart_rate"),
            "Heart Disease Detected" if r["prediction"] == 1 else "No Heart Disease Detected",
            r["probability"], r["risk"]
        ])
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=healthcare_predictive_analytics_history.csv"}
    )


# --------------------------------------------------------------------------
# Run Server
# --------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("HeartCare AI - Unified Clinical Decision Support Platform")
    print("Running Flask on http://127.0.0.1:5000 ...")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=True)
