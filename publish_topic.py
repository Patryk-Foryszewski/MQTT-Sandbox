import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

TOPIC = "TEMPERATURE_Qu4e"
BROKERS = [
    "iot.eclipse.org",
    "mqtt.eclipseprojects.io",
    "broker.hivemq.com",
    "127.0.0.1"
]
BROKER = BROKERS[3]
PORT = 1833

if __name__ == "__main__":
    mqtt_broker = BROKER

    client = mqtt.Client("Temperature_Inside")
    client.connect(mqtt_broker)

    print(f"PUBLISH DATA {TOPIC}")
    for _ in range(35):
        rand_number = uniform(20.0, 21.0)
        client.publish(TOPIC, rand_number)
        print(f"Just published {rand_number} to topic {TOPIC} on {BROKER}")
        time.sleep(1)
