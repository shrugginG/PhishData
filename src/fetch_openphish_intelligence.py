import argparse

from modules.phishing_intelligence.fetch_openphish import fetch_openphish_intelligence


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch github action secerets")
    parser.add_argument("--host", required=True, help="Database host")
    parser.add_argument("--user", required=True, help="Database user")
    parser.add_argument("--password", required=True, help="Database password")
    parser.add_argument("--port", type=int, required=True, help="Database port")
    return parser.parse_args()


def main():

    # Parse arguments
    args = parse_args()

    # Fetch openphish phishing intelligence
    # TODO - This is community feed.
    fetch_openphish_intelligence(args)

    # TODO - Fetch phishtank phishing intelligence

    # TODO - Fetch eCrimeX phishing intelligence

    # TODO - Fetch urlhaus phishing intelligence

    # TODO - Fetch certstream phishing intelligence

    # TODO - Fetch phishstats phishing intelligence

    # TODO - Fetch urlscan phishing intelligence

    # TODO - Fetch phishlabs phishing intelligence


if __name__ == "__main__":
    main()
