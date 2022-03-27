from prog import args
import os
TOPIC = "TEMPERATURE_Qu4e"

BROKERS = [
    "iot.eclipse.org",
    "mqtt.eclipseprojects.io",
    "broker.hivemq.com",
    "127.0.0.1"
]

BROKER = args.broker or os.environ.get('BROKER_DOMAIN')

LOGGER_DIR = "Logs"
LOGGER_FILE = f"{LOGGER_DIR}/mqtt_logger.log"
LOGGER_FORMAT = '%(asctime)s | %(name)s | %(message)s'
LOGGER_CONSOLE = False

PLAY_TIME = 600

TIME_INTERVAL = args.interval or 1

TRANSPORT = args.transport or 'tcp'

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file': {
            'level': "DEBUG",
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': f'{LOGGER_DIR}/log.log'
        }
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'] if args.print_logs else [],
            'level': 'WARNING',
            'propagate': False
        },
        'mqtt.clients': {
            'handlers': ['default', 'file'] if args.print_logs else ['file'],
            'level': 'DEBUG',
            'propagate': False
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default', 'file'] if args.print_logs else ['file'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
