# HeartCare AI - Healthcare Predictive Analytics Platform

An enterprise-grade Clinical Decision Support and Predictive Analytics Platform for cardiovascular disease risk stratification, built using Machine Learning, Flask, MySQL, and Chart.js.

---

## 🌟 Key Features

1. **Cardiac Machine Learning Prediction Engine**:
   - Evaluates patient clinical biomarkers in real time.
   - Utilizes an optimized **K-Nearest Neighbors (KNN)** model (**88.52% Accuracy**, **90.91% Recall**, **0.904 ROC-AUC**).
   - Classifies risk into **Low Risk (<30%)**, **Moderate Risk (30–60%)**, and **High Risk (>60%)**.

2. **Explainable AI (XAI) & Biomarker Flagging**:
   - Analyzes critical clinical thresholds (e.g., *Serum Cholesterol > 200 mg/dL*, *Resting BP > 130 mmHg*, *Exercise Angina*, *ST Depression*).
   - Generates personalized medical and lifestyle recommendations tailored to each patient's risk profile.

3. **Multi-Model Consensus & Ensemble Voting Engine**:
   - Cross-validates patient cases across **4 distinct machine learning paradigms**:
     - **KNN** (Instance/Distance-based)
     - **Random Forest** (Bagging Ensemble)
     - **AdaBoost** (Boosting Ensemble)
     - **Logistic Regression** (Linear Probabilistic)
   - Computes an algorithmic consensus agreement percentage and confidence score to eliminate single-model bias.

4. **Interactive "What-If" Health Simulator (`/simulator`)**:
   - Real-time clinical parameter sandbox with interactive sliders.
   - Allows doctors and patients to simulate lifestyle changes (e.g., lowering Blood Pressure from 155 to 120 mmHg or Cholesterol from 280 to 190 mg/dL).
   - Dynamically calculates the resulting **Risk Reduction Delta (-%)** and lifestyle goals in real-time (<10ms).

5. **Production REST API Microservice (`/api/predict`) & Live Console (`/api-docs`)**:
   - Standard JSON API endpoint ready for Hospital Electronic Health Record (EHR) and mobile application integrations.
   - Interactive Swagger-style documentation with a "Try-It-Live" test console.

6. **Population Health Analytics Dashboard (`/dashboard`)**:
   - **Prevalence Ratio**: Diagnostic breakdown of cardiac cases vs healthy controls.
   - **Risk Stratification**: Visual distribution across clinical risk tiers.
   - **Age Cohort Vulnerability**: Cardiac incidence grouped by age brackets (`<40`, `40–54`, `55–64`, `65+`).
   - **Gender-wise Profiling**: Comparative analysis between male and female cohorts.
   - **Biomarker Comparative Profiling**: Average cholesterol, blood pressure, and heart rate comparison between patient groups.

7. **Machine Learning Benchmark Studio (`/analytics`)**:
   - Side-by-side performance benchmarking of **13 Classification Algorithms** (KNN, LDA, Extra Trees, AdaBoost, Random Forest, Logistic Regression, Naive Bayes, MLP Neural Network, SVM, XGBoost, CatBoost, Decision Tree, Gradient Boosting).
   - Interactive **$K$-Hyperparameter Optimization Curve** ($K=1$ to $K=25$) proving why $K=5$ is mathematically optimal.
   - Interactive multi-metric bar charts, KNN radar metric profile, and leaderboard table.

8. **Official Clinical Diagnostic Report (Print / PDF Download)**:
   - Instant generation of a hospital-grade Cardiology Diagnostic Sheet (`/patient-report/<id>`).
   - Includes patient demographics, observed vitals, reference ranges, AI risk score, flagged biomarkers, and physician disclaimer.
   - Print-optimized stylesheet (`@media print`) for one-click PDF export via browser.

9. **Historical Audit Log & CSV Export**:
   - Complete historical tracking of patient diagnoses stored in MySQL.
   - Instant search and risk-tier filtering.
   - **One-click CSV Data Export** for clinical researchers and hospital audits.

---

## 🏗️ System Architecture

- **Backend Framework**: Python 3.x / Flask
- **Machine Learning**: Scikit-Learn, Pandas, NumPy, Joblib, XGBoost, CatBoost
- **Database**: MySQL (`healthcare_predictive_analytics`)
- **Frontend & Data Visualization**: HTML5, CSS3, JavaScript, Chart.js (CDN)
- **Model Encoders & Scalers**: `StandardScaler`, `LabelEncoder`

---

## 📊 Model Benchmark Summary

| Model | Accuracy | Recall | ROC-AUC | F1-Score | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **KNN (K-Nearest Neighbors)** | **88.52%** | **90.91%** | **0.904** | **89.55%** | **🏆 Production Active** |
| Linear Discriminant Analysis (LDA) | 83.61% | 90.91% | 0.889 | 85.71% | Benchmarked |
| Extra Trees Classifier | 81.97% | 84.85% | 0.878 | 83.58% | Benchmarked |
| AdaBoost Classifier | 81.97% | 84.85% | 0.887 | 83.58% | Benchmarked |
| Random Forest Classifier | 81.97% | 81.82% | 0.879 | 83.08% | Benchmarked |
| Logistic Regression | 80.33% | 84.85% | 0.879 | 82.35% | Benchmarked |
| Naive Bayes | 80.33% | 75.76% | 0.894 | 80.65% | Benchmarked |
| MLP Neural Network | 78.69% | 81.82% | 0.804 | 80.60% | Benchmarked |
| Support Vector Machine (SVM) | 78.69% | 81.82% | 0.870 | 80.60% | Benchmarked |
| XGBoost | 77.05% | 75.76% | 0.847 | 78.13% | Benchmarked |
| CatBoost | 73.77% | 78.79% | 0.856 | 76.47% | Benchmarked |
| Decision Tree | 73.77% | 75.76% | 0.736 | 75.76% | Benchmarked |
| Gradient Boosting | 73.77% | 75.76% | 0.828 | 75.76% | Benchmarked |

---

## 🚀 Installation & Running

### 1. Prerequisites
- Python 3.10+
- MySQL Server running on `localhost:3306`
- Database imported:
  ```bash
  mysql -u root -p < database/database.sql
  ```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the Web Platform
```bash
python app.py
```
Or double-click:
```bash
run.bat
```

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
HealthcarePredictiveAnalytics/
├── app.py                      # Core Flask web server & analytical routes
├── model_training.py           # Training pipeline for 12 classification models
├── run.bat                     # Windows batch launcher
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation
├── dataset/
│   └── HeartDiseaseTrain-Test.xlsx  # Cardiovascular training dataset
├── model/
│   ├── heart_model.pkl         # Production trained KNN model
│   ├── scaler.pkl              # Fitted StandardScaler
│   ├── encoders.pkl            # Fitted LabelEncoders
│   └── model_comparison.csv    # 12-Algorithm benchmark metrics
├── database/
│   └── database.sql            # MySQL schema for patients & predictions
├── screenshots/                # Model evaluation curves, confusion matrices & EDA plots
└── templates/
    ├── prediction.html         # Clinical parameter input interface
    ├── result.html             # Diagnosis finding, probability gauge & XAI
    ├── dashboard.html          # Population health analytics (Chart.js)
    ├── analytics.html          # ML benchmark comparison studio
    ├── report.html             # Printable cardiology diagnostic report (PDF)
    └── history.html            # Historical prediction records & CSV export
```
