from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)

system_state = {
    "tank_level": 0,
    "tank_capacity": 200,
    "flow_rate": 0,
    "consumption_today": 0,
    "pump": False,
    "leakage": False,
    "pump_mode": "AUTO",
    "pump_runtime": 0,
    "distance": 0,
    "timestamp": "--",
    "sensor_connected": False
}


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/status")
def status():

    water_volume = (
        system_state["tank_capacity"]
        * system_state["tank_level"]
        / 100
    )

    return jsonify({
        **system_state,
        "water_volume": round(water_volume, 1)
    })


@app.route("/api/sensor-data", methods=["POST"])
def receive_sensor_data():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Invalid JSON data"
        }), 400

    required = ["tank_level", "distance", "pump"]

    if any(key not in data for key in required):
        return jsonify({
            "error": "Missing sensor fields"
        }), 400

    try:
        level = float(data["tank_level"])
        distance = float(data["distance"])

        if not 0 <= level <= 100 or distance < 0:
            raise ValueError("Invalid sensor readings")

    except (TypeError, ValueError):
        return jsonify({
            "error": "Invalid sensor readings"
        }), 400

    system_state["tank_level"] = round(level, 1)
    system_state["distance"] = round(distance, 1)
    system_state["pump"] = bool(data["pump"])
    system_state["leakage"] = bool(data.get("leakage", False))
    system_state["timestamp"] = datetime.now().strftime("%H:%M:%S")
    system_state["sensor_connected"] = True

    return jsonify({
        "message": "Sensor data received successfully"
    }), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )