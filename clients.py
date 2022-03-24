from events import Subject
import paho.mqtt.client as mqtt
from events import Subject, Observer
from typing import List
import logging

logger = logging.getLogger(__name__)


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
    _observers: List[Observer] = None
    messages = {
        0: "CONNECTION SUCCESSFUL",
        1: "CONNECTION REFUSED – incorrect protocol version",
        2: "CONNECTION REFUSED – invalid client identifier",
        3: "CONNECTION REFUSED – server unavailable",
        4: "CONNECTION REFUSED – bad username or password",
        5: "CONNECTION REFUSED – not authorised",
    }

    def __init__(self, client_name, topic, broker):
        self.client_name = client_name
        self.topic = topic
        self.broker = broker
        self.client = mqtt.Client(self.client_name)
        self._observers = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def connect_fail(self, *args, **kwargs):
        logger.info(f"CONNECTION FAILED  {self.topic}")

    def log(self, message, severity='info'):
        self.message = message
        self.severity = severity
        self.notify()

    def start(self):
        self.client.on_connect_fail = self.connect_fail
        self.client.connect(self.broker)
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        connack_message = self.messages.get(rc, f"ERROR CODE {rc} NOT SUPPORTED")
        logger.info(f'CLIENT {client.cliend_id} ESTABLISH CONNECTION MESSAGE {connack_message}')


class Publisher(BaseClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def publish(self, value):
        self.client.publish(self.topic, value)
        logger.info(f"PUBLISHED {value} TO TOPIC {self.topic} ON {self.broker}")


class Subscriber(BaseClient):
    received: int = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_message(self, _client, userdata, message):
        self.received += 1
        logger.info(f"RECEIVED MESSAGE NR: {self.received} {str(message.payload.decode('utf-8'))}")

    def start(self):
        super().start()
        self.client.on_message = self.on_message
        self.client.subscribe(self.topic)
        self.client.loop_start()
        logger.info(f"STARTING SUBSCRIPTION to {self.topic}")

    def stop(self):
        self.client.loop_stop()
        logger.info(f"STOPPED SUBSCRIPTION AFTER {self.received} MESSAGES")
