import paho.mqtt.client as mqtt
import logging
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
    """
    Docstring under construction.
    Thoughts to be organized:
    1. If you need to log messages with severity different to
        'INFO' set object severity according to requirements i.e.
        'warning'
        'logging'
        Notice that above are not logging levels like logging.DEBUG
        but logger methods names.

    """
    message: str = ""
    severity = 'info'
    _observers: List[Observer] = []

    def __init__(self, client_name, topic, broker):
        self.client_name = client_name
        self.topic = topic
        self.broker = broker
        self.client = mqtt.Client(self.client_name)
        self.client.connect(self.broker)

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def publish(self, value):
        self.client.publish(self.topic, value)
        self.message = f"PUBLISHED {value} TO TOPIC {self.topic} ON {self.broker}"
        self.notify()
