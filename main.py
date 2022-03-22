from clients import Publisher, Subscriber
import settings
import sched
import time
from datetime import datetime
from random import uniform
from loggers import Logger
from prog import args

print('ARGS', args)

if __name__ == "__main__":
    data = {
        "topic": settings.TOPIC,
        "broker": settings.BROKER
    }

    subscriber = Subscriber(client_name="smartphone", **data)
    subscriber_logger = Logger(
        name="SUBSCRIBER",
        file="subscriber"
    )
    subscriber.attach(subscriber_logger)
    # subscriber.client.on_message = subscriber.on_message

    publisher = Publisher(client_name="temperature_inside", **data)
    publisher_logger = Logger(
        name="PUBLISHER",
        file="publisher"
    )
    publisher.attach(publisher_logger)
    time_start = datetime.now()
    s = sched.scheduler(time.time, time.sleep)

    interval = args.interval or settings.TIME_INTERVAL
    play_time = args.time or settings.PLAY_TIME

    def i_am_publishing(sc):
        value = uniform(20.0, 21.0)
        publisher.publish(value)
        delta = datetime.now() - time_start
        if delta.total_seconds() < play_time:
            s.enter(interval, 0, i_am_publishing, (sc,))

    i_am_publishing(s)
    s.run()
    subscriber.stop()
