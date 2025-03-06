import paho.mqtt.client as mqtt

# Configuración del broker MQTT (igual que el emisor)
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "mi/dispositivo/valor"

# Función que se ejecuta al recibir un mensaje
def on_message(client, userdata, msg):
    mensaje = msg.payload.decode("utf-8")  # Decodifica el mensaje recibido
    print(f"Mensaje recibido en {msg.topic}: {mensaje}")

# Función que se ejecuta al conectar
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT")
        client.subscribe(TOPIC)  # Suscribirse al tópico
    else:
        print(f"Error de conexión con código {rc}")

# Crear cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Conectar al broker
client.connect(BROKER, PORT, 60)
client.loop_start()  # Inicia el loop para escuchar mensajes

# Mantener el programa corriendo
try:
    while True:
        pass  # Mantener el script activo para recibir mensajes
except KeyboardInterrupt:
    print("\nDesconectando...")
    client.loop_stop()
    client.disconnect()
