TOPIC = "TEMPERATURE_Qu4e"

BROKERS = [
    "iot.eclipse.org",
    "mqtt.eclipseprojects.io",
    "broker.hivemq.com",
    "127.0.0.1"
]

BROKER = BROKERS[3]

LOGGER_DIR = "Logs"
LOGGER_FILE = f"{LOGGER_DIR}/mqtt_logger.log"
LOGGER_FORMAT = '%(asctime)s | %(name)s | %(message)s'
LOGGER_LEVEL = 10  # DEBUG
LOGGER_CONSOLE = False

