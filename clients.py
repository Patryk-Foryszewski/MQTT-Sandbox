import paho.mqtt.client as mqtt
from events import Subject, Observer
from typing import List
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class BaseClient(Subject):

    message: str = ""
    _observers: List[Observer] = None
    messages = {  # return code: log_message
        0: "CONNECTION SUCCESSFUL",
        1: "CONNECTION REFUSED – incorrect protocol version",
        2: "CONNECTION REFUSED – invalid client identifier",
        3: "CONNECTION REFUSED – server unavailable",
        4: "CONNECTION REFUSED – bad username or password",
        5: "CONNECTION REFUSED – not authorised",
    }
    messages = defaultdict(lambda: "RETURN CODE NOT SUPPORTED", messages)

    def __init__(self, client_name: str, topic: str, broker: str):
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
        logger.info(f"CONNECTION FROM {self.client_name} TO {self.topic} FAILED")

    def connect(self):
        logger.info(f"{self.client_name} CONNECTING TO {self.broker} ON {self.broker}")
        try:
            self.client.connect(self.broker)
        except Exception as ex:
            logger.exception(f"FAILED TO CONNECT {ex}",)
            return False
        else:
            return True

    def start(self):
        self.client.on_connect_fail = self.connect_fail
        self.client.on_connect = self.on_connect
        self.connect()

    def stop(self):
        self.client.loop_stop()

    def on_connect(self, client, userdata, flags, rc):
        logger.info(f'CLIENT {self.client_name} ESTABLISH CONNECTION MESSAGE {self.messages[rc]}')


class Publisher(BaseClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_publish(self, client, userdata, ):
        print("ON PUBLISH", args)

    def publish(self, value: str):
        rc,  = self.client.publish(self.topic, value)
        print("PUBLISHED", published)
        logger.info(f"{self.client_name} PUBLISHED {value}")

    def start(self):
        super(Publisher, self).start()
        self.client.on_publish = self.on_publish

    def stop(self):
        super().stop()
        logger.info(f"PUBLISHER {self.client_name} STOPPED PUBLISHING")


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
        super().stop()
        logger.info(f"STOPPED SUBSCRIPTION AFTER {self.received} MESSAGES")
