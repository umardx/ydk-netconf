from argparse import ArgumentParser
from urllib.parse import urlparse

from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ifmgr_cfg \
    as xr_ifmgr_cfg
import logging


def config_interface_configurations(interface_configurations, if_name, desc, addr, mask):
    """Add config data to interface_configurations object."""
    # configure IPv4 interface
    interface_configuration = interface_configurations.InterfaceConfiguration()
    interface_configuration.active = 'act'
    interface_configuration.interface_name = if_name
    interface_configuration.description = desc

    primary = interface_configuration.ipv4_network.addresses.Primary()
    primary.address = addr
    primary.netmask = mask
    interface_configuration.ipv4_network.addresses.primary = primary
    interface_configurations.interface_configuration.append(interface_configuration)


if __name__ == "__main__":
    """Execute main program."""
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", help="print debugging messages",
                        action="store_true")
    parser.add_argument("device",
                        help="NETCONF device (ssh://user:password@host:port)")
    args = parser.parse_args()
    device = urlparse(args.device)

    # log debug messages if verbose argument specified
    if args.verbose:
        logger = logging.getLogger("ydk")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(("%(asctime)s - %(name)s - "
                                      "%(levelname)s - %(message)s"))
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create NETCONF provider
    provider = NetconfServiceProvider(address=device.hostname,
                                      port=device.port,
                                      username=device.username,
                                      password=device.password,
                                      protocol=device.scheme)
    # create CRUD service
    crud = CRUDService()

    interface_configurations = xr_ifmgr_cfg.InterfaceConfigurations()  # create object
    # add object configuration
    config_interface_configurations(interface_configurations,
                                    if_name="GigabitEthernet0/0/0/0",
                                    desc="Interface 0",
                                    addr="172.18.0.1",
                                    mask="255.255.255.252")

    config_interface_configurations(interface_configurations,
                                    if_name="GigabitEthernet0/0/0/1",
                                    desc="Interface 1",
                                    addr="172.18.1.1",
                                    mask="255.255.255.0")

    config_interface_configurations(interface_configurations,
                                    if_name="GigabitEthernet0/0/0/2",
                                    desc="Interface 2",
                                    addr="172.18.3.1",
                                    mask="255.255.255.0")

    # create configuration on NETCONF device
    try:
        crud.create(provider, interface_configurations)
    except Exception as e:
        print(str(e))

    exit()
# End of script
