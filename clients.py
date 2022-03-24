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
        self._observers = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def connect_fail(self, *args, **kwargs):
        print('CONNECTION FAILED', args, kwargs)
        self.severity = 'exception'
        self.log(f"CONNECTION FAILED  {self.topic}", severity='exception')

    def log(self, message, severity='info'):
        self.message = message
        self.severity = severity
        self.notify()

    def start(self):
        self.client.on_connect_fail = self.connect_fail
        self.client.connect(self.broker)
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        messages = {
            0: "Connection successful",
            1: "Connection refused – incorrect protocol version",
            2: "Connection refused – invalid client identifier",
            3: "Connection refused – server unavailable",
            4: "Connection refused – bad username or password",
            5: "Connection refused – not authorised",
        }
        self.log(messages.get(rc, f"ERROR CODE {rc} NOT SUPPORTED").upper())


class Publisher(BaseClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def publish(self, value):
        self.client.publish(self.topic, value)
        self.log(f"PUBLISHED {value} TO TOPIC {self.topic} ON {self.broker}")


class Subscriber(BaseClient):
    received: int = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.subscribe(self.topic)

    def on_message(self, _client, userdata, message):
        # print(f'CLIENT {self.client_name}', type(_client), _client, self.on_message)
        # print('MORE ABUOT CLIENT', dir(_client))
        self.received += 1
        self.log(f"RECEIVED MESSAGE NR: {self.received} {str(message.payload.decode('utf-8'))}")

    def start(self):
        super().start()
        self.client.on_message = self.on_message
        self.client.loop_start()
        self.log(f"STARTED SUBSCRIPTION to {self.topic}")

    def stop(self):
        self.client.loop_stop()
        self.log(f"STOPPED SUBSCRIPTION AFTER {self.received} MESSAGES")
