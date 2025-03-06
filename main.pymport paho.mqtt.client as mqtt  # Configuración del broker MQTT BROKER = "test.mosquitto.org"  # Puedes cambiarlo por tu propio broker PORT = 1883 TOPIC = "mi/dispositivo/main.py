import paho.mqtt.client as mqtt
import time

# Configuración del broker MQTT (cambiado a HiveMQ)
BROKER = "broker.hivemq.com"  # Broker público de HiveMQ
PORT = 1883
TOPIC = "mi/dispositivo/valor"

# Variable global para el cliente MQTT
client = None

# Función para conectarse al broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT")
    else:
        print(f"Error de conexión con código {rc}")

# Inicializar y conectar el cliente MQTT
def init_mqtt():
    global client
    client = mqtt.Client()
    client.on_connect = on_connect
    try:
        client.connect(BROKER, PORT, 60)
        client.loop_start()  # Inicia el loop en un hilo separado
    except Exception as e:
        print(f"No se pudo conectar al broker: {e}")
        return False
    return True

# Función para publicar un valor en MQTT
def publish_value(value):
    if client is None or not client.is_connected():
        print("Cliente MQTT no conectado. Intentando reconectar...")
        if not init_mqtt():
            return False
    try:
        result = client.publish(TOPIC, str(value))
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Valor '{value}' publicado en {TOPIC}")
            return True
        else:
            print(f"Error al publicar: {result.rc}")
            return False
    except Exception as e:
        print(f"Error al publicar el valor: {e}")
        return False

# Función de automatización que recibe un valor y lo publica
def make_automatization(value):
    return publish_value(value)

# Ejemplo de uso
if _name_ == "_main_":
    # Inicializar conexión MQTT
    if init_mqtt():
        # Bucle principal para prueba manual
        while True:
            valor = input("Ingrese un valor para enviar a MQTT (o 'salir' para terminar): ")
            if valor.lower() == "salir":
                break
            # Usar la función make_automatization para publicar
            make_automatization(valor)
        
        # Detener el loop y desconectar
        client.loop_stop()
        client.disconnect()
        print("Desconectado de MQTT")
    else:
        print("No se pudo iniciar el programa debido a problemas de conexión."
