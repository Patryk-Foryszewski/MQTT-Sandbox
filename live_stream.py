from mqtt.clients import Publisher, Subscriber
from mqtt import settings
import sched
import time
from datetime import datetime
from prog import args
import random

import logging
from logging.config import dictConfig
dictConfig(settings.LOGGING_CONFIG)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Get input arguments or set defaults
    interval = args.interval or settings.TIME_INTERVAL
    play_time = args.time or settings.PLAY_TIME
    broker = args.broker or settings.BROKER

    data = {
        "topic": "PROD_LINE_1",
        "broker": broker
    }
    logger.info(f'## START SESSION TO BROKER {data["broker"]}')
    publisher = Publisher(client_name="CAMERA_1", **data)
    publisher.start()

    time_start = datetime.now()
    s = sched.scheduler(time.time, time.sleep)

    STICKER = 1

    def i_am_publishing(sc):
        global STICKER
        result = "DAMAGED" if random.randrange(1, 100) <= 5 else "OK"  # 5% chance the sticker is damaged
        info = f"STICKER - {STICKER} - {result}"
        publisher.publish(info)
        delta = datetime.now() - time_start
        STICKER += 1
        if delta.total_seconds() < play_time:
            s.enter(interval, 0, i_am_publishing, (sc,))

    i_am_publishing(s)
    s.run()
    publisher.stop()

