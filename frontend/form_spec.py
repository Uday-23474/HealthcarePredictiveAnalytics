"""The 13 clinical fields, in one place.

The form template, the browser-side checks and the server-side checks all
read from GROUPS, so a change here shows up everywhere.

The option values (the first item of each pair) are the labels used in the
public heart disease spreadsheet. If your encoders were fitted on different
labels, change the values here and leave the display text alone.
"""

GROUPS = [
    {
        "id": "patient",
        "title": "Patient information",
        "desc": "Basic details about the patient.",
        "fields": [
            {"name": "age", "label": "Age", "unit": "years", "kind": "number",
             "min": 18, "max": 100, "step": 1,
             "hint": "Whole years, 18 to 100."},
            {"name": "sex", "label": "Sex", "kind": "select",
             "options": [("Male", "Male"), ("Female", "Female")],
             "hint": "As recorded in the patient file."},
        ],
    },
    {
        "id": "symptoms",
        "title": "Heart symptoms",
        "desc": "What the patient reports and how the heart responds to exercise.",
        "fields": [
            {"name": "chest_pain_type", "label": "Chest pain type", "kind": "select",
             "options": [("Typical angina", "Typical angina"),
                         ("Atypical angina", "Atypical angina"),
                         ("Non-anginal pain", "Non-anginal pain"),
                         ("Asymptomatic", "Asymptomatic")],
             "hint": "The type of chest pain the patient reports."},
            {"name": "max_heart_rate", "label": "Maximum heart rate", "unit": "bpm",
             "kind": "number", "min": 60, "max": 220, "step": 1,
             "hint": "Highest rate reached during the exercise test."},
            {"name": "exercise_angina", "label": "Exercise induced angina", "kind": "select",
             "options": [("No", "No"), ("Yes", "Yes")],
             "hint": "Did exercise bring on chest pain?"},
        ],
    },
    {
        "id": "measurements",
        "title": "Blood pressure and blood tests",
        "desc": "Measurements taken at rest.",
        "fields": [
            {"name": "resting_bp", "label": "Resting blood pressure", "unit": "mm Hg",
             "kind": "number", "min": 80, "max": 220, "step": 1,
             "hint": "Measured at rest. A typical adult reading is 90 to 140."},
            {"name": "cholesterol", "label": "Cholesterol", "unit": "mg/dl",
             "kind": "number", "min": 100, "max": 600, "step": 1,
             "hint": "Serum cholesterol. Under 200 is desirable."},
            {"name": "fasting_blood_sugar", "label": "Fasting blood sugar", "kind": "select",
             "options": [("Lower than 120 mg/ml", "Lower than 120 mg/dl (Normal)"),
                         ("Greater than 120 mg/ml", "Greater than 120 mg/dl (Elevated)")],
             "hint": "Whether fasting blood sugar is above 120 mg/dl."},
        ],
    },
    {
        "id": "ecg",
        "title": "ECG and exercise test findings",
        "desc": "Results from the electrocardiogram and the stress test.",
        "fields": [
            {"name": "rest_ecg", "label": "Rest ECG", "kind": "select",
             "options": [("Normal", "Normal"),
                         ("ST-T wave abnormality", "ST-T wave abnormality"),
                         ("Left ventricular hypertrophy", "Left ventricular hypertrophy")],
             "hint": "Resting electrocardiogram result."},
            {"name": "oldpeak", "label": "Oldpeak", "unit": "ST depression",
             "kind": "number", "min": 0, "max": 7, "step": 0.1,
             "hint": "ST depression caused by exercise compared with rest, 0 to 7."},
            {"name": "slope", "label": "Slope", "kind": "select",
             "options": [("Upsloping", "Upsloping"), ("Flat", "Flat"),
                         ("Downsloping", "Downsloping")],
             "hint": "Slope of the ST segment at peak exercise."},
            {"name": "vessels", "label": "Vessels colored by fluoroscopy", "kind": "select",
             "options": [("Zero", "0"), ("One", "1"), ("Two", "2"), ("Three", "3")],
             "hint": "Number of major vessels, 0 to 3, that show up on the scan."},
            {"name": "thalassemia", "label": "Thalassemia", "kind": "select", "wide": True,
             "options": [("Normal", "Normal perfusion"),
                         ("Fixed Defect", "Fixed defect (Prior infarct)"),
                         ("Reversable Defect", "Reversible defect (Ischemia)")],
             "hint": "Blood flow result from the stress test: normal, fixed defect or reversible defect."},
        ],
    },
]


def iter_fields():
    for group in GROUPS:
        for field in group["fields"]:
            yield field


def validate(form):
    """Return (clean_values, errors). Mirrors the checks in static/js/app.js."""
    values, errors = {}, {}
    for f in iter_fields():
        name = f["name"]
        raw = (form.get(name) or "").strip()
        if f["kind"] == "number":
            if not raw:
                errors[name] = "Enter a value."
                continue
            try:
                num = float(raw)
            except ValueError:
                errors[name] = "Enter a number."
                continue
            if not (f["min"] <= num <= f["max"]):
                errors[name] = "Enter a value between %s and %s." % (f["min"], f["max"])
                continue
            if f["step"] == 1:
                if num != int(num):
                    errors[name] = "Enter a whole number."
                    continue
                values[name] = int(num)
            else:
                values[name] = round(num, 1)
        else:
            if raw == "Reversible Defect":
                raw = "Reversable Defect"
            elif "120 mg/dl" in raw:
                raw = raw.replace("mg/dl", "mg/ml")
            allowed = [value for value, _ in f["options"]]
            if raw not in allowed:
                errors[name] = "Select an option."
                continue
            values[name] = raw
    return values, errors


def display_rows(values):
    """(label, text) pairs for showing a saved record on the result page."""
    rows = []
    for f in iter_fields():
        v = values[f["name"]]
        if f["kind"] == "number":
            text = "%s %s" % (v, f["unit"]) if f.get("unit") else str(v)
        else:
            text = dict(f["options"]).get(v, v)
        rows.append((f["label"], text))
    return rows
