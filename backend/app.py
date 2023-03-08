import io
import csv
import matplotlib.pyplot as plt
from flask import Flask, request, send_file

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)