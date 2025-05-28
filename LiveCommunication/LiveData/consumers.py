# import asyncio
# import json
# from channels.consumer import AsyncConsumer, SyncConsumer
# from channels.exceptions import StopConsumer

# # 🌡️ Sensor uitleesfunctie (DS18B20 via 1-Wire)
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
#         print("Sensor niet gevonden!")
#         return None


# # 🧠 Sync Consumer (optioneel, als je hem nodig hebt)
# class MySyncConsumer(SyncConsumer):
#     def websocket_connect(self, event):
#         print("WebSocket connected (sync)", event)
#         self.send({
#             'type': 'websocket.accept'
#         })

#     def websocket_receive(self, event):
#         print("Message received (sync):", event)
#         self.send({
#             'type': 'websocket.send',
#             'text': "Hallo vanuit SyncConsumer!"
#         })

#     def websocket_disconnect(self, event):
#         print("WebSocket disconnected (sync)", event)
#         raise StopConsumer()


# # ⚡ Async Consumer met sensor-data
# class MyAsyncConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):
#         print("WebSocket connected (async)", event)
#         await self.send({
#             'type': 'websocket.accept'
#         })

#         # Verstuur 30 keer de temperatuur (of gebruik while True voor onbeperkt)
#         for _ in range(30):
#             temp = read_temp()
#             if temp is not None:
#                 await self.send({
#                     'type': 'websocket.send',
#                     'text': json.dumps({'temperature': round(temp, 2)})
#                 })
#             else:
#                 await self.send({
#                     'type': 'websocket.send',
#                     'text': json.dumps({'error': 'Sensor niet uitgelezen'})
#                 })
#             await asyncio.sleep(2)

#     async def websocket_receive(self, event):
#         print("Message received (async):", event)

#     async def websocket_disconnect(self, event):
#         print("WebSocket disconnected (async)", event)
#         raise StopConsumer()
# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# import asyncio

# from .sensors import get_sensor_data  # Import jouw meetfunctie (zie stap 2)

# class MyAsyncConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         self.send_data = True
#         asyncio.create_task(self.send_sensor_data())

#     async def disconnect(self, close_code):
#         self.send_data = False

#     async def send_sensor_data(self):
#         while self.send_data:
#             data = get_sensor_data()  # Dit haalt temp, pH en waterhoogte op

#             await self.send(text_data=json.dumps(data))
#             await asyncio.sleep(1)
# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# import asyncio
# from .sensors import get_sensor_data  # Importeren van de sensordata ophalen functie

# class MyAsyncConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Accepteer de WebSocket-verbinding
#         await self.accept()

#         self.send_data = True
#         # Start een achtergrondtaak die sensor data verstuurt
#         asyncio.create_task(self.send_sensor_data())

#     async def disconnect(self, close_code):
#         # Stop met het verzenden van data als de WebSocket verbinding wordt verbroken
#         self.send_data = False

#     async def send_sensor_data(self):
#         while self.send_data:
#             # Haal de laatste sensor data op
#             data = get_sensor_data()

#             # Stuur de sensor data naar de WebSocket
#             await self.send(text_data=json.dumps(data))

#             # Wacht een seconde voordat we de volgende set gegevens sturen
#             await asyncio.sleep(1)
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .sensors import get_sensor_data  # Importeren van de sensordata ophalen functie
from .models import SensorLog  # Zorg ervoor dat de SensorLog goed is geïmporteerd voor database opslag

# Als je Django ORM gebruikt in een async context
database_sync_to_async = sync_to_async

class MyAsyncConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accepteer de WebSocket-verbinding
        await self.accept()
        self.send_data = True
        # Start een achtergrondtaak die sensor data verstuurt
        asyncio.create_task(self.send_sensor_data())

    async def disconnect(self, close_code):
        # Stop met het verzenden van data als de WebSocket verbinding wordt verbroken
        self.send_data = False

    async def send_sensor_data(self):
        while self.send_data:
            # Haal de laatste sensor data op
            data = get_sensor_data()

            # Data opslaan in de database
            await database_sync_to_async(SensorLog.objects.create)(
                ph=data['ph'],
                temperature=data['temperature'],
                water_level_aquarium_cm=data['water_levels']['aquarium']['cm'],
                water_level_filterbak_cm=data['water_levels']['filterbak']['cm']
            )

            # Data verzenden via WebSocket
            await self.send(text_data=json.dumps(data))

            # Wacht een seconde voordat we de volgende set gegevens sturen
            await asyncio.sleep(1)

