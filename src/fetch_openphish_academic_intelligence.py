import argparse

from modules.phishing_intelligence.fetch_openphish_academic import fetch_openphish_academic_intelligence


def parse_args():
    parser = argparse.ArgumentParser(description="Fetch OpenPhish Academic Intelligence")
    parser.add_argument("--host", required=True, help="Database host")
    parser.add_argument("--user", required=True, help="Database user")
    parser.add_argument("--password", required=True, help="Database password")
    parser.add_argument("--port", type=int, required=True, help="Database port")
    return parser.parse_args()


def main():

    # Parse arguments
    args = parse_args()

    # Fetch openphish academic phishing intelligence
    fetch_openphish_academic_intelligence(args)


if __name__ == "__main__":
    main()
