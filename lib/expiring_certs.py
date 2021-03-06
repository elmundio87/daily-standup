import socket
import ssl
import datetime
import json
from config import expiring_certs_config as config
from pyasn1_modules import pem, rfc2459
from pyasn1.codec.der import decoder as der_decoder
from retrying import retry


def get_expiring_certs(board_name):
    output = []
    if board_name in config.sites.keys():
        for host in config.sites[board_name]:
            output.append(ssl_output_item(host))
    output = sorted(output, key=lambda k: k.get('days_remaining', 0))
    return json.dumps(output)


def ssl_output_item(hostname):
    expire_date, error = ssl_expiry_datetime(hostname)
    return {"hostname": hostname,
            "days_remaining": ssl_valid_time_remaining(hostname),
            "notAfter": "{:%B %d, %Y}".format(expire_date),
            "error": error}


@retry(stop_max_attempt_number=4)
def ssl_expiry_datetime(hostname):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    try:
        pem_cert = ssl.get_server_certificate((hostname, 443))
        der_cert = ssl.PEM_cert_to_DER_cert(pem_cert)
        cert = der_decoder.decode(der_cert, asn1Spec=rfc2459.Certificate())[0]
        tbs = cert.getComponentByName('tbsCertificate')
        validity = tbs.getComponentByName('validity')
        not_after = validity.getComponentByName('notAfter').getComponent()
        return datetime.datetime.strptime(str(not_after), '%y%m%d%H%M%SZ'), ""
    except Exception, e:
        return datetime.datetime.now(), str(e)


def ssl_valid_time_remaining(hostname):
    """Get the number of days left in a cert's lifetime."""
    expires, error = ssl_expiry_datetime(hostname)

    return (expires - datetime.datetime.utcnow()).days
