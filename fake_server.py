from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route("/sensors")
def sensors():
    # Date simulate (exact structura de pe Pi)
    data = {
        "temperature": { "valoare": round(random.uniform(20.0, 30.0), 1), "unitate": "°C" },
        "humidity":    { "valoare": round(random.uniform(30.0, 60.0), 1), "unitate": "%" },
        "lux":         { "valoare": round(random.uniform(100, 800), 1),   "unitate": "lx" },
        "mq135_co2":   { "valoare": round(random.uniform(400, 1500), 1),  "unitate": "ppm" },
        "pm2_5":       { "valoare": random.randint(5, 50),                "unitate": "ug/m3" },
        "tvoc":        { "valoare": random.randint(50, 400),              "unitate": "ppb" },
        "co":          { "valoare": round(random.uniform(0, 10), 1),      "unitate": "ppm" },
        "fum":         { "valoare": 0 if random.random() > 0.05 else 1,   "unitate": "bool" },
        "mq5":         { "valoare": round(random.uniform(0, 5), 1),       "unitate": "%" },
        "mq7":         { "valoare": round(random.uniform(0, 5), 1),       "unitate": "%" },
        "air_quality_index": { "valoare": random.randint(10, 90),         "unitate": "idx" },
        "sunet":       { "valoare": random.randint(30, 70),               "unitate": "dB" }
    }
    print(f"[FAKE] Temp: {data['temperature']['valoare']}")
    return jsonify(data)

if __name__ == "__main__":
    print("--- SERVER FAKE (LOCALHOST) ---")
    app.run(host="0.0.0.0", port=5000)