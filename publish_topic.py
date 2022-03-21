import paho.mqtt.client as mqtt
from random import uniform
import time

import settings


if __name__ == "__main__":
    mqtt_broker = settings.BROKER

    client = mqtt.Client("Temperature_Inside")
    client.connect(mqtt_broker)

    print(f"PUBLISH DATA {settings.TOPIC}")
    for _ in range(35):
        rand_number = uniform(20.0, 21.0)
        client.publish(settings.TOPIC, rand_number)
        print(f"Just published {rand_number} to topic {settings.TOPIC} on {settings.BROKER}")
        time.sleep(1)
