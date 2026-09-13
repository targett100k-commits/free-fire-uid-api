from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

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

        # SOURCE API USED BY THE WEBSITE YOU PROVIDED
        api_url = "https://s.xysushi.in/ff/"

        response = requests.get(
            api_url,
            params={
                "uid": uid
            },
            headers={
                "Accept": "application/json",
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        try:
            data = response.json()

        except Exception:
            return jsonify({
                "error": "Source API returned invalid response",
                "status_code": response.status_code,
                "response_preview": response.text[:300]
            }), 502

        return jsonify(data), response.status_code

    except requests.exceptions.RequestException as e:

        return jsonify({
            "error": "Failed to connect to source API",
            "details": str(e)
        }), 502


if __name__ == "__main__":
    app.run()
