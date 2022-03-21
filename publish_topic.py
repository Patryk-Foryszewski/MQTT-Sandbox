import paho.mqtt.client as mqtt
from random import uniform
import time

import settings
from logger import get_logger

log = get_logger(name="PUBLISH")

if __name__ == "__main__":
    mqtt_broker = settings.BROKER

    client = mqtt.Client("Temperature_Inside")
    client.connect(mqtt_broker)
    log.info(f"START PUBLISHING DATA {settings.TOPIC}")

    for _ in range(35):
        rand_number = uniform(20.0, 21.0)
        client.publish(settings.TOPIC, rand_number)
        log.info(f"PUBLISHED {rand_number} TO TOPIC {settings.TOPIC} ON {settings.BROKER}")
        time.sleep(1)
