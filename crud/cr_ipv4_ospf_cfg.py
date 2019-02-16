from argparse import ArgumentParser
from urllib.parse import urlparse

from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_ospf_cfg \
    as xr_ipv4_ospf_cfg
from ydk.types import Empty
import logging


def config_ospf(ospf):
    """Add config data to ospf object."""
    # OSPF process
    process = ospf.processes.Process()
    process.process_name = "udx"
    process.start = Empty()

    # Area 0
    area_area_id = process.default_vrf.area_addresses.AreaAreaId()
    area_area_id.area_id = 0
    area_area_id.running = Empty()

    # gi0/0/0/0 interface
    name_scope = area_area_id.name_scopes.NameScope()
    name_scope.interface_name = "GigabitEthernet0/0/0/0"
    name_scope.running = Empty()
    area_area_id.name_scopes.name_scope.append(name_scope)

    # gi0/0/0/1 interface
    name_scope = area_area_id.name_scopes.NameScope()
    name_scope.interface_name = "GigabitEthernet0/0/0/1"
    name_scope.running = Empty()
    area_area_id.name_scopes.name_scope.append(name_scope)

    # gi0/0/0/2 interface
    name_scope = area_area_id.name_scopes.NameScope()
    name_scope.interface_name = "GigabitEthernet0/0/0/2"
    name_scope.running = Empty()
    area_area_id.name_scopes.name_scope.append(name_scope)

    # append area/process config
    process.default_vrf.area_addresses.area_area_id.append(area_area_id)
    ospf.processes.process.append(process)


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

    ospf = xr_ipv4_ospf_cfg.Ospf()  # create object
    config_ospf(ospf)  # add object configuration

    # create configuration on NETCONF device
    try:
        crud.create(provider, ospf)
    except Exception as e:
        print(str(e))

    exit()
# End of script
