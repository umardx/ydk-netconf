from argparse import ArgumentParser
from urllib.parse import urlparse

from ydk.errors import YModelError, YServiceProviderError
from ydk.services import CRUDService, CodecService
from ydk.providers import NetconfServiceProvider, CodecServiceProvider
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_telemetry_model_driven_cfg \
    as xr_telemetry_model_driven_cfg
from ydk.types import Empty
import logging
import time


def config_telemetry_model_driven(telemetry_model_driven):
    """Add config data to telemetry_model_driven object."""
    # destination group
    destination_group = telemetry_model_driven.destination_groups.DestinationGroup()
    destination_group.destination_id = "DGROUP1"
    ipv4_destination = destination_group.ipv4_destinations.Ipv4Destination()
    ipv4_destination.destination_port = 5432
    ipv4_destination.ipv4_address = "167.205.3.41"
    ipv4_destination.destination_port = int("5432")
    ipv4_destination.encoding = xr_telemetry_model_driven_cfg.EncodeType.self_describing_gpb
    protocol = ipv4_destination.Protocol()
    protocol.protocol = xr_telemetry_model_driven_cfg.ProtoType.grpc
    protocol.no_tls = 1
    ipv4_destination.protocol = protocol
    destination_group.ipv4_destinations.ipv4_destination.append(ipv4_destination)
    telemetry_model_driven.destination_groups.destination_group.append(destination_group)
    telemetry_model_driven.enable = Empty()

    # sensor group
    sensor_group = telemetry_model_driven.sensor_groups.SensorGroup()
    sensor_group.sensor_group_identifier = "SGROUP1"
    sensor_path = sensor_group.sensor_paths.SensorPath()
    sensor_path.telemetry_sensor_path = "Cisco-IOS-XR-infra-statsd-oper:infra-statistics/interfaces/interface/latest/generic-counters"
    sensor_group.sensor_paths.sensor_path.append(sensor_path)
    telemetry_model_driven.sensor_groups.sensor_group.append(sensor_group)
    sensor_group = telemetry_model_driven.sensor_groups.SensorGroup()
    sensor_group.sensor_group_identifier = "SGROUP2"
    sensor_path = sensor_group.sensor_paths.SensorPath()
    sensor_path.telemetry_sensor_path = "Cisco-IOS-XR-nto-misc-oper:memory-summary/nodes/node/summary"
    sensor_group.sensor_paths.sensor_path.append(sensor_path)
    telemetry_model_driven.sensor_groups.sensor_group.append(sensor_group)

    # subscription
    subscription = telemetry_model_driven.subscriptions.Subscription()
    subscription.subscription_identifier = "SUB1"
    sensor_profile = subscription.sensor_profiles.SensorProfile()
    sensor_profile.sensorgroupid = "SGROUP1"
    sensor_profile.sample_interval = 5000
    subscription.sensor_profiles.sensor_profile.append(sensor_profile)
    sensor_profile = subscription.sensor_profiles.SensorProfile()
    sensor_profile.sensorgroupid = "SGROUP2"
    sensor_profile.sample_interval = 8000
    subscription.sensor_profiles.sensor_profile.append(sensor_profile)
    destination_profile = subscription.destination_profiles.DestinationProfile()
    destination_profile.destination_id = "DGROUP1"
    subscription.destination_profiles.destination_profile.append(destination_profile)
    telemetry_model_driven.subscriptions.subscription.append(subscription)


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

    # Instantiate codec providers with json and xml options
    json_provider = CodecServiceProvider(type='json')
    xml_provider = CodecServiceProvider(type='xml')

    # create NETCONF provider
    provider = NetconfServiceProvider(address=device.hostname,
                                      port=device.port,
                                      username=device.username,
                                      password=device.password,
                                      protocol=device.scheme)
    # create CRUD service
    crud = CRUDService()

    # create codec service
    codec = CodecService()

    telemetry_model_driven = xr_telemetry_model_driven_cfg.TelemetryModelDriven()  # create object
    config_telemetry_model_driven(telemetry_model_driven)  # add object configuration

    # create configuration on NETCONF device
    try:
        crud.create(provider, telemetry_model_driven)
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
