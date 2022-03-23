from clients import Publisher, Subscriber
import settings
import sched
import time
from datetime import datetime
from random import uniform
from loggers import Logger
from prog import args


if __name__ == "__main__":
    # Get input arguments or set defaults
    interval = args.interval or settings.TIME_INTERVAL
    play_time = args.time or settings.PLAY_TIME
    broker = args.broker or settings.BROKER

    data = {
        "topic": settings.TOPIC,
        "broker": broker
    }

    subscriber = Subscriber(client_name="smartphone", **data)
    subscriber_logger = Logger(
        name="SUBSCRIBER",
        file="subscriber"
    )
    subscriber.attach(subscriber_logger)

    publisher = Publisher(client_name="temperature_inside", **data)
    publisher_logger = Logger(
        name="PUBLISHER",
        file="publisher"
    )
    publisher.attach(publisher_logger)
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
    subscriber.stop()
