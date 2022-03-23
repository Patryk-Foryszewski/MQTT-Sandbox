import argparse

parser = argparse.ArgumentParser(description='Play with MQTT Clients.')
parser.add_argument("-t", "--time", type=int,  help="Play for given time (seconds)")
parser.add_argument("-i", "--interval", type=int, help="Publish to topic in given interval")
parser.add_argument("-b", "--broker", type=str, help="Set the MQTT Broker")
args = parser.parse_args()
