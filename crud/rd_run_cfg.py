from argparse import ArgumentParser
from urllib.parse import urlparse
import logging

from ncclient import manager

if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("device",
                        help="NETCONF device (ssh://user:password@host:port)")
    args = parser.parse_args()
    device = urlparse(args.device)

    with manager.connect(
            host=device.hostname,
            port=device.port,
            username=device.username,
            password=device.password,
            hostkey_verify=False,
            device_params={'name': 'iosxr'}
    ) as m:
        reply = m.get_config(source='running').data_xml

        with open("../running.xml", 'w') as f:
            f.write(reply)
