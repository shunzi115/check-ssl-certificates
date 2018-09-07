#!/usr/bin/python
import socket
import ssl
import datetime
import argparse

def ssl_expiry_datetime(hostname):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
        )
    # 3 second timeout because Lambda has runtime limitations
    conn.settimeout(3.0)

    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    # parse the string from the certificate into a Python datetime object
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)

def ssl_valid_time_remaining(hostname):
    """Get the number of days left in a cert's lifetime."""
    expires = ssl_expiry_datetime(hostname)
    return expires - datetime.datetime.utcnow()


parser = argparse.ArgumentParser(description='returns the time before expiration of certificate')
parser.add_argument("-c","--hostname", help="hostname of the certificate you want to check")
args = parser.parse_args()

expire = ssl_valid_time_remaining(args.hostname)
print int(round(datetime.timedelta.total_seconds(expire), 0))
