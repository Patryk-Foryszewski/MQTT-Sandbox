from clients import Publisher, Subscriber
import settings
import sched
import time
from datetime import datetime
from random import uniform
from prog import args

from logging.config import dictConfig

dictConfig(settings.LOGGING_CONFIG)


if __name__ == "__main__":
    # Get input arguments or set defaults
    interval = args.interval or settings.TIME_INTERVAL
    play_time = args.time or settings.PLAY_TIME
    broker = args.broker or settings.BROKER

    data = {
        "topic": settings.TOPIC,
        "broker": broker
    }

    # subscriber_1 = Subscriber(client_name="smartphone_1", **data)
    # subscriber_1.start()
    #
    # subscriber_2 = Subscriber(client_name="smartphone_2", **data)
    # subscriber_2.start()

    publisher = Publisher(client_name="temperature_inside", **data)
    publisher.start()

    time_start = datetime.now()
    s = sched.scheduler(time.time, time.sleep)


    def i_am_publishing(sc):
        value = uniform(20.0, 21.0)
        publisher.publish(value)
        delta = datetime.now() - time_start
        if delta.total_seconds() < play_time:
            s.enter(interval, 0, i_am_publishing, (sc,))

    i_am_publishing(s)
    s.run()
    publisher.stop()
    # subscriber_1.stop()
    # subscriber_2.stop()
