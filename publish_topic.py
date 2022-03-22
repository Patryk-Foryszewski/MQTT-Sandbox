import paho.mqtt.client as mqtt
from events import Subject, Observer
from typing import List


class Publisher(Subject):
    """
    Docstring under construction.
    Thoughts to be organized:
    1. If you need to log messages with severity different to
        'INFO' set Publisher instance severity according to requirements i.e.
        'warning'
        'logging'
        Notice that above are not logging levels like logging.DEBUG
        but logger methods names.

    """
    message: str = ""
    severity = 'info'
    _observers: List[Observer] = None

    def __init__(self, client_name, topic, broker):
        self.client_name = client_name
        self.topic = topic
        self.broker = broker
        self.client = mqtt.Client(self.client_name)
        self.client.connect(self.broker)
        self._observers = []

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
