import paho.mqtt.client as mqtt
from events import Subject, Observer
from typing import List


class Subscriber(Subject):
    message: str = ""
    severity = 'info'
    _observers: List[Observer] = None
    received: int = 0

    def __init__(self, client_name, topic, broker):
        self.client_name = client_name
        self.topic = topic
        self.broker = broker
        self.client = mqtt.Client(self.client_name)
        self.client.connect(self.broker)
        self.set_messanger()
        self.client.subscribe(topic)
        self._observers = []
        self.start()

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def on_message(self, _client, userdata, message):
        self.received += 1
        self.message = f"RECEIVED MESSAGE NR: {self.received} {str(message.payload.decode('utf-8'))}"
        self.notify()

    def set_messanger(self):
        self.client.on_message = self.on_message

    def start(self):
        self.client.loop_start()
        self.message = f"STOPPED SUBSCRIPTION AFTER {self.received} MESSAGES"
        self.notify()

    def stop(self):
        self.client.loop_stop()
        self.message = f"STARTED SUBSCRIPTION AFTER {self.received} MESSAGES"
        self.notify()
