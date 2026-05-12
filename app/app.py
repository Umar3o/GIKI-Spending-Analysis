import os
import joblib
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'outputs', 'best_model.joblib')

YEARS = ['Freshman', 'Sophomore', 'Junior', 'Senior']
MAJORS = ['FCSE', 'Engineering', 'MGS']
GENDERS = ['Male', 'Female']


def classify(allowance, predicted_spend):
    surplus = allowance - predicted_spend
    threshold = 0.05 * allowance
    if surplus > threshold:
        return 'Saving', surplus
    elif surplus < -threshold:
        return 'Overspending', surplus
    else:
        return 'Balanced', surplus


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', years=YEARS, majors=MAJORS, genders=GENDERS)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        age = float(request.form['age'])
        year = request.form['year']
        major = request.form['major']
        gender = request.form['gender']
        allowance = float(request.form['allowance'])
    except (KeyError, ValueError):
        return render_template('index.html', years=YEARS, majors=MAJORS, genders=GENDERS,
                               error='Please fill in all fields correctly.')

    model = joblib.load(MODEL_PATH)

    X = pd.DataFrame([{'age': age, 'year': year, 'major': major, 'gender': gender}])
    predicted_spend = float(model.predict(X)[0])

    status, surplus = classify(allowance, predicted_spend)

    return render_template(
        'index.html',
        years=YEARS, majors=MAJORS, genders=GENDERS,
        result={
            'predicted_spend': predicted_spend,
            'status': status,
            'surplus': surplus,
        },
        form={
            'age': age, 'year': year, 'major': major,
            'gender': gender, 'allowance': allowance,
        }
    )


if __name__ == '__main__':
    app.run(debug=True)
