import socket
import ssl
import datetime
import json
import expiring_certs_config as config

output = []

def get_expiring_certs(board_name):
    if board_name in config.sites.keys():
        for site in config.sites[board_name]:
            output.append(ssl_output_item(site))
    return json.dumps(output)
    
def ssl_output_item(hostname):
    return {"hostname": hostname, "days_remaining": ssl_valid_time_remaining(hostname)}

def ssl_expiry_datetime(hostname):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    # 3 second timeout because Lambda has runtime limitations
    conn.settimeout(3.0)

    try:
        conn.connect((hostname, 443))
        ssl_info = conn.getpeercert()
        # parse the string from the certificate into a Python datetime object
        return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
    except:
        return datetime.datetime.now()

def ssl_valid_time_remaining(hostname):
    """Get the number of days left in a cert's lifetime."""
    expires = ssl_expiry_datetime(hostname)
    
    return (expires - datetime.datetime.utcnow()).days
