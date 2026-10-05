// -------------------------------------
// Tank Level Chart
// -------------------------------------

const tankChart = new Chart(
    document.getElementById("tankChart"),
    {
        type: "line",

        data: {
            labels: [],
            datasets: [
                {
                    label: "Tank Level (%)",

                    data: [],

                    borderWidth: 2,

                    tension: 0.3
                }
            ]
        },

        options: {
            responsive: true,

            scales: {
                y: {
                    min: 0,
                    max: 100
                }
            }
        }
    }
);


// -------------------------------------
// Consumption Chart
// -------------------------------------

const consumptionChart = new Chart(
    document.getElementById("consumptionChart"),
    {
        type: "bar",

        data: {
            labels: [
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun"
            ],

            datasets: [
                {
                    label: "Water Consumption (L)",

                    data: [
                        120,
                        145,
                        130,
                        160,
                        125,
                        150,
                        140
                    ],

                    borderWidth: 1
                }
            ]
        }
    }
);


// -------------------------------------
// Update Dashboard
// -------------------------------------

async function updateDashboard() {

    try {

        const response = await fetch("/api/status");

        const data = await response.json();


        // Statistics

        document.getElementById("tank-level")
            .textContent = data.tank_level;

        document.getElementById("water-volume")
            .textContent = data.water_volume;

        document.getElementById("flow-rate")
            .textContent = data.flow_rate;

        document.getElementById("consumption")
            .textContent = data.consumption_today;


        // Tank

        document.getElementById("tank-percentage")
            .textContent = data.tank_level;

        document.getElementById("water")
            .style.height = data.tank_level + "%";


        // System status

        document.getElementById("pump-status")
            .textContent = data.pump ? "ON" : "OFF";

        document.getElementById("pump-mode")
            .textContent = data.pump_mode;

        document.getElementById("leakage-status")
            .textContent = data.leakage ? "DETECTED" : "NO";

        document.getElementById("pump-runtime")
            .textContent = data.pump_runtime;


        // Add current level to chart

        const now = data.timestamp;

        tankChart.data.labels.push(now);

        tankChart.data.datasets[0].data.push(
            data.tank_level
        );


        // Keep only last 10 readings

        if (tankChart.data.labels.length > 10) {

            tankChart.data.labels.shift();

            tankChart.data.datasets[0].data.shift();
        }


        tankChart.update();

    }

    catch (error) {

        console.error(
            "Error loading dashboard data:",
            error
        );

    }
}


// -------------------------------------
// Start dashboard
// -------------------------------------

updateDashboard();


// Update every 3 seconds

setInterval(
    updateDashboard,
    3000
);