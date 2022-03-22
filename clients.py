from events import Subject
import paho.mqtt.client as mqtt
from events import Subject, Observer
from typing import List


class BaseClient(Subject):
    """
    Docstring under construction.
    Thoughts to be organized:
    1. If you need to log messages with severity different to
        'INFO' set Publisher instance severity according to requirements i.e.
        'warning'
        'error'
        Notice that above are not logging levels like logging.DEBUG
        but logger methods names. This idea is to be discussed.

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


class Publisher(BaseClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def publish(self, value):
        self.client.publish(self.topic, value)
        self.message = f"PUBLISHED {value} TO TOPIC {self.topic} ON {self.broker}"
        self.notify()


class Subscriber(BaseClient):
    received: int = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_messanger()
        self.client.subscribe(self.topic)
        self.start()

    def on_message(self, _client, userdata, message):
        self.received += 1
        self.message = f"RECEIVED MESSAGE NR: {self.received} {str(message.payload.decode('utf-8'))}"
        self.notify()

    def set_messanger(self):
        self.client.on_message = self.on_message

    def start(self):
        self.client.loop_start()
        self.message = f"STARTED SUBSCRIPTION to {self.topic}"
        self.notify()

    def stop(self):
        self.client.loop_stop()
        self.message = f"STOPPED SUBSCRIPTION AFTER {self.received} MESSAGES"
        self.notify()
