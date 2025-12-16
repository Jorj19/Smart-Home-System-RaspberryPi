import time
import board
import busio
import adafruit_bh1750
import adafruit_dht
import spidev

# --- BH1750 ---
i2c = busio.I2C(board.SCL, board.SDA)
bh1750 = adafruit_bh1750.BH1750(i2c)

# --- DHT22 ---
dht = adafruit_dht.DHT22(board.D4)

# --- MCP3008 ---
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_mcp(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((adc[1] & 3) << 8) + adc[2]

try:
    while True:
        # BH1750
        lux = bh1750.lux

        # DHT22
        try:
            temp = dht.temperature
            hum = dht.humidity
        except RuntimeError:
            temp = None
            hum = None

        # MQ
        mq135 = read_mcp(0)
        mq5 = read_mcp(1)
        mq7 = read_mcp(2)

        print(f"Lux: {lux} lx | Temp: {temp if temp else 'ERR'} °C | Hum: {hum if hum else 'ERR'} % | "
              f"MQ135: {mq135} | MQ5: {mq5} | MQ7: {mq7}")
        time.sleep(2)

except KeyboardInterrupt:
    print("Oprit")
finally:
    dht.exit()
    spi.close()
