# import project root path
import hashlib
import sys
import os
import csv
from typing import List, Dict, Any

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
)

import pymysql
from src.utils.mysql_utils import fetch_result, batch_insert
from datetime import datetime


def parse_datetime(datetime_str: str) -> datetime:
    """Parse datetime string from CSV to datetime object"""
    if not datetime_str:
        return None
    try:
        # Parse format like "01-06-2025 08:36:40 UTC"
        return datetime.strptime(datetime_str, "%d-%m-%Y %H:%M:%S UTC")
    except ValueError:
        try:
            # Parse ISO format like "2025-06-01T08:36:40Z"
            return datetime.strptime(datetime_str.replace('Z', '+00:00'), "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None)
        except ValueError:
            return None


def parse_csv_row(row: Dict[str, str]) -> List[Any]:
    """Parse a CSV row and return data for database insertion"""
    url = row.get('url', '').strip()
    url_sha256 = hashlib.sha256(url.encode()).hexdigest()
    
    # Parse boolean field
    is_spear = row.get('is_spear', '').strip().lower() == 'true'
    
    # Parse datetime fields
    discover_time = parse_datetime(row.get('discover_time', '').strip())
    isotime = parse_datetime(row.get('isotime', '').strip())
    
    return [
        url,                                          # url
        url_sha256,                                   # url_sha256
        row.get('brand', '').strip() or None,         # brand
        row.get('ip', '').strip() or None,           # ip_address
        row.get('asn', '').strip() or None,          # asn
        row.get('asn_name', '').strip() or None,     # asn_name
        row.get('country_code', '').strip() or None, # country_code
        row.get('country_name', '').strip() or None, # country_name
        row.get('tld', '').strip() or None,          # tld
        discover_time,                               # discover_time
        row.get('family_id', '').strip() or None,    # family_id
        row.get('host', '').strip() or None,         # host
        isotime,                                     # isotime
        row.get('page_language', '').strip() or None, # page_language
        row.get('ssl_cert_issued_by', '').strip() or None, # ssl_cert_issued_by
        row.get('ssl_cert_issued_to', '').strip() or None, # ssl_cert_issued_to
        row.get('ssl_cert_serial', '').strip() or None,   # ssl_cert_serial
        is_spear,                                    # is_spear
        row.get('sector', '').strip() or None,       # sector
    ]


def get_latest_url_from_db(mysql_conn) -> str:
    """Get the latest URL from database based on highest ID"""
    result = fetch_result(
        mysql_conn,
        "SELECT url FROM phishing_intelligence.openphish_academic ORDER BY id DESC LIMIT 1"
    )
    return result['url'] if result else None


def read_csv_data(csv_file_path: str) -> List[Dict[str, str]]:
    """Read CSV data from file"""
    data = []
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data


def find_new_data(csv_data: List[Dict[str, str]], latest_url: str) -> List[Dict[str, str]]:
    """Find new data that should be inserted into database"""
    if not latest_url:
        # If no latest URL, insert all data in reverse order
        return csv_data[::-1]
    
    # Find the index of latest URL in CSV data
    for i, row in enumerate(csv_data):
        if row.get('url', '').strip() == latest_url:
            # Return data before this URL, in reverse order
            return csv_data[:i][::-1]
    
    # If latest URL not found, insert all data in reverse order
    return csv_data[::-1]


def fetch_openphish_academic_intelligence(args=None):
    """Main function to fetch OpenPhish Academic intelligence"""
    
    # Connect to mysql
    mysql_conn = pymysql.connect(
        host=args.host,
        user=args.user,
        password=args.password,
        port=args.port,
        cursorclass=pymysql.cursors.DictCursor,
    )

    try:
        # Path to the CSV file (should be cloned by GitHub Actions)
        csv_file_path = "academic/feed.csv"
        
        if not os.path.exists(csv_file_path):
            print(f"Error: CSV file not found at {csv_file_path}")
            return
        
        # Read CSV data
        csv_data = read_csv_data(csv_file_path)
        print(f"Read {len(csv_data)} rows from CSV file")
        
        # Get latest URL from database
        latest_url = get_latest_url_from_db(mysql_conn)
        print(f"Latest URL in database: {latest_url}")
        
        # Find new data to insert
        new_data_rows = find_new_data(csv_data, latest_url)
        print(f"Found {len(new_data_rows)} new rows to insert")
        
        if not new_data_rows:
            print("No new data to insert")
            return
        
        # Parse data for database insertion
        batch_insert_data = []
        for row in new_data_rows:
            try:
                parsed_data = parse_csv_row(row)
                batch_insert_data.append(parsed_data)
            except Exception as e:
                print(f"Error parsing row {row}: {e}")
                continue
        
        if batch_insert_data:
            # Insert data into database
            sql = """
            INSERT IGNORE INTO phishing_intelligence.openphish_academic 
            (url, url_sha256, brand, ip_address, asn, asn_name, country_code, country_name, 
             tld, discover_time, family_id, host, isotime, page_language, ssl_cert_issued_by, 
             ssl_cert_issued_to, ssl_cert_serial, is_spear, sector) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            fetch_time = datetime.now()
            affected_rows = batch_insert(mysql_conn, sql, batch_insert_data)
            print(f"Successfully fetched OpenPhish Academic intelligence on {fetch_time} with {affected_rows} new URLs")
        else:
            print("No valid data to insert after parsing")
            
    except Exception as e:
        print(f"Error processing OpenPhish Academic intelligence: {e}")
    finally:
        mysql_conn.close()
