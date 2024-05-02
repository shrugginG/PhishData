import argparse

from modules.phishing_intelligence.fetch_openphish import fetch_openphish_intelligence

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch github action secerets")
    parser.add_argument("--host", required=True, help="Database host")
    parser.add_argument("--user", required=True, help="Database user")
    parser.add_argument("--password", required=True, help="Database password")
    parser.add_argument("--port", type=int, required=True, help="Database port")
    return parser.parse_args()


if __name__ == "__main__":
    # get_openphish_feed()

    # Parse arguments
    args = parse_args()

    fetch_openphish_intelligence(args)
