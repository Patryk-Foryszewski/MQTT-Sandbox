import argparse

parser = argparse.ArgumentParser(description='Play with MQTT Clients.')
parser.add_argument("-t", "--time", type=int,  help="Play for given time (seconds).")
parser.add_argument("-i", "--interval", type=int, help="Publish to topic in given interval.")
parser.add_argument("-b", "--broker", type=str, help="Set the MQTT Broker.")
parser.add_argument("-p", "--port", type=str, help="Set the MQTT Broker Port.")
parser.add_argument("-pl", "--print_logs", type=bool, help="Print logs to the console. Defaults to False.")
parser.add_argument("-tr", "--transport", type=str, help="Set transport. Defaults to tcp.", choices=['tcp', 'websockets'])
args = parser.parse_args()
