from server import server
import argparse

LOCATION_FILE = "locations.json"

parser = argparse.ArgumentParser()
parser.add_argument("ip", type=str, nargs=1)
parser.add_argument("port", type=int, nargs=1)
parser.add_argument("channel", type=str, nargs=1)

def main():
    args = parser.parse_args()
    server(args.ip[0], args.port[0], args.channel[0], LOCATION_FILE).run()
