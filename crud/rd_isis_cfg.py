from argparse import ArgumentParser
from urllib.parse import urlparse

from ydk.errors import YModelError, YServiceProviderError
from ydk.services import CRUDService, CodecService
from ydk.providers import NetconfServiceProvider, CodecServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_clns_isis_cfg
from ydk.types import Empty
from ydk.filters import YFilter
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

    # Instantiate codec providers with json and xml options
    json_provider = CodecServiceProvider(type='json')
    xml_provider = CodecServiceProvider(type='xml')

    # create CRUD service
    crud = CRUDService()

    # create codec service
    codec = CodecService()

    # First create the top-level Isis() object
    isis = Cisco_IOS_XR_clns_isis_cfg.Isis()

    # Create the list instance
    ins = Cisco_IOS_XR_clns_isis_cfg.Isis.Instances.Instance()
    ins.instance_name = 'default'

    # Set the yfilter attribute of the leaf called 'running' to YFilter.read
    ins.running = YFilter.read

    # Append the instance to the parent
    isis.instances.instance.append(ins)

    # Call the CRUD read on the top-level isis object
    # (assuming you have already instantiated the service and provider)

    # create NETCONF operation
    try:
        _result = crud.read(provider, isis)
        if _result is not None:
            result = codec.encode(json_provider, _result)
            print(result)
            with open("rd_isis_cfg.json", "w") as f:
                f.write(result)
        else:
            print("No result")
    except YServiceProviderError as err:
        print("NETCONF FAILED with Error:")
        print(err.message.split('</error-message>')[0].split('"en">')[1])
    except YModelError as err:
        print("YDK VALIDATION FAILED with YModelError:")
        print(err.message)

    end_time = time.time()
    delta = end_time - start_time
    print("Time delta: ", str(delta))
    exit()
# End of script
