import io
import csv
import pickle
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request, send_file
import NN_preprocessing_methods
import MonteCarlo_methods
import NSSRFR_methods
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/process_csv", methods=["POST"])
def process_csv():
    file = request.files["file"]
    if not file:
        return {"error": "No file provided"}, 400

    file_contents = file.read().decode("utf-8")
    reader = csv.reader(io.StringIO(file_contents))
    header = next(reader)
    data = [row for row in reader]

    # Do something with the data
    x = [int(row[0]) for row in data]
    y = [int(row[1]) for row in data]
    plt.plot(x, y)

    # Create the plot as a PNG image
    plot_file = io.BytesIO()
    plt.savefig(plot_file, format="png")
    plot_file.seek(0)

    return send_file(plot_file, mimetype="image/png")


@app.route("/neural_network_default", methods=["GET"])
def neural_network_default():
    model_input = NN_preprocessing_methods.preprocess_csv("data/daily-treasury-rates-2014-2023.csv")
    pickled_model = pickle.load(open('model.pkl', 'rb'))
    prediction_array = pickled_model.predict(model_input)
    scaled_output = NN_preprocessing_methods.scale_input(prediction_array)
    return scaled_output

@app.route("/neural_network/<string:csv_file>", methods=["GET"])
def neural_network(csv_file):
    model_input = NN_preprocessing_methods.preprocess_csv(csv_file)
    pickled_model = pickle.load(open('model.pkl', 'rb'))
    prediction_array = pickled_model.predict(model_input)
    scaled_output = NN_preprocessing_methods.scale_input(prediction_array)
    return scaled_output

@app.route("/monte_carlo/<string:csv_file>", methods=["GET"])
def monte_carlo(csv_file):
    MonteCarlo_methods.monte_carlo_yield_estimation(csv_file).to_excel("output.xlsx")

@app.route("/monte_carlo_default", methods=["GET"])
def monte_carlo_default():
    return MonteCarlo_methods.monte_carlo_yield_estimation("data/daily-treasury-rates-2022.csv").to_excel("output.xlsx")

@app.route("/nss_calibrate/<int:year>/<int:maturity_bound>", methods=["GET"])
def nss_calibrate(year, maturity_bound):
    result = NSSRFR_methods.Calibrate(year, maturity_bound)
    popt_list = np.array(result[0]).tolist()
    pcov_list = np.array(result[1]).tolist()
    return jsonify({'popt': popt_list, 'pcov': pcov_list})

@app.route("/nss_predict/<int:prediction_year>/<int:prediction_maturity>/<int:years_available>", methods=["GET"])
def nss_predict(prediction_year, prediction_maturity, years_available):
    return str(NSSRFR_methods.Predict(prediction_year, prediction_maturity, years_available))
    
if __name__ == "__main__":
    app.run(debug=True)