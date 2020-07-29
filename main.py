from flask import Flask, request, jsonify
from apis.address import ResponseBuilder

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route("/api/getAddresses", methods=["POST"])
def get_addresses():
    if "csv_file" not in request.files:
        return "No file given"
    file = request.files['csv_file']
    response_object = ResponseBuilder(file)
    return jsonify(response_object.get())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
