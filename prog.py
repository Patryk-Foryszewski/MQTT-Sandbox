import argparse

parser = argparse.ArgumentParser(description='Play with MQTT Clients.')
parser.add_argument("-t", "--time", type=int,  help="Play for given time (seconds)")
parser.add_argument("-i", "--interval", type=int, help="Publish to topic in given interval")
args = parser.parse_args()

# parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')
#
# args = parser.parse_args()
# print(args.accumulate(args.integers))