mport paho.mqtt.client as mqtt

# Configuración del broker MQTT
BROKER = "test.mosquitto.org"  # Puedes cambiarlo por tu propio broker
PORT = 1883
TOPIC = "mi/dispositivo/valor"

# Función para conectarse al broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT")
    else:
        print(f"Error de conexión con código {rc}")

# Crear cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect

# Conectar al broker
client.connect(BROKER, PORT, 60)

# Publicar un valor
while True:
    valor = input("Ingrese un valor para enviar a MQTT (o 'salir' para terminar): ")
    if valor.lower() == "salir":
        break
    client.publish(TOPIC, valor)
    print(f"Valor '{valor}' publicado en {TOPIC}")

# Cerrar conexión
client.disconnect()
print("Desconectado de MQTT")
