from server import server
import argparse

LOCATION_FILE = "locations.json"

parser = argparse.ArgumentParser()
parser.add_argument("ip", type=int, nargs=1)
parser.add_argument("port", type=int, nargs=1)
parser.add_argument("channel", type=str, nargs=1)

if __name__ == "__main__":
    args = parser.parse_args()
    server(args.ip, args.port, args.channel, LOCATION_FILE).run()
