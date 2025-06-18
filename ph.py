import time
import Adafruit_ADS1x15

ads = Adafruit_ADS1x15.ADS1115(busnum=1)
GAIN = 2/3  # ±6.144V bereik

# Jouw gemeten spanningen bij pH 4 en pH 7
ph4_voltage = 4.33  # of 4.40
ph7_voltage = 3.80 # of 3.88

def voltage_to_ph(voltage):
    # Lineaire interpolatie tussen pH4 en pH7
    slope = (7 - 4) / (ph7_voltage - ph4_voltage)
    ph = 4 + slope * (voltage - ph4_voltage)
    return ph

def lees_gemiddelde_voltage(kanaal=1, samples=10):
    total = 0
    for _ in range(samples):
        raw = ads.read_adc(kanaal, gain=GAIN)
        voltage = raw * (6.144 / 32768.0)
        total += voltage
        time.sleep(0.05)  # korte pauze tussen metingen
    return total / samples

try:
    while True:
        avg_voltage = lees_gemiddelde_voltage()
        ph = voltage_to_ph(avg_voltage)
        print(f"Gemiddelde spanning: {avg_voltage:.3f} V, pH-waarde: {ph:.1f}")
        time.sleep(1)

except KeyboardInterrupt:
    print("Meten gestopt.")