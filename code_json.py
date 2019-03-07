from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.errors import YModelError
import json

from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv6_ospfv3_cfg

json_provider = CodecServiceProvider(type='json')
xml_provider = CodecServiceProvider(type='xml')
codec = CodecService()


result = codec.encode(json_provider, Cisco_IOS_XR_ipv6_ospfv3_cfg.Ospfv3())

print(result)
