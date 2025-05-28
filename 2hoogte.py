import smbus2
import time

# I2C-bus (1 is standaard op Raspberry Pi)
bus = smbus2.SMBus(1)

# I2C-adres van de multiplexer (TCA9548A)
MUX_ADDR = 0x70

# Adressen van de sensoren
ATTINY1_HIGH_ADDR = 0x78  # Hogere secties
ATTINY2_LOW_ADDR = 0x77   # Lagere secties

# Multiplexer kanaal selecteren
def select_mux_channel(channel):
    if 0 <= channel <= 7:
        bus.write_byte(MUX_ADDR, 1 << channel)
        time.sleep(0.05)  # korte delay om te stabiliseren
    else:
        raise ValueError("Kanaal moet tussen 0 en 7 liggen.")

# Lees 12 hogere secties
def get_high_section_value():
    high_data = []
    bus.write_byte(ATTINY1_HIGH_ADDR, 0)
    time.sleep(0.1)
    for i in range(12):
        high_data.append(bus.read_byte(ATTINY1_HIGH_ADDR))
    return high_data

# Lees 8 lagere secties
def get_low_section_value():
    low_data = []
    bus.write_byte(ATTINY2_LOW_ADDR, 0)
    time.sleep(0.1)
    for i in range(8):
        low_data.append(bus.read_byte(ATTINY2_LOW_ADDR))
    return low_data

# Berekent waterniveau in percentage
def calculate_water_level_percentage():
    high_data = get_high_section_value()
    low_data = get_low_section_value()

    # Tel hoeveel secties een waarde ≥ 50 hebben
    low_count = sum(1 for value in low_data if value >= 50)
    high_count = sum(1 for value in high_data if value >= 50)

    total_triggered_sections = low_count + high_count
    total_sections = 20  # 8 laag + 12 hoog
    return (total_triggered_sections / total_sections) * 100

# Omzetten naar centimeters
def convert_percentage_to_cm(percentage):
    max_height_cm = 10
    return (percentage / 100) * max_height_cm

# Hoofdlus
while True:
    for channel in [0, 1]:  # Sensor 1 op kanaal 0, sensor 2 op kanaal 1
        select_mux_channel(channel)

        # Naam geven op basis van kanaal
        if channel == 0:
            sensor_naam = "Sensor hoogte aquarium"
        elif channel == 1:
            sensor_naam = "Sensor hoogte filterbak"
        else:
            sensor_naam = f"Sensor kanaal {channel}"

        print(f"\n--- {sensor_naam} ---")

        try:
            # Lees en bereken waterniveau
            percentage = calculate_water_level_percentage()
            cm = convert_percentage_to_cm(percentage)

            # Print resultaten
            print(f"Waterniveau: {percentage:.2f}%")
            print(f"Waterhoogte: {cm:.2f} cm")
        except Exception as e:
            print(f"Fout bij uitlezen van {sensor_naam}: {e}")

        time.sleep(1)  # korte pauze tussen de sensoren

    time.sleep(1)  # wachttijd voor volgende volledige cyclus
