import os
from flask_cors import CORS
from keras.models import load_model 
from flask import Flask, request, send_file, jsonify, make_response
import NN_preprocessing_methods
import MonteCarlo_methods
import NSSBFGS_methods
import RFR_methods
import NSSVARDEX_methods
import Stocks_methods

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
    

####################################################################################################################################
# App and Data related APIs
####################################################################################################################################

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
    
# @app.route('/delete_file/<string:filename>', methods=['DELETE'])
# def delete_file(filename):
#     file_path = os.path.join(app.root_path, filename)
#     if os.path.exists(file_path):
#         os.remove(file_path)
#         return jsonify({'message': 'File successfully deleted.'}), 200
#     else:
#         return jsonify({'message': 'File not found.'}), 404
    
@app.route("/impute_missing_data/<string:csv_file_name>", methods=["GET"])
def impute_missing_data(csv_file_name):
    file_path = "imputed_" + csv_file_name
    NN_preprocessing_methods.impute_missing_data(csv_file_name)
    return send_file(file_path, as_attachment=True)

####################################################################################################################################
# Neural Network related APIs
####################################################################################################################################

@app.route("/neural_network_default", methods=["GET"])
def neural_network_default():
    loaded_model = load_model('model.h5')
    (model_input, scaler) = NN_preprocessing_methods.preprocess_csv("data/daily-treasury-rates-2021.csv")
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

####################################################################################################################################
# Monte-Carlo related APIs
####################################################################################################################################

@app.route("/monte_carlo/<string:csv_file_name>/<int:number_of_days>", methods=["GET"])
def monte_carlo(csv_file_name, number_of_days):
    file_path = "output.xlsx"
    MonteCarlo_methods.monte_carlo_yield_estimation(csv_file_name, number_of_days).to_excel(file_path)
    return send_file(file_path, as_attachment=True)

@app.route("/monte_carlo_default/<int:number_of_days>", methods=["GET"])
def monte_carlo_default(number_of_days):
    file_path = "output.xlsx"
    MonteCarlo_methods.monte_carlo_yield_estimation("data/daily-treasury-rates-2022.csv", number_of_days).to_excel(file_path)
    return send_file(file_path, as_attachment=True)

####################################################################################################################################
# NSS related APIs
####################################################################################################################################

@app.route("/nss_calibrate/<int:year>/<int:maturity_bound>", methods=["GET"])
def nss_calibrate(year, maturity_bound):
    return list(NSSBFGS_methods.Calibrate(maturity_bound=maturity_bound+1, data_year=year))

@app.route("/nss_predict_value/<int:prediction_year>/<int:prediction_maturity>", methods=["GET"])
def nss_predict_value(prediction_year, prediction_maturity):
    return str(NSSBFGS_methods.PredictValue(prediction_year=prediction_year, prediction_maturity=prediction_maturity))

@app.route("/nss_predict_array/<int:prediction_year>/<int:prediction_maturity>", methods=["GET"])
def nss_predict_array(prediction_year, prediction_maturity):
    return list(NSSBFGS_methods.PredictArray(prediction_year=prediction_year, prediction_maturity=prediction_maturity))

####################################################################################################################################
# RFR related APIs
####################################################################################################################################

@app.route("/rfr_predict_default/<string:prediction_maturity>", methods=["GET"])
def rfr_predict_default(prediction_maturity):
    return list(RFR_methods.Predict_RFR(prediction_maturity=prediction_maturity))

@app.route("/rfr_predict/<string:csv_file>/<string:prediction_maturity>", methods=["GET"])
def rfr_predict(csv_file, prediction_maturity):
    return list(RFR_methods.Predict_RFR(prediction_maturity=prediction_maturity, csv=csv_file))

####################################################################################################################################
# Exchange Rate related APIs
####################################################################################################################################

@app.route("/exchange_predict_default/<string:prediction_date>/<string:currency_from>/<string:currency_to>", methods=["GET"])
def exchange_predict_default(prediction_date, currency_from, currency_to):
    return str(NSSVARDEX_methods.PredictExchange(prediction_date=prediction_date, currency_from=currency_from, currency_to=currency_to))

@app.route("/exchange_predict/<string:prediction_date>/<string:csv_file>", methods=["GET"])
def exchange_predict(prediction_date, csv_file):
    return str(NSSVARDEX_methods.PredictExchange(prediction_date=prediction_date, csv=csv_file))

####################################################################################################################################
# Stock Prices related APIs
####################################################################################################################################

@app.route("/stock_predict/<string:stock>/<int:predict_days>", methods=["GET"])
def stock_predict(stock, predict_days):
    return str(Stocks_methods.predict_stock_closing_price(stock, predict_days))
    
if __name__ == "__main__":
    app.run(debug=True)