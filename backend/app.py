import os
from flask_cors import CORS
from keras.models import load_model 
from flask import Flask, request, send_file, jsonify, make_response
import NN_preprocessing_methods
import MonteCarlo_methods
import NSSRFR_methods

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

def add_cors_headers(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE'
        return response
    return wrapper

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['file']
    print(file)
    if file:
        file.save(file.filename)
        return {'message': 'File uploaded successfully'}
    else:
        return {'error': 'File upload failed'}
    
@app.route('/delete_file/<string:filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(app.root_path, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'message': 'File successfully deleted.'}), 200
    else:
        return jsonify({'message': 'File not found.'}), 404
    
@app.route("/impute_missing_data/<string:csv_file_name>", methods=["GET"])
def impute_missing_data(csv_file_name):
    file_path = "imputed_" + csv_file_name
    NN_preprocessing_methods.impute_missing_data(csv_file_name).to_csv(file_path)
    return send_file(file_path, as_attachment=True)

@app.route("/neural_network_default", methods=["GET"])
def neural_network_default():
    loaded_model = load_model('model.h5')
    (model_input, scaler) = NN_preprocessing_methods.preprocess_csv("data/daily-treasury-rates-2014-2023.csv")
    prediction_array = loaded_model.predict(model_input)
    scaled_output = NN_preprocessing_methods.scale_input(prediction_array, scaler)
    fixed_output = NN_preprocessing_methods.fix_list(scaled_output)
    return jsonify(fixed_output)

@app.route("/neural_network/<string:csv_file_name>", methods=["GET"])
def neural_network(csv_file_name):
    print("CSV FILE:", csv_file_name)
    loaded_model = load_model('model.h5')
    (model_input, scaler) = NN_preprocessing_methods.preprocess_csv(csv_file_name)
    prediction_array = loaded_model.predict(model_input)
    scaled_output = NN_preprocessing_methods.scale_input(prediction_array, scaler)
    fixed_output = NN_preprocessing_methods.fix_list(scaled_output)
    return jsonify(fixed_output)

@app.route("/monte_carlo/<string:csv_file_name>", methods=["GET"])
def monte_carlo(csv_file_name):
    file_path = "output.xlsx"
    MonteCarlo_methods.monte_carlo_yield_estimation(csv_file_name).to_excel(file_path)
    return send_file(file_path, as_attachment=True)

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