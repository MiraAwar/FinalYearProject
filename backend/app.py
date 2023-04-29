import io
import csv
import pickle
from flask_cors import CORS
from keras.models import load_model 
import matplotlib.pyplot as plt
from flask import Flask, request, send_file, jsonify, make_response
import NN_preprocessing_methods
import MonteCarlo_methods
import NSSRFR_methods
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

def add_cors_headers(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
        return response
    return wrapper

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

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    print(file)
    if file:
        # Specify the desired location to save the uploaded file
        file.save(file.filename)

        # Return a response indicating the success or failure of the upload
        return {'message': 'File uploaded successfully'}
    else:
        return {'error': 'File upload failed'}

@app.route("/neural_network_default", methods=["GET"])
def neural_network_default():
    loaded_model = load_model('model.h5')
    (model_input, scaler) = NN_preprocessing_methods.preprocess_csv("data/daily-treasury-rates-2014-2023.csv")
    prediction_array = loaded_model.predict(model_input)
    scaled_output = NN_preprocessing_methods.scale_input(prediction_array, scaler)
    fixed_output = NN_preprocessing_methods.fix_list(scaled_output)
    return jsonify(fixed_output)

@app.route("/neural_network/<string:csv_file>", methods=["GET"])
def neural_network(csv_file):
    print("CSV FILE:", csv_file)
    loaded_model = load_model('model.h5')
    (model_input, scaler) = NN_preprocessing_methods.preprocess_csv(csv_file)
    prediction_array = loaded_model.predict(model_input)
    scaled_output = NN_preprocessing_methods.scale_input(prediction_array, scaler)
    fixed_output = NN_preprocessing_methods.fix_list(scaled_output)
    return jsonify(fixed_output)

@app.route("/monte_carlo/<string:csv_file>", methods=["GET"])
def monte_carlo(csv_file):
    print("CSV FILE: ", csv_file)
    file_path = "output.xlsx"
    print("IT'S WORKING !!!!!!!!!!!!!!!!!!!!!")
    MonteCarlo_methods.monte_carlo_yield_estimation(csv_file).to_excel(file_path)
    print("It passed this?")
    return send_file(file_path, as_attachment=True)

# @app.route("/monte_carlo_default", methods=["GET"])
# def monte_carlo_default():
#     return print(MonteCarlo_methods.monte_carlo_yield_estimation("data/daily-treasury-rates-2014-2023.csv"))#.to_excel("output.xlsx")

@app.route("/monte_carlo_default", methods=["GET"])
def monte_carlo_default():
    file_path = "output.xlsx"
    MonteCarlo_methods.monte_carlo_yield_estimation("data/daily-treasury-rates-2014-2023.csv").to_excel(file_path)
    return send_file(file_path, as_attachment=True)

@app.route("/nss_calibrate/<int:year>/<int:maturity_bound>", methods=["GET"])
def nss_calibrate(year, maturity_bound):
    return str(NSSRFR_methods.Calibrate(year, maturity_bound))

@app.route("/nss_predict/<int:prediction_year>/<int:prediction_maturity>/<int:years_available>", methods=["GET"])
def nss_predict(prediction_year, prediction_maturity, years_available):
    return str(NSSRFR_methods.Predict(prediction_year, prediction_maturity, years_available))
    
if __name__ == "__main__":
    app.run(debug=True)