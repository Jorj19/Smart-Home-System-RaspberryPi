import time
import board
import busio
import adafruit_bh1750
import adafruit_dht
import spidev

# -------------------------
# BH1750 (I2C)
# -------------------------
i2c = busio.I2C(board.SCL, board.SDA)
bh1750 = adafruit_bh1750.BH1750(i2c)

# -------------------------
# DHT22
# -------------------------
dht = adafruit_dht.DHT22(board.D4)

# -------------------------
# MCP3008 pentru MQ135, MQ5, MQ7
# -------------------------
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_mcp(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    value = ((adc[1] & 3) << 8) + adc[2]
    return value

# -------------------------
# Loop principal
# -------------------------
try:
    while True:
        # --- BH1750 ---
        try:
            lux = bh1750.lux
        except Exception:
            lux = None

        # --- DHT22 ---
        try:
            temp = dht.temperature
            hum = dht.humidity
        except RuntimeError:
            temp = None
            hum = None

        # --- MQ sensors ---
        try:
            mq135 = read_mcp(0)
            mq5 = read_mcp(1)
            mq7 = read_mcp(2)
        except Exception:
            mq135 = mq5 = mq7 = None

        # --- Afisare valori ---
        print(f"Lux: {lux if lux is not None else 'ERR'} lx | "
              f"Temp: {temp if temp is not None else 'ERR'} °C | "
              f"Hum: {hum if hum is not None else 'ERR'} % | "
              f"MQ135: {mq135 if mq135 is not None else 'ERR'} | "
              f"MQ5: {mq5 if mq5 is not None else 'ERR'} | "
              f"MQ7: {mq7 if mq7 is not None else 'ERR'}")

        time.sleep(2)

except KeyboardInterrupt:
    print("\nOprit de utilizator")
finally:
    dht.exit()
    spi.close()
