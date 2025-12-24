from flask import Flask, jsonify
import time
import board
import adafruit_dht
from smbus2 import SMBus
import spidev
import random
import math
from collections import deque

def estimate_tvoc(mq135_adc, mq5_adc, mq7_adc):
    mq135_n = mq135_adc / 1023.0
    mq5_n   = mq5_adc / 1023.0
    mq7_n   = mq7_adc / 1023.0

    # ponderi
    base = (
        mq135_n * 0.6 +
        mq5_n   * 0.25 +
        mq7_n   * 0.15
    )

    # conversie în ppb
    tvoc = base * 1500

    # zgomot random
    noise = random.randint(-50, 50)

    if random.random() < 0.1: 
        tvoc *= random.uniform(1.5, 2.5)

    return int(max(tvoc + noise, 0))

def random_pm25():
    return random.randint(5, 150)  # ug/m3

def random_sound():
    return random.randint(30, 90)  # dB

def random_smoke():
    return random.choice([0, 1])  # bool

def mq7_co_ppm(adc):
    # normalizare
    ratio = adc / 1023.0

    # valori orientative
    if ratio < 0.2:
        ppm = ratio * 10          # 0–2 ppm
    elif ratio < 0.4:
        ppm = 10 + (ratio - 0.2) * 50   # 10–20 ppm
    elif ratio < 0.6:
        ppm = 20 + (ratio - 0.4) * 150  # 20–50 ppm
    else:
        ppm = 50 + (ratio - 0.6) * 300  # >50 ppm (PERICOL)

    return round(ppm, 1)


#   BH1750 (Lumina)

BH1750_ADDR = 0x23
BH1750_CONT_HIRES = 0x10
bus = SMBus(1)

def read_bh1750():
    try:
        data = bus.read_i2c_block_data(BH1750_ADDR, BH1750_CONT_HIRES, 2)
        lux = (data[0] << 8) | data[1]
        return round(lux / 1.2, 1)
    except:
        return None


#   DHT22 (Temp + Umiditate)


dht = adafruit_dht.DHT22(board.D4)

def read_dht22():
    try:
        temp = dht.temperature
        hum = dht.humidity
        if temp is not None:
            temp = round(temp, 1)
        if hum is not None:
            hum = round(hum, 1)
        return temp, hum
    except:
        return None, None


#   MCP3008 (MQ-urile)


spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_adc(ch):
    if ch < 0 or ch > 7:
        return 0
    r = spi.xfer2([1, (8 + ch) << 4, 0])
    adc_out = ((r[1] & 3) << 8) + r[2]
    return adc_out

RL = 10000.0  # Load resistor MQ

def mq_percent(adc):
    return round((adc / 1023.0) * 100, 1)


#   CO2 Auto-calibrat


adc_mq135_ref = None
_co2_buffer = deque(maxlen=5)

def mq135_co2_ppm(adc):
        global adc_mq135_ref
    
        if adc <= 0:
            return 400.0
    
        if adc_mq135_ref is None:
            adc_mq135_ref = adc
        else:
            adc_mq135_ref = min(adc_mq135_ref * 0.999, adc)
    
        ratio = adc / adc_mq135_ref
    
        ppm = 400 * (ratio ** 1.7)
    
        ppm = max(400, min(ppm, 5000))
    
        _co2_buffer.append(ppm)
        ppm_smoothed = sum(_co2_buffer) / len(_co2_buffer)
    
        return round(ppm_smoothed, 1)
    

#   Air Quality Index


def air_quality_index(mq135, mq5, mq7, co2_ppm):
    score = (mq135*0.4 + mq5*0.2 + mq7*0.2 + (co2_ppm/1000)*0.2)*100/100
    return round(min(max(score, 0), 100), 1)

#   FLASK SERVER

app = Flask(__name__)

@app.route("/sensors")
def sensors():
    # DHT22
    temp, hum = read_dht22()

    # BH1750
    lux = read_bh1750()

    # MQ-uri prin MCP3008
    adc_mq135 = read_adc(0)
    adc_mq5   = read_adc(1)
    adc_mq7   = read_adc(2)

    co2_ppm = mq135_co2_ppm(adc_mq135)
    mq135_pct = mq_percent(adc_mq135)
    mq5_pct   = mq_percent(adc_mq5)
    mq7_pct   = mq_percent(adc_mq7)

    tvoc = estimate_tvoc(adc_mq135, adc_mq5, adc_mq7)
    pm25 = random_pm25()
    sound = random_sound()
    smoke = random_smoke()
    co_ppm = mq7_co_ppm(adc_mq7)

    aqi = air_quality_index(mq135_pct, mq5_pct, mq7_pct, co2_ppm)

    data = {
        "temperature": {"valoare": temp, "unitate": "°C"},
        "humidity": {"valoare": hum, "unitate": "%"},
        "lux": {"valoare": lux, "unitate": "lux"},
        "mq135_co2": {"valoare": co2_ppm, "unitate": "ppm"},
        "mq5": {"valoare": mq5_pct, "unitate": "%"},
        "mq7": {"valoare": mq7_pct, "unitate": "%"},
        "air_quality_index": {"valoare": aqi, "unitate": "indice"},
        "tvoc": {"valoare": tvoc, "unitate": "ppb"},
        "pm2_5": {"valoare": pm25, "unitate": "ug/m3"},
        "sunet": {"valoare": sound, "unitate": "dB"},
        "fum": {"valoare": smoke, "unitate": "bool"},
        "co": {"valoare": co_ppm, "unitate": "ppm"}

    }

    return jsonify(data)

if __name__ == "__main__":
    print("Server pornit pe http://0.0.0.0:5000/sensors")
    app.run(host="0.0.0.0", port=5000)
