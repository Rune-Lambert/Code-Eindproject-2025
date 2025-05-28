import time

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
        print("Sensor niet gevonden!")
        return None

while True:
    temp = read_temp()
    if temp is not None:
        print(f"Temperatuur: {temp:.2f} °C")
    else:
        print("Kon temperatuur niet uitlezen.")
    time.sleep(1)