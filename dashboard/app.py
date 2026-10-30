from flask import Flask, render_template, jsonify, request
from datetime import datetime

app = Flask(__name__)

# ---------------- SYSTEM STATE ----------------

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


# ---------------- DASHBOARD PAGES ----------------

@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        active_page="dashboard"
    )


@app.route("/tank-monitor")
def tank_monitor():
    return render_template(
        "tank_monitor.html",
        active_page="tank-monitor"
    )


@app.route("/analytics")
def analytics():
    return render_template(
        "analytics.html",
        active_page="analytics"
    )


@app.route("/alerts")
def alerts():
    return render_template(
        "alerts.html",
        active_page="alerts"
    )


# ---------------- STATUS API ----------------

@app.route("/api/status", methods=["GET"])
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


# ---------------- RECEIVE ARDUINO DATA ----------------

@app.route("/api/sensor-data", methods=["POST"])
def receive_sensor_data():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Invalid JSON data"
        }), 400

    required_fields = [
        "tank_level",
        "distance",
        "pump"
    ]

    if any(field not in data for field in required_fields):
        return jsonify({
            "error": "Missing required sensor fields"
        }), 400

    try:
        level = float(data["tank_level"])
        distance = float(data["distance"])

        if not 0 <= level <= 100 or distance < 0:
            raise ValueError("Invalid sensor readings")

        pump_value = data["pump"]

        if not isinstance(pump_value, bool):
            if pump_value not in (0, 1):
                raise ValueError("Invalid pump status")

            pump_value = bool(pump_value)

        leakage_value = data.get("leakage", False)

        if not isinstance(leakage_value, bool):
            if leakage_value not in (0, 1):
                raise ValueError("Invalid leakage status")

            leakage_value = bool(leakage_value)

    except (TypeError, ValueError):
        return jsonify({
            "error": "Invalid sensor readings"
        }), 400

    # Update system readings
    system_state["tank_level"] = round(level, 1)
    system_state["distance"] = round(distance, 1)
    system_state["pump"] = pump_value
    system_state["leakage"] = leakage_value
    system_state["timestamp"] = datetime.now().strftime("%H:%M:%S")
    system_state["sensor_connected"] = True

    return jsonify({
        "message": "Sensor data received successfully",
        "tank_level": system_state["tank_level"],
        "distance": system_state["distance"],
        "pump": system_state["pump"]
    }), 200


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )