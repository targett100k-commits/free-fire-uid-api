from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

GAMESKINBO_API_KEY = os.environ.get("GAMESKINBO_API_KEY")

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "service": "Free Fire UID Info API"
    })


@app.route("/info", methods=["GET"])
def get_player_info():

    uid = request.args.get("uid")
    region = request.args.get("region", "IND").upper()

    if not uid:
        return jsonify({
            "error": "UID is required"
        }), 400

    if not uid.isdigit():
        return jsonify({
            "error": "UID must contain numbers only"
        }), 400

    if not GAMESKINBO_API_KEY:
        return jsonify({
            "error": "Games Kinbo API key is not configured"
        }), 500

    url = "https://api.gameskinbo.com/ff-info/get"

    headers = {
        "x-api-key": GAMESKINBO_API_KEY
    }

    params = {
        "uid": uid,
        "region": region
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=20
        )

        try:
            data = response.json()
        except Exception:
            data = {
                "error": response.text
            }

        return jsonify(data), response.status_code

    except requests.exceptions.RequestException as e:

        return jsonify({
            "error": "Failed to connect to Games Kinbo",
            "details": str(e)
        }), 502


if __name__ == "__main__":
    app.run()
