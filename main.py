import asyncio
import websockets
import paho.mqtt.client as mqtt
import json
from datetime import datetime

# MQTT Broker settings
MQTT_BROKER = "broker.hivemq.com"  # Public broker, replace with your own if needed
MQTT_PORT = 1883
MQTT_TOPIC = "render/messages"

# MQTT Client setup
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message published with mid: {mid}")

mqtt_client.on_connect = on_connect
mqtt_client.on_publish = on_publish
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.loop_start()  # Start the loop to process MQTT messages

# WebSocket handler
async def handle_message(websocket, path):
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            
            # Prepare data to send via MQTT
            data = {
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
            
            # Publish to MQTT
            mqtt_client.publish(MQTT_TOPIC, json.dumps(data))
            await websocket.send(f"Echo: {message} - Sent to MQTT")
    except websockets.ConnectionClosed:
        print("Client disconnected")

# Start WebSocket server
async def main():
    server = await websockets.serve(
        handle_message,
        "0.0.0.0",  # Listen on all interfaces
        5000        # Port (Render will override with $PORT if set in environment)
    )
    print("WebSocket server started on port 8000")
    await server.wait_closed()

# Run the server
if __name__ == "__main__":
    asyncio.run(main())
