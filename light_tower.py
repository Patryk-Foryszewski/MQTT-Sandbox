from mqtt.clients import Publisher, Subscriber
from mqtt import settings
import sched
import time
from datetime import datetime
from prog import args
from mqtt.observers import StickerStatusObserver
import logging
from logging.config import dictConfig
dictConfig(settings.LOGGING_CONFIG)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Get input arguments or set defaults
    interval = args.interval or settings.TIME_INTERVAL
    play_time = args.time or settings.PLAY_TIME
    broker = args.broker or settings.BROKER
    # broker = socket.gethostbyname('broker')

    data = {
        "topic": "PROD_LINE_1",
        "broker": broker
    }
    logger.info(f'## START SESSION TO BROKER {data["broker"]} ON TOPIC {data["topic"]}  ##')
    subscriber_1 = Subscriber(client_name="light_tower_1", **data)

    observer = StickerStatusObserver()
    subscriber_1.attach(observer)

    subscriber_1.start()

    time_start = datetime.now()
    s = sched.scheduler(time.time, time.sleep)

    def wait(sc):
        delta = datetime.now() - time_start
        if delta.total_seconds() < play_time:
            s.enter(interval, 0, wait, (sc,))

    wait(s)
    s.run()
    subscriber_1.stop()

