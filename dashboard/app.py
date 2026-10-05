from flask import Flask, render_template, jsonify
from datetime import datetime

app = Flask(__name__)


# -----------------------------
# Mock system data
# -----------------------------
system_state = {
    "tank_level": 76,
    "tank_capacity": 200,
    "flow_rate": 2.1,
    "consumption_today": 126.4,
    "pump": True,
    "leakage": False,
    "pump_mode": "AUTO",
    "pump_runtime": 18
}


# -----------------------------
# Dashboard page
# -----------------------------
@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# -----------------------------
# API: Get system status
# -----------------------------
@app.route("/api/status")
def status():

    water_volume = (
        system_state["tank_capacity"]
        * system_state["tank_level"]
        / 100
    )

    return jsonify({
        "tank_level": system_state["tank_level"],
        "tank_capacity": system_state["tank_capacity"],
        "water_volume": round(water_volume, 1),
        "flow_rate": system_state["flow_rate"],
        "consumption_today": system_state["consumption_today"],
        "pump": system_state["pump"],
        "leakage": system_state["leakage"],
        "pump_mode": system_state["pump_mode"],
        "pump_runtime": system_state["pump_runtime"],
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })


# -----------------------------
# Run Flask application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)