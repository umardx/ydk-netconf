from netconf.models import NetConf
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ifmgr_cfg as ifmgr_cfg
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_telemetry_model_driven_cfg as mdt_cfg

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider

json_provider = CodecServiceProvider(type='json')
xml_provider = CodecServiceProvider(type='xml')
codec = CodecService()

if_cfgs = ifmgr_cfg.InterfaceConfigurations()
mdt = mdt_cfg.TelemetryModelDriven()

xrv = NetConf(
    address='167.205.3.51',
    port=22,
    username='umar',
    password='kuya'
)

if xrv.session is not None:
    result = xrv.get(read_filter=mdt)
else:
    result = None

if result is not None:
    print(result)
    print(type(result))
else:
    print('Can\'t get any result, maybe its client error.')

# sleep(4)
