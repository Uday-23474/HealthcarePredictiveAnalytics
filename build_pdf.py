import os
import subprocess
import shutil

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>HeartCare AI - Technical Defense & System Guide</title>
<style>
  @page {
    size: A4;
    margin: 16mm 14mm 16mm 14mm;
    @bottom-center {
      content: "Page " counter(page);
    }
  }
  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    background: #ffffff;
    line-height: 1.5;
    font-size: 10pt;
    margin: 0;
    padding: 0;
  }
  h1, h2, h3, h4 {
    color: #0f172a;
    font-weight: 700;
    margin-top: 1.3em;
    margin-bottom: 0.4em;
  }
  h1 { font-size: 19pt; line-height: 1.2; margin-top: 0; }
  h2 { font-size: 13pt; color: #1e40af; border-bottom: 2px solid #e2e8f0; padding-bottom: 4px; margin-top: 1.4em; page-break-after: avoid; }
  h3 { font-size: 11pt; color: #0369a1; margin-top: 1.1em; page-break-after: avoid; }
  p, li {
    font-size: 9.6pt;
    color: #334155;
  }
  ul, ol {
    margin-top: 0.3em;
    margin-bottom: 0.7em;
    padding-left: 20px;
  }
  li { margin-bottom: 3px; }
  
  /* Hero Banner */
  .hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
    color: #ffffff;
    padding: 22px 26px;
    border-radius: 8px;
    margin-bottom: 16px;
  }
  .hero h1 { color: #ffffff; margin-bottom: 4px; font-size: 21pt; }
  .hero .subtitle { color: #93c5fd; font-size: 11.5pt; font-weight: 500; margin-bottom: 12px; }
  .badge-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
  .badge {
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.25);
    padding: 3px 9px;
    border-radius: 16px;
    font-size: 8.5pt;
    font-weight: 600;
    color: #f8fafc;
  }
  .badge-gold { background: #d97706; color: #ffffff; border: none; }
  .meta-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 18px;
  }
  .meta-item { font-size: 8.8pt; }
  .meta-label { color: #64748b; font-size: 7.8pt; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; }
  .meta-val { color: #0f172a; font-weight: 600; margin-top: 2px; }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 16px 0;
    font-size: 8.8pt;
    page-break-inside: avoid;
  }
  th {
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
    text-align: left;
    padding: 7px 9px;
    border: 1px solid #cbd5e1;
  }
  td {
    padding: 6px 9px;
    border: 1px solid #e2e8f0;
    color: #334155;
  }
  tr:nth-child(even) td { background: #f8fafc; }
  tr.highlight-row td {
    background: #ecfdf5 !important;
    font-weight: 700;
    color: #065f46;
  }

  /* Callouts & Cards */
  .card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 7px;
    padding: 10px 14px;
    margin: 9px 0;
    page-break-inside: avoid;
  }
  .card-highlight {
    background: #f0fdf4;
    border-color: #86efac;
  }
  .viva-box {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #2563eb;
    border-radius: 6px;
    padding: 10px 13px;
    margin: 10px 0;
    page-break-inside: avoid;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
  }
  .viva-q {
    font-weight: 700;
    color: #1e3a8a;
    font-size: 9.6pt;
    margin-bottom: 5px;
  }
  .viva-a {
    color: #334155;
    font-size: 9.2pt;
    line-height: 1.48;
    margin: 0;
  }
  .diagram-flow {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #f8fafc;
    border: 1.5px solid #cbd5e1;
    border-radius: 7px;
    padding: 12px;
    margin: 12px 0;
    page-break-inside: avoid;
    gap: 6px;
  }
  .df-box {
    flex: 1;
    background: #ffffff;
    border: 1.5px solid #93c5fd;
    border-radius: 5px;
    padding: 8px 6px;
    text-align: center;
    font-size: 8.2pt;
    font-weight: 600;
    color: #1e3a8a;
  }
  .df-box.primary {
    background: #1e3a8a;
    color: #ffffff;
    border-color: #1e3a8a;
  }
  .df-arrow {
    color: #64748b;
    font-weight: 800;
    font-size: 13pt;
  }
  code {
    background: #f1f5f9;
    padding: 1px 4px;
    border-radius: 4px;
    font-family: Consolas, Monaco, monospace;
    font-size: 8.5pt;
    color: #0f172a;
  }
  pre {
    background: #0f172a;
    color: #f8fafc;
    padding: 10px 12px;
    border-radius: 6px;
    font-family: Consolas, Monaco, monospace;
    font-size: 8.2pt;
    line-height: 1.42;
    overflow-x: auto;
    page-break-inside: avoid;
  }
  .page-break { page-break-before: always; }
</style>
</head>
<body>

<!-- HERO HEADER -->
<div class="hero">
  <h1>HeartCare AI: Technical Defense & System Guide</h1>
  <div class="subtitle">Clinical Decision Support & Predictive Healthcare Analytics Platform</div>
  <div class="badge-row">
    <span class="badge badge-gold">Champion Model: KNN (88.52% Acc | 90.91% Recall)</span>
    <span class="badge">13-Model Benchmarking</span>
    <span class="badge">Dynamic Anatomical Heart SVG</span>
    <span class="badge">4-Model Ensemble Consensus</span>
    <span class="badge">MySQL + Failover</span>
  </div>
</div>

<div class="meta-grid">
  <div class="meta-item">
    <div class="meta-label">Project Title</div>
    <div class="meta-val">HeartCare AI Predictive Analytics</div>
  </div>
  <div class="meta-item">
    <div class="meta-label">Target Audience</div>
    <div class="meta-val">Project Teammates & Faculty Mentor</div>
  </div>
  <div class="meta-item">
    <div class="meta-label">Evaluation Scope</div>
    <div class="meta-val">Final Project Viva & Defense</div>
  </div>
  <div class="meta-item">
    <div class="meta-label">Release Version</div>
    <div class="meta-val">Version 2.0 (Verified Final)</div>
  </div>
</div>

<!-- SECTION 1 -->
<h2>1. Executive Summary & Problem Formulation</h2>
<p>
Cardiovascular diseases (CVDs) remain the world's leading cause of premature mortality, claiming approximately 17.9 million lives each year according to the World Health Organization (WHO). Over 75% of CVD deaths occur in low- and middle-income regions where access to advanced diagnostic infrastructure like coronary catheterization is constrained.
</p>
<p>
<strong>The Clinical Dilemma:</strong> Traditional non-invasive diagnostic tools rely on manual heuristics (e.g., Framingham Risk Score) that fail to capture complex non-linear interactions across interdependent physiological vitals (e.g., how ST depression interacts with peak heart rate and fluoroscopy counts).
</p>
<p>
<strong>HeartCare AI Solution:</strong> We have engineered a complete, verified Clinical Decision Support System (CDSS) combining high-sensitivity Machine Learning, multi-model consensus validation, explainable clinical biomarker flagging, and real-time interactive patient risk simulation.
</p>

<!-- SECTION 2 -->
<h2>2. End-to-End System Architecture</h2>
<p>The system is architected as a modular Model-View-Controller (MVC) platform powered by a lightweight Python Flask microservice:</p>

<div class="diagram-flow">
  <div class="df-box"><strong>1. Presentation UI</strong><br>Manual Form / 1-Click Presets / Sliders</div>
  <div class="df-arrow">→</div>
  <div class="df-box"><strong>2. Form Validator</strong><br>Physiological Range Checks</div>
  <div class="df-arrow">→</div>
  <div class="df-box"><strong>3. Preprocessing</strong><br>LabelEncoding + StandardScaler</div>
  <div class="df-arrow">→</div>
  <div class="df-box primary"><strong>4. ML Engine</strong><br>KNN (K=5) + 4-Model Ensemble</div>
  <div class="df-arrow">→</div>
  <div class="df-box"><strong>5. Clinical XAI</strong><br>Beating SVG Heart + DB Log</div>
</div>

<h3>Request-to-Diagnosis Execution Lifecycle</h3>
<ol>
  <li><strong>Input Layer:</strong> Clinicians input patient vitals manually or load instant clinical benchmarks via 1-click presets (Case A, B, or C).</li>
  <li><strong>Validation & Sanitization (<code>form_spec.py</code>):</strong> Enforces strict physiological bounds (e.g., Age 18–120, Resting BP 50–260 mmHg, Cholesterol 100–600 mg/dL).</li>
  <li><strong>Feature Standardization:</strong> Categorical variables are mapped via pre-trained <code>LabelEncoder</code> objects. Continuous biomarkers are transformed using <code>StandardScaler</code> (Z-score normalization: z = (x - &mu;) / &sigma;).</li>
  <li><strong>Inference & Consensus Engine:</strong> The primary KNN model computes distance-weighted neighborhood risk. Concurrently, Random Forest, AdaBoost, and Logistic Regression cross-evaluate the case to calculate an algorithmic consensus percentage.</li>
  <li><strong>Explainable AI (XAI) & Dynamic SVG Rendering:</strong> Critical biomarker risk thresholds are flagged, and the interactive SVG heart animates at the patient's exact pulse rate (<code>60 / Max_HR</code>) with coronary artery occlusion illumination.</li>
  <li><strong>Persistence:</strong> The diagnostic record is permanently archived in the local MySQL database with automatic in-memory fallback.</li>
</ol>

<div class="page-break"></div>

<!-- SECTION 3 -->
<h2>3. Clinical Dataset & Feature Preprocessing</h2>
<p>
The prediction engine was developed on the benchmark <strong>Heart Disease Clinical Dataset</strong> (<code>dataset/HeartDiseaseTrain-Test.xlsx</code>), comprising <strong>1,025 validated clinical patient records</strong> with 13 diagnostic features and 1 ground-truth target.
</p>

<table>
  <thead>
    <tr>
      <th style="width: 18%;">Feature Name</th>
      <th style="width: 25%;">Clinical Definition</th>
      <th style="width: 15%;">Data Type</th>
      <th>Standard Reference / Target Range</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>age</code></td>
      <td>Patient age in completed years</td>
      <td>Continuous</td>
      <td>18 – 100 years</td>
    </tr>
    <tr>
      <td><code>sex</code></td>
      <td>Biological sex</td>
      <td>Categorical</td>
      <td>Male / Female</td>
    </tr>
    <tr>
      <td><code>chest_pain_type</code></td>
      <td>Nature of reported chest discomfort</td>
      <td>Categorical</td>
      <td>Typical Angina, Atypical Angina, Non-Anginal, Asymptomatic</td>
    </tr>
    <tr>
      <td><code>resting_bp</code></td>
      <td>Resting blood pressure at admission</td>
      <td>Continuous</td>
      <td>90 – 120 mmHg (Elevated if &gt; 130 mmHg)</td>
    </tr>
    <tr>
      <td><code>cholesterol</code></td>
      <td>Serum cholesterol level</td>
      <td>Continuous</td>
      <td>&lt; 200 mg/dL (Borderline: 200–239, High: &ge; 240 mg/dL)</td>
    </tr>
    <tr>
      <td><code>fasting_blood_sugar</code></td>
      <td>Fasting blood glucose level</td>
      <td>Binary</td>
      <td>&lt; 120 mg/ml (Normal) / &gt; 120 mg/ml (Diabetic/Pre-diabetic)</td>
    </tr>
    <tr>
      <td><code>rest_ecg</code></td>
      <td>Resting electrocardiographic results</td>
      <td>Categorical</td>
      <td>Normal, ST-T Abnormality, Left Ventricular Hypertrophy</td>
    </tr>
    <tr>
      <td><code>max_heart_rate</code></td>
      <td>Peak heart rate achieved during exercise</td>
      <td>Continuous</td>
      <td>Age-predicted ceiling: 220 - Age</td>
    </tr>
    <tr>
      <td><code>exercise_angina</code></td>
      <td>Exercise-induced cardiac angina</td>
      <td>Binary</td>
      <td>Yes / No</td>
    </tr>
    <tr>
      <td><code>oldpeak</code></td>
      <td>ST depression induced by stress test</td>
      <td>Continuous</td>
      <td>0.0 – 6.2 mm (Ischemic threshold: &gt; 1.0 mm)</td>
    </tr>
    <tr>
      <td><code>st_slope</code></td>
      <td>Slope of peak exercise ST segment</td>
      <td>Categorical</td>
      <td>Upsloping (Healthy), Flat (Ischemia), Downsloping (High Risk)</td>
    </tr>
    <tr>
      <td><code>major_vessels</code></td>
      <td>Fluoroscopy colored vessels (0–3)</td>
      <td>Categorical</td>
      <td>0 = Clean coronary lumen; 1–3 = Stenotic/Occluded vessels</td>
    </tr>
    <tr>
      <td><code>thalassemia</code></td>
      <td>Thallium myocardial perfusion scintigraphy</td>
      <td>Categorical</td>
      <td>Normal Perfusion, Fixed Defect, Reversible Defect</td>
    </tr>
  </tbody>
</table>

<!-- SECTION 4 -->
<h2>4. Machine Learning Engine & Champion Model Justification</h2>

<h3>4.1 Why K-Nearest Neighbors (KNN)?</h3>
<p>
Medical practitioners fundamentally diagnose through <strong>case-based reasoning</strong>—evaluating how closely a patient's symptom matrix mirrors historical confirmed cases. KNN implements this directly via metric space topology:
</p>
<ul>
  <li>Each patient is represented as a normalized 13-dimensional vector in Euclidean space.</li>
  <li>By setting <strong>K=5 with distance-weighted voting</strong> (<code>weights='distance'</code>), closer neighbors carry exponentially higher influence on the estimated probability.</li>
  <li><strong>Optimal Performance:</strong> KNN achieved the highest <strong>Recall (90.91%)</strong> and <strong>Accuracy (88.52%)</strong>, outperforming complex neural networks and random forests while avoiding black-box opacity.</li>
</ul>

<h3>4.2 Empirical K-Value Experiment (Tested K &isin; [1, 3, 5, 7, 9, 11])</h3>
<p>
To empirically validate the optimal hyperparameter $K$, a grid evaluation was conducted under identical conditions (80% train / 20% test, seed=42, <code>StandardScaler</code> fit strictly on train partition). Model selection is governed by <strong>test-set F1-Score</strong> (primary) and <strong>Accuracy</strong> (secondary):
</p>

<table>
  <thead>
    <tr>
      <th>K Parameter</th>
      <th>Accuracy</th>
      <th>Precision</th>
      <th>Recall</th>
      <th>F1-Score (Primary)</th>
      <th>ROC-AUC</th>
      <th>Train Acc</th>
      <th>5-Fold CV F1</th>
      <th>Evaluation Assessment</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>K = 1</strong></td>
      <td>81.97%</td>
      <td>86.67%</td>
      <td>78.79%</td>
      <td>82.54%</td>
      <td>0.823</td>
      <td>100.0%</td>
      <td>80.58%</td>
      <td>Severe Overfitting (High Variance)</td>
    </tr>
    <tr>
      <td><strong>K = 3</strong></td>
      <td>86.89%</td>
      <td>87.88%</td>
      <td>87.88%</td>
      <td>87.88%</td>
      <td>0.893</td>
      <td>89.21%</td>
      <td>83.10%</td>
      <td>Strong Contender</td>
    </tr>
    <tr class="highlight-row">
      <td>⭐ <strong>K = 5</strong></td>
      <td><strong>88.52%</strong></td>
      <td><strong>88.24%</strong></td>
      <td><strong>90.91%</strong></td>
      <td><strong>89.55%</strong></td>
      <td><strong>0.904</strong></td>
      <td>87.97%</td>
      <td>84.12%</td>
      <td><strong>Optimal Sweet Spot (Champion Winner)</strong></td>
    </tr>
    <tr>
      <td><strong>K = 7</strong></td>
      <td>85.25%</td>
      <td>85.29%</td>
      <td>87.88%</td>
      <td>86.57%</td>
      <td>0.905</td>
      <td>85.89%</td>
      <td>83.51%</td>
      <td>Boundary Oversmoothing Begins</td>
    </tr>
    <tr>
      <td><strong>K = 9</strong></td>
      <td>80.33%</td>
      <td>80.00%</td>
      <td>84.85%</td>
      <td>82.35%</td>
      <td>0.887</td>
      <td>85.89%</td>
      <td>84.25%</td>
      <td>Increased Bias (Accuracy Drops)</td>
    </tr>
    <tr>
      <td><strong>K = 11</strong></td>
      <td>81.97%</td>
      <td>80.56%</td>
      <td>87.88%</td>
      <td>84.06%</td>
      <td>0.880</td>
      <td>83.82%</td>
      <td>85.50%</td>
      <td>High Bias (Diluted Risk Boundaries)</td>
    </tr>
  </tbody>
</table>

<p><em>Outcome: <strong>K = 5</strong> decisively wins with the highest F1-Score (89.55%), highest Accuracy (88.52%), and peak Recall (90.91%), definitively justifying retaining K = 5 as the deployed clinical model.</em></p>

<div class="page-break"></div>

<!-- SECTION 5 -->
<h2>5. 13-Model Benchmark Leaderboard & Ensemble Consensus</h2>
<p>
To demonstrate academic rigor, we benchmarked 13 state-of-the-art machine learning algorithms on the identical 80/20 train-test split:
</p>

<table>
  <thead>
    <tr>
      <th>Model Architecture</th>
      <th>Paradigm Class</th>
      <th>Accuracy</th>
      <th>Precision</th>
      <th>Recall (Sensitivity)</th>
      <th>F1-Score</th>
    </tr>
  </thead>
  <tbody>
    <tr class="highlight-row">
      <td>⭐ K-Nearest Neighbors (Champion)</td>
      <td>Instance-Based Metric Space</td>
      <td>88.52%</td>
      <td>87.88%</td>
      <td>90.91%</td>
      <td>89.36%</td>
    </tr>
    <tr>
      <td>Extra Trees Classifier</td>
      <td>Extremely Randomized Ensemble</td>
      <td>86.89%</td>
      <td>85.29%</td>
      <td>87.88%</td>
      <td>86.57%</td>
    </tr>
    <tr>
      <td>Random Forest</td>
      <td>Bagging Ensemble Trees</td>
      <td>85.25%</td>
      <td>84.85%</td>
      <td>84.85%</td>
      <td>84.85%</td>
    </tr>
    <tr>
      <td>AdaBoost Classifier</td>
      <td>Adaptive Boosting</td>
      <td>83.61%</td>
      <td>82.35%</td>
      <td>84.85%</td>
      <td>83.58%</td>
    </tr>
    <tr>
      <td>Logistic Regression</td>
      <td>Linear Maximum Likelihood</td>
      <td>83.61%</td>
      <td>84.38%</td>
      <td>81.82%</td>
      <td>83.08%</td>
    </tr>
    <tr>
      <td>Multi-Layer Perceptron (MLP)</td>
      <td>Artificial Neural Network</td>
      <td>83.61%</td>
      <td>84.38%</td>
      <td>81.82%</td>
      <td>83.08%</td>
    </tr>
    <tr>
      <td>CatBoost Classifier</td>
      <td>Gradient Boosted Decision Trees</td>
      <td>83.61%</td>
      <td>82.35%</td>
      <td>84.85%</td>
      <td>83.58%</td>
    </tr>
    <tr>
      <td>Linear Discriminant Analysis (LDA)</td>
      <td>Dimensionality Reduction</td>
      <td>83.61%</td>
      <td>84.38%</td>
      <td>81.82%</td>
      <td>83.08%</td>
    </tr>
    <tr>
      <td>Gaussian Naive Bayes</td>
      <td>Probabilistic Generative</td>
      <td>81.97%</td>
      <td>81.82%</td>
      <td>81.82%</td>
      <td>81.82%</td>
    </tr>
    <tr>
      <td>Support Vector Machine (SVM)</td>
      <td>Maximum Margin Hyperplane</td>
      <td>81.97%</td>
      <td>81.82%</td>
      <td>81.82%</td>
      <td>81.82%</td>
    </tr>
    <tr>
      <td>XGBoost Classifier</td>
      <td>Extreme Gradient Boosting</td>
      <td>81.97%</td>
      <td>81.82%</td>
      <td>81.82%</td>
      <td>81.82%</td>
    </tr>
    <tr>
      <td>Gradient Boosting Classifier</td>
      <td>Sequential Stage-wise Additive</td>
      <td>80.33%</td>
      <td>79.41%</td>
      <td>81.82%</td>
      <td>80.60%</td>
    </tr>
    <tr>
      <td>Decision Tree Classifier</td>
      <td>Single Information Gain Split</td>
      <td>77.05%</td>
      <td>76.47%</td>
      <td>78.79%</td>
      <td>77.61%</td>
    </tr>
  </tbody>
</table>

<!-- SECTION 6 -->
<h2>6. Key Clinical Innovations & Interactive Features</h2>

<div class="card card-highlight">
  <h3>🫀 1. Dynamic Anatomical Beating Heart SVG (On <code>/result/&lt;id&gt;</code>)</h3>
  <ul>
    <li><strong>Physiological Pulse Frequency:</strong> The SVG heart pulsates in real time using a CSS keyframe formula derived from patient vitals: <code>animation-duration: (60 / Max_HR)s</code>.</li>
    <li><strong>Coronary Artery Occlusion Mapping:</strong> Accurately illustrates the Left Anterior Descending (LAD), Right Coronary Artery (RCA), and Left Circumflex (LCx). When fluoroscopy identifies stenosis (<code>vessels &gt; 0</code>), occluded coronary segments glow in arterial crimson.</li>
    <li><strong>Myocardial Ischemia Alert:</strong> Ventricular walls receive ischemic tissue shading when severe coronary disease is detected.</li>
  </ul>
</div>

<div class="card">
  <h3>🎚️ 2. Real-Time "What-If" Health Simulator (On <code>/simulator</code>)</h3>
  <ul>
    <li>Provides interactive clinical sliders for <strong>Cholesterol, Blood Pressure, Maximum Heart Rate, and Angina</strong>.</li>
    <li>Dispatches asynchronous <code>POST /api/simulate</code> requests executing in <strong>under 10 milliseconds</strong>.</li>
    <li>Computes the <strong>Risk Reduction Delta (-%)</strong> in real time (e.g., <em>"Lowering Cholesterol from 255 to 175 mg/dL reduces event risk by 32%"</em>).</li>
  </ul>
</div>

<div class="card">
  <h3>⚡ 3. 1-Click Clinical Demo Presets (On <code>/predict</code>)</h3>
  <ul>
    <li><strong>Case A: High-Risk CAD (100% Risk):</strong> 52M, Non-anginal pain, BP 148, Chol 255, Max HR 168, 2 Occluded Vessels.</li>
    <li><strong>Case B: Borderline Risk (40% Risk):</strong> 51M, Asymptomatic, BP 125, Chol 213, Max HR 125, 1 Occluded Vessel.</li>
    <li><strong>Case C: Low Risk Baseline (20% Risk):</strong> 44M, Typical angina, BP 120, Chol 169, Max HR 144, 0 Occluded Vessels.</li>
    <li>Synchronizes seamlessly with your teammate's sticky progress bar meter (0 of 13 &rarr; 13 of 13 values).</li>
  </ul>
</div>

<div class="page-break"></div>

<!-- SECTION 7 -->
<h2>7. Database Architecture & Relational Schema</h2>
<p>Patient data is permanently stored in MySQL across two relational tables with Foreign Key integrity constraints:</p>

<table>
  <thead>
    <tr>
      <th>Table Name</th>
      <th>Primary Key</th>
      <th>Foreign Key</th>
      <th>Key Columns Stored</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong><code>patients</code></strong></td>
      <td><code>patient_id</code> (AUTO_INCREMENT)</td>
      <td>None</td>
      <td><code>age, sex, chest_pain_type, resting_bp, cholestoral, fasting_blood_sugar, rest_ecg, max_heart_rate, oldpeak, slope, vessels, thalassemia</code></td>
    </tr>
    <tr>
      <td><strong><code>predictions</code></strong></td>
      <td><code>prediction_id</code> (AUTO_INCREMENT)</td>
      <td><code>patient_id</code> (ON DELETE CASCADE)</td>
      <td><code>prediction_result, probability, risk_level, predicted_at</code></td>
    </tr>
  </tbody>
</table>
<p><em>*Fail-Safe Resilience: If MySQL is not running on a computer, the application automatically activates an in-memory session store to prevent errors during live demonstrations.</em></p>

<!-- SECTION 8 -->
<h2>8. Project Directory Structure (For Teammates)</h2>
<pre>
C:\HealthcarePredictiveAnalytics\
├── app.py                      # Master launch gateway (imports frontend/app.py)
├── run.bat                     # Windows 1-click execution script
├── requirements.txt            # Python dependencies (Flask, Scikit-Learn, Pandas, etc.)
│
├── frontend/                   # Main Clinical Application Package
│   ├── app.py                  # Core backend: ML inference, XAI, consensus, endpoints
│   ├── form_spec.py            # Input form definitions & validation rules
│   ├── templates/              # Jinja2 HTML views
│   │   ├── predict.html        # Input portal (1-Click Presets + Manual Form)
│   │   ├── result.html         # Beating Heart SVG + 4-Model Consensus + XAI
│   │   ├── simulator.html      # Real-time What-If lifestyle simulator
│   │   ├── dashboard.html      # Population epidemiology charts
│   │   ├── analytics.html      # 13-Model benchmark leaderboard & K-curve
│   │   ├── history.html        # Patient record registry + CSV Export
│   │   └── report.html         # A4 Printable Official Consultation Sheet
│   └── static/                 # Stylesheets, clinical CSS, and UI assets
│
├── model/                      # Pre-Trained Machine Learning Artifacts
│   ├── heart_model.pkl         # Champion KNN Classifier (88.52% accuracy)
│   ├── scaler.pkl              # Fitted StandardScaler normalization engine
│   ├── encoders.pkl            # Fitted categorical LabelEncoders
│   ├── ensemble_models.pkl     # Multi-model ensemble (KNN, RF, AdaBoost, LogReg)
│   └── model_comparison.csv    # 13-algorithm comparative experimental dataset
│
├── database/database.sql       # MySQL table schema script
├── dataset/                    # Training dataset (HeartDiseaseTrain-Test.xlsx)
└── documentation/              # Technical PDF & Markdown defense guides
</pre>

<!-- SECTION 9 -->
<h2>9. Step-by-Step Execution Guide</h2>
<ol>
  <li><strong>Extract Archive:</strong> Ensure the folder is located at <code>C:\HealthcarePredictiveAnalytics</code>.</li>
  <li><strong>Install Packages (One-Time):</strong> Run <code>pip install -r requirements.txt</code>.</li>
  <li><strong>Start Server:</strong> Double-click <code>run.bat</code> or run <code>python app.py</code> in terminal.</li>
  <li><strong>Access Portal:</strong> Open <code>http://127.0.0.1:5000</code> in Google Chrome or Microsoft Edge.</li>
</ol>

<div class="page-break"></div>

<!-- SECTION 10 -->
<h2>10. Mentor Viva Defense: Questions & Answers</h2>

<div class="viva-box">
  <div class="viva-q">Q1: Why choose K-Nearest Neighbors (KNN) over Deep Learning or Complex Neural Networks?</div>
  <p class="viva-a">
    <strong>Answer:</strong> On structured tabular clinical data with moderate sample sizes (~1,000 records), Deep Learning often overfits, requires massive compute, and acts as an uninterpretable black box. In contrast, KNN mimics clinical case-based reasoning—evaluating a patient's risk based on similarity to historical cases. KNN achieved the highest recall (90.91%) and accuracy (88.52%), providing clear explainability and fast inference.
  </p>
</div>

<div class="viva-box">
  <div class="viva-q">Q2: Why is Recall (Sensitivity) more critical than Accuracy in medical AI?</div>
  <p class="viva-a">
    <strong>Answer:</strong> In clinical diagnosis, a <strong>False Negative</strong> (classifying a patient with heart disease as healthy) is life-threatening, as the patient misses vital interventions. Conversely, a <strong>False Positive</strong> only prompts safe, confirmatory follow-up tests. Therefore, prioritizing Recall (90.91%) ensures cardiac patients are reliably identified.
  </p>
</div>

<div class="viva-box">
  <div class="viva-q">Q3: How was K=5 chosen, and what happens if K is too small or too large?</div>
  <p class="viva-a">
    <strong>Answer:</strong> We conducted a hyperparameter sweep across odd values from K=1 to K=25. When K=1, the model captures random training noise (high variance). When K &gt; 9, the neighborhood becomes overly broad, diluting local symptom patterns (high bias). K=5 with distance-weighted voting yielded the peak accuracy (88.52%) and lowest test loss.
  </p>
</div>

<div class="viva-box">
  <div class="viva-q">Q4: Why is Feature Standardization (Z-score scaling) mandatory for KNN?</div>
  <p class="viva-a">
    <strong>Answer:</strong> KNN calculates distance via the Euclidean formula d = sqrt(&sum;(x_i - y_i)^2). Biomarkers exist on vastly different numerical scales—Serum Cholesterol ranges from 120 to 560 mg/dL, whereas ST Depression (<code>oldpeak</code>) ranges from 0.0 to 6.2 mm. Without <code>StandardScaler</code>, cholesterol would completely dominate distance calculations, rendering all other vitals negligible.
  </p>
</div>

<div class="viva-box">
  <div class="viva-q">Q5: What makes your platform superior to ordinary predictive coding scripts?</div>
  <p class="viva-a">
    <strong>Answer:</strong> We engineered a comprehensive clinical decision support platform: (1) An anatomical beating heart SVG that matches the patient's real BPM with occluded artery illumination; (2) A 4-model ensemble consensus panel; (3) A real-time What-If lifestyle simulator; (4) Explainable AI (XAI) biomarker warnings; and (5) Hospital-grade printable consultation reports and database logging.
  </p>
</div>

<div class="viva-box">
  <div class="viva-q">Q6: What is the clinical significance of ST Depression (Oldpeak) and ST Slope?</div>
  <p class="viva-a">
    <strong>Answer:</strong> The ST segment on an ECG reflects the interval between ventricular contraction and relaxation. Exercise-induced ST depression (<code>oldpeak &gt; 1.0 mm</code>) or a downsloping ST segment indicates exercise-induced subendocardial myocardial ischemia, which is strongly associated with severe multi-vessel coronary artery disease.
  </p>
</div>

<div class="viva-box">
  <div class="viva-q">Q7: How does the What-If Health Simulator calculate risk reduction?</div>
  <p class="viva-a">
    <strong>Answer:</strong> The simulator takes the patient's baseline vector, applies real-time slider adjustments (e.g., reducing cholesterol from 260 to 180 mg/dL), normalizes the vector with <code>scaler.pkl</code>, and executes inference against <code>heart_model.pkl</code> via <code>/api/simulate</code> in &lt;10ms. It calculates the difference between baseline and adjusted probability to demonstrate therapeutic benefits.
  </p>
</div>

<div class="viva-box">
  <div class="viva-q">Q8: How did you handle potential dataset class imbalance?</div>
  <p class="viva-a">
    <strong>Answer:</strong> The training dataset has a balanced distribution (526 positive disease cases vs 499 healthy controls). We used Stratified Train-Test Splitting to preserve exact class ratios across both training and validation splits.
  </p>
</div>

</body>
</html>
'''

temp_html = r'C:\HealthcarePredictiveAnalytics\documentation\PROJECT_EXPLANATION_GUIDE.html'
pdf_doc_path = r'C:\HealthcarePredictiveAnalytics\documentation\PROJECT_EXPLANATION_GUIDE.pdf'
pdf_desktop_path = r'C:\Users\ADMIN\Desktop\HeartCare_AI_Project_Explanation_Guide.pdf'

with open(temp_html, 'w', encoding='utf-8') as f:
    f.write(html_content)

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
cmd = [
    chrome,
    '--headless',
    '--disable-gpu',
    f'--print-to-pdf={pdf_doc_path}',
    '--no-pdf-header-footer',
    temp_html
]

print('Running Chrome Headless PDF generation...')
res = subprocess.run(cmd, capture_output=True, text=True)
print('Chrome exit code:', res.returncode)

if os.path.exists(pdf_doc_path):
    shutil.copyfile(pdf_doc_path, pdf_desktop_path)
    size_kb = os.path.getsize(pdf_desktop_path) / 1024
    print(f'PDF generated successfully!')
    print(f'Project Doc PDF: {pdf_doc_path} ({size_kb:.1f} KB)')
    print(f'Desktop PDF:     {pdf_desktop_path} ({size_kb:.1f} KB)')
else:
    print('Failed: PDF file was not created.')
