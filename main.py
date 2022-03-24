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

    subscriber = Subscriber(client_name="smartphone_1", **data)
    subscriber_logger = Logger(
        name="SUBSCRIBER",
        file=f"subscriber_{subscriber.client_name}"
    )
    subscriber.attach(subscriber_logger)

    subscriber_2 = Subscriber(client_name="smartphone_2", **data)
    subscriber_logger_2 = Logger(
        name="SUBSCRIBER_2",
        file=f"subscriber_{subscriber_2.client_name}"
    )
    subscriber.attach(subscriber_logger_2)
    subscriber.start()

    publisher = Publisher(client_name="temperature_inside", **data)
    publisher_logger = Logger(
        name="PUBLISHER",
        file=f"publisher_{publisher.client_name}"
    )
    publisher.attach(publisher_logger)
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
    subscriber.stop()
