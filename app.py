import numpy as np
from flask import Flask, request, render_template
import pickle
from datetime import datetime

app = Flask(__name__)

model_path = 'templates/forex_pred_model.pkl'

with open(model_path, 'rb') as file:
    linReg = pickle.load(file)


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/getting prediction", methods=["POST"])
def getprediction():
    date_string = request.form["Date"]
    date = datetime.strptime(date_string, '%Y-%m-%d')
    input = np.array([date.day])  # Assuming your model expects the day as the input feature
    final_input = np.array(input).reshape(1, -1)
    prediction = linReg.predict(final_input)

    # Render the prediction result in a template
    return render_template('index.html', output='Predicted forex prices: {}'.format(prediction[0]))


if __name__ == "__main__":
    app.run(debug=True)
