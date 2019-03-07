from argparse import ArgumentParser
from urllib.parse import urlparse

from ydk.errors import YModelError, YServiceProviderError
from ydk.services import CRUDService, CodecService
from ydk.providers import NetconfServiceProvider, CodecServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ifmgr_cfg \
    as xr_ifmgr_cfg
from ydk.models.openconfig import openconfig_interfaces
import logging
import time


if __name__ == "__main__":
    """Execute main program."""
    start_time = time.time()
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
        formatter = logging.Formatter(
            ("%(asctime)s - %(levelname)s - %(message)s")
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # create NETCONF provider
    provider = NetconfServiceProvider(
        address=device.hostname,
        port=device.port,
        username=device.username,
        password=device.password,
        protocol=device.scheme
    )

    # Instantiate codec providers with json and xml options
    json_provider = CodecServiceProvider(type='json')
    xml_provider = CodecServiceProvider(type='xml')

    # create CRUD service
    crud = CRUDService()

    # create codec service
    codec = CodecService()

    # create object
    interface_configurations = xr_ifmgr_cfg.InterfaceConfigurations()
    oc_ifaces = openconfig_interfaces.Interfaces()

    # create NETCONF operation
    try:
        _result = crud.read_config(provider, interface_configurations)
        if _result is not None:
            result_json = codec.encode(json_provider, _result)
            with open("rd_ifmgr_cfg.json", "w") as f:
                f.write(result_json)
            result_xml = codec.encode(xml_provider, _result)
            with open("rd_ifmgr_cfg.xml", "w") as f:
                f.write(result_xml)
    except YServiceProviderError as err:
        print("NETCONF FAILED with Error:")
        print(err.message.split('</error-message>')[0].split('"en">')[1])
    except YModelError as err:
        print("YDK VALIDATION FAILED with YModelError:")
        print(err.message)

    end_time = time.time()
    delta = end_time - start_time
    print("Time delta: ", str(delta))
    print(type(result_json))
    print(result_json)
    exit()

# End of script
