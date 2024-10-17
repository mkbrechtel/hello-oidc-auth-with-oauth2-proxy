from flask import Flask, jsonify, g
from auth import token_required

app = Flask(__name__)

# Root endpoint (token required)
@app.route("/")
@token_required
def root():
    return jsonify({"message": "Hello!", "user": g.user})


if __name__ == "__main__":
    app.run(debug=True)
