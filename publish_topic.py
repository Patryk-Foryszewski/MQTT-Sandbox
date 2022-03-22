import paho.mqtt.client as mqtt
from random import uniform
import time

import settings
from events import Subject, Observer
from random import randrange
from typing import List
# from logger import get_logger
#
# log = get_logger(name="PUBLISH")
#
# if __name__ == "__main__":
#     mqtt_broker = settings.BROKER
#
#     client = mqtt.Client("Temperature_Inside")
#     client.connect(mqtt_broker)
#     log.info(f"START PUBLISHING DATA {settings.TOPIC}")
#
#     for _ in range(35):
#         rand_number = uniform(20.0, 21.0)
#         client.publish(settings.TOPIC, rand_number)
#         log.info(f"PUBLISHED {rand_number} TO TOPIC {settings.TOPIC} ON {settings.BROKER}")
#         time.sleep(1)


class Publisher(Subject):
    message: str = ""

    _observers: List[Observer] = []
    """
    List of subscribers. In real life, the list of subscribers can be stored
    more comprehensively (categorized by event type, etc.).
    """
    def __init__(self, client):
        self.client = client

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:

        for observer in self._observers:
            observer.update(self)

    def publish_temperature(self, temperature):
        self.client.publish(settings.TOPIC, temperature)
        self.message = f"PUBLISHED {temperature} TO TOPIC {settings.TOPIC} ON {settings.BROKER}"
        self.notify()
