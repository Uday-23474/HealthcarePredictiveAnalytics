# HeartCare AI front end

This is the front end for the Healthcare Predictive Analytics Platform. It is a Flask project with four pages: the prediction form, the result page, the history list and the analytics dashboard. It uses plain HTML, CSS and JavaScript with no libraries, so nothing needs to be installed on the browser side.

## Run it

    pip install -r requirements.txt
    python app.py

Open http://127.0.0.1:5000. The app starts with 18 demo records so the history and dashboard pages are not empty. Set HEARTCARE_DEMO=0 to start with none.

## What is stubbed

The model and the database are placeholders so the pages work on their own. In app.py there are four functions marked SWAP. run_model should load your saved KNN model, encoders and scaler, then return the prediction (1 or 0) and the probability as a percentage. save_prediction, get_prediction and list_predictions should run your MySQL INSERT and SELECT queries. Each record is a dictionary with the keys id, created_at, inputs, prediction, probability and risk. Keep those keys and the templates work unchanged.

## Risk bands

LOW_MAX and HIGH_MIN at the top of app.py set the bands. The gauge, the legend and the dashboard charts all read from them. Set them to the same rule your code uses to turn a probability into Low, Moderate or High.

## Form fields

The 13 fields live in form_spec.py. The form, the browser checks and the server checks all read from that file. The option values match the public heart disease spreadsheet. If your encoders were fitted on different labels, change the values there.

## Files

    app.py              routes, stubs, demo data
    form_spec.py        the 13 fields and their validation
    templates/          base, predict, result, history, dashboard
    static/css/         style.css
    static/js/          app.js
