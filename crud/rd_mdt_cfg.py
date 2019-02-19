from argparse import ArgumentParser
from urllib.parse import urlparse

from ncclient import manager

if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("device",
                        help="NETCONF device (ssh://user:password@host:port)")
    args = parser.parse_args()
    device = urlparse(args.device)

    filter_tag = '''
    <filter>
    <telemetry-model-driven xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-telemetry-model-driven-cfg"/>
    </filter>
    '''

    with manager.connect(
            host=device.hostname,
            port=device.port,
            username=device.username,
            password=device.password,
            hostkey_verify=False,
            device_params={'name': 'iosxr'}
    ) as m:
        reply = m.get_config(source='running',
                             filter=filter_tag).data_xml

        with open("../running_mdt.xml", 'w') as f:
            f.write(reply)
