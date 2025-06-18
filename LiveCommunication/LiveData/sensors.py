# import Adafruit_ADS1x15
# import smbus2
# import time

# # === pH-sensor instellingen ===
# ads = Adafruit_ADS1x15.ADS1115(busnum=1)
# GAIN = 1
# pH_offset = 4650
# pH_slope = 59

# def read_ph_sensor(channel=0):
#     adc_value = ads.read_adc(channel, gain=GAIN)
#     voltage = (adc_value / 32767.0) * 5.0
#     pH_value = (adc_value - pH_offset) / pH_slope + 7
#     return pH_value

# # === Temperatuursensor (DS18B20) instellingen ===
# def read_temp():
#     device_folder = '/sys/bus/w1/devices/28-00000055e325'
#     device_file = f'{device_folder}/w1_slave'

#     try:
#         with open(device_file, 'r') as f:
#             lines = f.readlines()
#         if lines[0].strip()[-3:] != 'YES':
#             return None
#         equals_pos = lines[1].find('t=')
#         if equals_pos != -1:
#             temp_string = lines[1][equals_pos + 2:]
#             temp_c = float(temp_string) / 1000.0
#             return temp_c
#     except FileNotFoundError:
#         print("Temperatuursensor niet gevonden!")
#         return None

# # === Multiplexer & grove waterhoogte sensoren ===
# MUX_ADDR = 0x70
# ATTINY1_HIGH_ADDR = 0x78
# ATTINY2_LOW_ADDR = 0x77
# bus = smbus2.SMBus(1)

# def select_mux_channel(channel):
#     if 0 <= channel <= 7:
#         bus.write_byte(MUX_ADDR, 1 << channel)
#         time.sleep(0.05)
#     else:
#         raise ValueError("Kanaal moet tussen 0 en 7 liggen.")

# def get_high_section_value():
#     high_data = []
#     bus.write_byte(ATTINY1_HIGH_ADDR, 0)
#     time.sleep(0.1)
#     for i in range(12):
#         high_data.append(bus.read_byte(ATTINY1_HIGH_ADDR))
#     return high_data

# def get_low_section_value():
#     low_data = []
#     bus.write_byte(ATTINY2_LOW_ADDR, 0)
#     time.sleep(0.1)
#     for i in range(8):
#         low_data.append(bus.read_byte(ATTINY2_LOW_ADDR))
#     return low_data

# def calculate_water_level_percentage():
#     high_data = get_high_section_value()
#     low_data = get_low_section_value()

#     low_count = sum(1 for value in low_data if value >= 50)
#     high_count = sum(1 for value in high_data if value >= 50)

#     total_triggered_sections = low_count + high_count
#     total_sections = 20
#     return (total_triggered_sections / total_sections) * 100

# def convert_percentage_to_cm(percentage):
#     max_height_cm = 10
#     return (percentage / 100) * max_height_cm

# # Functie om alle sensordata in 1 keer op te halen
# def get_sensor_data():
#     # Lees temperatuur & pH
#     ph_value = read_ph_sensor()
#     temp_value = read_temp()

#     # Voor elk kanaal op de multiplexer (0 = aquarium, 1 = filterbak)
#     waterhoogtes = {}
#     for channel in [0, 1]:
#         select_mux_channel(channel)
#         naam = "aquarium" if channel == 0 else "filterbak"
#         try:
#             perc = calculate_water_level_percentage()
#             cm = convert_percentage_to_cm(perc)
#             waterhoogtes[naam] = {
#                 "percentage": perc,
#                 "cm": cm
#             }
#         except Exception as e:
#             print(f"Fout bij uitlezen {naam}: {e}")
#             waterhoogtes[naam] = {
#                 "percentage": None,
#                 "cm": None
#             }

#     # Gegevens voorbereiden voor teruggeven als JSON
#     sensor_data = {
#         "ph": round(ph_value, 2),
#         "temperature": round(temp_value, 2) if temp_value is not None else None,
#         "water_levels": waterhoogtes
#     }

#     # De data wordt teruggestuurd als een dictionary met sensorwaarden
#     return sensor_data

# import time
# import Adafruit_ADS1x15
# import smbus2

# # === pH-sensor instellingen ===
# ads = Adafruit_ADS1x15.ADS1115(busnum=1)
# GAIN = 2/3  # ±6.144V bereik

# # Jouw gemeten spanningen bij pH 4 en pH 7 (kalibratie)
# ph4_voltage = 4.33
# ph7_voltage = 3.80

# def voltage_to_ph(voltage):
#     slope = (7 - 4) / (ph7_voltage - ph4_voltage)
#     ph = 4 + slope * (voltage - ph4_voltage)
#     return ph

# def lees_gemiddelde_voltage(kanaal=1, samples=10):
#     total = 0
#     for _ in range(samples):
#         raw = ads.read_adc(kanaal, gain=GAIN)
#         voltage = raw * (6.144 / 32768.0)
#         total += voltage
#         time.sleep(0.05)
#     return total / samples

# def read_ph_sensor():
#     avg_voltage = lees_gemiddelde_voltage()
#     ph_value = voltage_to_ph(avg_voltage)
#     return ph_value

# # === Temperatuursensor (DS18B20) instellingen ===
# def read_temp():
#     device_folder = '/sys/bus/w1/devices/28-00000055e325'
#     device_file = f'{device_folder}/w1_slave'

#     try:
#         with open(device_file, 'r') as f:
#             lines = f.readlines()
#         if lines[0].strip()[-3:] != 'YES':
#             return None
#         equals_pos = lines[1].find('t=')
#         if equals_pos != -1:
#             temp_string = lines[1][equals_pos + 2:]
#             temp_c = float(temp_string) / 1000.0
#             return temp_c
#     except FileNotFoundError:
#         return None

# # === Multiplexer & grove waterhoogte sensoren ===
# MUX_ADDR = 0x70
# ATTINY1_HIGH_ADDR = 0x78
# ATTINY2_LOW_ADDR = 0x77
# bus = smbus2.SMBus(1)

# def select_mux_channel(channel):
#     if 0 <= channel <= 7:
#         bus.write_byte(MUX_ADDR, 1 << channel)
#         time.sleep(0.05)
#     else:
#         raise ValueError("Kanaal moet tussen 0 en 7 liggen.")

# def get_high_section_value():
#     high_data = []
#     bus.write_byte(ATTINY1_HIGH_ADDR, 0)
#     time.sleep(0.1)
#     for _ in range(12):
#         high_data.append(bus.read_byte(ATTINY1_HIGH_ADDR))
#     return high_data

# def get_low_section_value():
#     low_data = []
#     bus.write_byte(ATTINY2_LOW_ADDR, 0)
#     time.sleep(0.1)
#     for _ in range(8):
#         low_data.append(bus.read_byte(ATTINY2_LOW_ADDR))
#     return low_data

# def calculate_water_level_percentage():
#     high_data = get_high_section_value()
#     low_data = get_low_section_value()

#     low_count = sum(1 for value in low_data if value >= 50)
#     high_count = sum(1 for value in high_data if value >= 50)

#     total_triggered_sections = low_count + high_count
#     total_sections = 20
#     return (total_triggered_sections / total_sections) * 100

# def convert_percentage_to_cm(percentage):
#     max_height_cm = 10
#     return (percentage / 100) * max_height_cm

# def get_sensor_data():
#     ph_value = read_ph_sensor()
#     temp_value = read_temp()

#     waterhoogtes = {}
#     for channel in [0, 1]:
#         select_mux_channel(channel)
#         naam = "aquarium" if channel == 0 else "filterbak"
#         try:
#             perc = calculate_water_level_percentage()
#             cm = convert_percentage_to_cm(perc)
#             waterhoogtes[naam] = {
#                 "percentage": perc,
#                 "cm": cm
#             }
#         except Exception:
#             waterhoogtes[naam] = {
#                 "percentage": None,
#                 "cm": None
#             }

#     sensor_data = {
#         "ph": round(ph_value, 2),
#         "temperature": round(temp_value, 2) if temp_value is not None else None,
#         "water_levels": waterhoogtes
#     }
#     return sensor_data
import time
import Adafruit_ADS1x15
import smbus2

# === ADS1115 voor pH-sensor ===
ads = Adafruit_ADS1x15.ADS1115(busnum=1)
GAIN = 2/3  # ±6.144V bereik

# Jouw gemeten spanningen bij pH 4 en pH 7 (kalibratie)
ph4_voltage = 4.40  # Pas aan als nodig
ph7_voltage = 3.88  # Pas aan als nodig

def voltage_to_ph(voltage):
    slope = (7 - 4) / (ph7_voltage - ph4_voltage)
    ph = 4 + slope * (voltage - ph4_voltage)
    return ph

def lees_gemiddelde_voltage(kanaal=1, samples=10):
    total = 0
    for _ in range(samples):
        raw = ads.read_adc(kanaal, gain=GAIN)
        voltage = raw * (6.144 / 32768.0)
        total += voltage
        time.sleep(0.05)
    return total / samples

def read_ph_sensor():
    avg_voltage = lees_gemiddelde_voltage()
    return voltage_to_ph(avg_voltage)

# === Temperatuursensor (DS18B20) instellingen ===
def read_temp():
    device_folder = '/sys/bus/w1/devices/28-00000055e325'
    device_file = f'{device_folder}/w1_slave'

    try:
        with open(device_file, 'r') as f:
            lines = f.readlines()
        if lines[0].strip()[-3:] != 'YES':
            return None
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c
    except FileNotFoundError:
        print("Temperatuursensor niet gevonden!")
        return None

# === Multiplexer & grove waterhoogte sensoren ===
MUX_ADDR = 0x70
ATTINY1_HIGH_ADDR = 0x78
ATTINY2_LOW_ADDR = 0x77
bus = smbus2.SMBus(1)

def select_mux_channel(channel):
    if 0 <= channel <= 7:
        bus.write_byte(MUX_ADDR, 1 << channel)
        time.sleep(0.05)
    else:
        raise ValueError("Kanaal moet tussen 0 en 7 liggen.")

def get_high_section_value():
    high_data = []
    bus.write_byte(ATTINY1_HIGH_ADDR, 0)
    time.sleep(0.1)
    for i in range(12):
        high_data.append(bus.read_byte(ATTINY1_HIGH_ADDR))
    return high_data

def get_low_section_value():
    low_data = []
    bus.write_byte(ATTINY2_LOW_ADDR, 0)
    time.sleep(0.1)
    for i in range(8):
        low_data.append(bus.read_byte(ATTINY2_LOW_ADDR))
    return low_data

def calculate_water_level_percentage():
    high_data = get_high_section_value()
    low_data = get_low_section_value()

    low_count = sum(1 for value in low_data if value >= 50)
    high_count = sum(1 for value in high_data if value >= 50)

    total_triggered_sections = low_count + high_count
    total_sections = 20
    return (total_triggered_sections / total_sections) * 100

def convert_percentage_to_cm(percentage):
    max_height_cm = 10
    return (percentage / 100) * max_height_cm

# Functie om alle sensordata in 1 keer op te halen
def get_sensor_data():
    ph_value = read_ph_sensor()
    temp_value = read_temp()

    waterhoogtes = {}
    for channel in [0, 1]:
        select_mux_channel(channel)
        naam = "aquarium" if channel == 0 else "filterbak"
        try:
            perc = calculate_water_level_percentage()
            cm = convert_percentage_to_cm(perc)
            waterhoogtes[naam] = {
                "percentage": perc,
                "cm": cm
            }
        except Exception as e:
            print(f"Fout bij uitlezen {naam}: {e}")
            waterhoogtes[naam] = {
                "percentage": None,
                "cm": None
            }

    sensor_data = {
        "ph": round(ph_value, 1),
        "temperature": round(temp_value, 1) if temp_value is not None else None,
        "water_levels": waterhoogtes
    }

    return sensor_data


if __name__ == "__main__":
    try:
        while True:
            data = get_sensor_data()
            print(data)
            time.sleep(2)
    except KeyboardInterrupt:
        print("Programma gestopt.")
