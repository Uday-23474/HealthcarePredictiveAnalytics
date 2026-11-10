"""
HeartCare AI: Enterprise Clinical Decision Support & Predictive Analytics Platform.
Root launch gateway that boots the unified application.
"""
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
if FRONTEND_DIR not in sys.path:
    sys.path.insert(0, FRONTEND_DIR)

from frontend.app import app

if __name__ == "__main__":
    print("=" * 60)
    print("HeartCare AI - Unified Healthcare Predictive Analytics Platform")
    print("=" * 60)
    print("Serving from: http://127.0.0.1:5000")
    print("Modules Active:")
    print("  - 🩺 Prediction Portal:      http://127.0.0.1:5000/predict")
    print("  - 🎚️ What-If Simulator:      http://127.0.0.1:5000/simulator")
    print("  - 📊 Analytics Dashboard:    http://127.0.0.1:5000/dashboard")
    print("  - 🔬 Model Benchmarks:       http://127.0.0.1:5000/analytics")
    print("  - 📋 Patient History:        http://127.0.0.1:5000/history")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=True)