import paho.mqtt.client as mqtt
import time
import settings
from logger import get_logger

log = get_logger(name="SUBSCRIBE")
log.info(f"SUBSCRIBED TO TOPIC {settings.TOPIC}")

received = 0


def on_message(_client, userdata, message):
    global received
    received += 1
    log.info(f"RECEIVED MESSAGE NR: {received} {str(message.payload.decode('utf-8'))}")


if __name__ == "__main__":
    mqttBroker = settings.BROKER

    client = mqtt.Client("Smartphone")
    client.connect(mqttBroker)

    client.loop_start()

    client.subscribe(settings.TOPIC)
    client.on_message = on_message

    time.sleep(30)
    client.loop_stop()
