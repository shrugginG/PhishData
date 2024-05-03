import argparse
from modules.phishing_intelligence.fetch_phishtank import fetch_phishtank_intelligence

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch github action secerets")
    parser.add_argument("--host", required=True, help="Database host")
    parser.add_argument("--user", required=True, help="Database user")
    parser.add_argument("--password", required=True, help="Database password")
    parser.add_argument("--port", type=int, required=True, help="Database port")
    parser.add_argument("--phishtank_token", required=False, help="Phishtank token")
    return parser.parse_args()


if __name__ == "__main__":

    # Parse arguments
    args = parse_args()

    fetch_phishtank_intelligence(args)