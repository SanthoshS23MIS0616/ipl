import importlib.util
import subprocess
import sys
import site
import os

# ✅ List of required Python packages
required_packages = ["flask", "numpy", "scikit-learn"]

# ✅ Function to check if a package is installed (in venv or globally)
def is_package_installed(package_name):
    try:
        # Check in current environment
        if importlib.util.find_spec(package_name):
            return True

        # Check in global site-packages (Python 3.11)
        global_site_packages = site.getsitepackages()
        for path in global_site_packages:
            if os.path.exists(os.path.join(path, package_name)):
                return True
    except Exception:
        pass
    return False

# ✅ Install missing packages only if not already installed
for package in required_packages:
    if not is_package_installed(package):
        print(f"📦 Installing missing dependency: {package} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    else:
        print(f"✅ {package} already installed — skipping.")

# -------------------------------------------------------------------
# ✅ Your actual Flask app starts below
# -------------------------------------------------------------------

from flask import Flask, render_template, request
import pickle
import numpy as np

# Load the trained model
filename = 'first-innings-score-lr-model.pkl'
try:
    regressor = pickle.load(open(filename, 'rb'))
except FileNotFoundError:
    raise FileNotFoundError(f"❌ Model file '{filename}' not found in directory: {os.getcwd()}")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index1.html')

@app.route('/predict', methods=['POST'])
def predict():
    temp_array = []

    if request.method == 'POST':
        team_encoding = {
            'Chennai Super Kings': [1,0,0,0,0,0,0,0],
            'Delhi Daredevils': [0,1,0,0,0,0,0,0],
            'Kings XI Punjab': [0,0,1,0,0,0,0,0],
            'Kolkata Knight Riders': [0,0,0,1,0,0,0,0],
            'Mumbai Indians': [0,0,0,0,1,0,0,0],
            'Rajasthan Royals': [0,0,0,0,0,1,0,0],
            'Royal Challengers Bangalore': [0,0,0,0,0,0,1,0],
            'Sunrisers Hyderabad': [0,0,0,0,0,0,0,1]
        }

        batting_team = request.form['batting-team']
        bowling_team = request.form['bowling-team']

        temp_array += team_encoding[batting_team]
        temp_array += team_encoding[bowling_team]

        overs = float(request.form['overs'])
        runs = int(request.form['runs'])
        wickets = int(request.form['wickets'])
        runs_in_prev_5 = int(request.form['runs_in_prev_5'])
        wickets_in_prev_5 = int(request.form['wickets_in_prev_5'])

        temp_array += [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]

        data = np.array([temp_array])
        my_prediction = int(regressor.predict(data)[0])

        return render_template('result1.html', lower_limit=my_prediction-10, upper_limit=my_prediction+5)

if __name__ == '__main__':
    app.run(debug=True)
