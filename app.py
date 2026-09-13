from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time

app = Flask(__name__)

CORS(app)


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Free Fire UID API is working"
    })


@app.route("/info", methods=["GET"])
def get_player_info():

    uid = request.args.get("uid")

    if not uid:
        return jsonify({
            "error": "UID is required"
        }), 400

    if not uid.isdigit():
        return jsonify({
            "error": "UID must contain numbers only"
        }), 400

    try:

        api_url = "https://wzapiinfo.vercel.app/get"

        response = requests.get(
            api_url,
            params={
                "uid": uid,
                "_t": int(time.time())
            },
            headers={
                "Cache-Control": "no-cache",
                "Pragma": "no-cache"
            },
            timeout=20
        )

        try:
            data = response.json()

        except Exception:
            return jsonify({
                "error": "API returned invalid response",
                "status_code": response.status_code
            }), 502

        return jsonify(data), response.status_code

    except requests.exceptions.RequestException as e:

        return jsonify({
            "error": "Failed to connect to player API",
            "details": str(e)
        }), 502


if __name__ == "__main__":
    app.run()
