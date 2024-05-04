import argparse
from modules.phishing_intelligence.fetch_ecrimex import dump_latest_ecrimex_phish_intelligence_into_mysql

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch github action secerets")
    parser.add_argument("--host", required=True, help="Database host")
    parser.add_argument("--user", required=True, help="Database user")
    parser.add_argument("--password", required=True, help="Database password")
    parser.add_argument("--port", type=int, required=True, help="Database port")
    parser.add_argument("--ecrimex_token", required=True, help="eCrimeX token")
    return parser.parse_args()

def main():
    args = parse_args()
    dump_latest_ecrimex_phish_intelligence_into_mysql(args)

if __name__ == "__main__":

    main()