from ydk.services import CodecService
from ydk.providers import CodecServiceProvider
from ydk.errors import YModelError
import json

json_provider = CodecServiceProvider(type='json')
xml_provider = CodecServiceProvider(type='xml')
codec = CodecService()

with open('crud/rd_ifmgr_cfg.json') as f:
    data_dict_f = json.load(f)
#
# print('DICT FROM FILE: \n{}\n\n'.format(json_dict))
# print('STRING FROM FILE: \n{}\n\n'.format(json.dumps(json_dict)))

# res_json = codec.decode(json_provider, json.dumps(json_dict))
# res_xml = codec.decode(xml_provider, json.dumps(json_dict))
#
# print('RES_JSON: \n{}\n\n'.format(res_json))
# print('RES_XML: \n{}\n\n'.format(res_xml))


data_dict = {'Cisco-IOS-XR-ifmgr-cfg:interface-configurations': {'interface-configuration': [{'active': 'act', 'interface-name': 'MgmtEth0/RP0/CPU0/0', 'Cisco-IOS-XR-ipv4-io-cfg:ipv4-network': {'addresses': {'primary': {'address': '167.205.3.51', 'netmask': '255.255.255.0'}}}}, {'active': 'act', 'interface-name': 'GigabitEthernet0/0/0/0', 'description': 'Interface 0', 'Cisco-IOS-XR-ipv4-io-cfg:ipv4-network': {'addresses': {'primary': {'address': '172.18.0.1', 'netmask': '255.255.255.252'}}}}, {'active': 'act', 'interface-name': 'GigabitEthernet0/0/0/1', 'description': 'Interface 1', 'Cisco-IOS-XR-ipv4-io-cfg:ipv4-network': {'addresses': {'primary': {'address': '172.18.1.1', 'netmask': '255.255.255.0'}}}}, {'active': 'act', 'interface-name': 'GigabitEthernet0/0/0/2', 'description': 'Interface 2', 'Cisco-IOS-XR-ipv4-io-cfg:ipv4-network': {'addresses': {'primary': {'address': '172.18.3.1', 'netmask': '255.255.255.0'}}}}]}}

print(type(data_dict_f))
print('datadict_f\n{}\n'.format(data_dict_f))
print(type(data_dict))
print('datadict\n{}\n'.format(data_dict))


try:
    resp0 = codec.decode(json_provider, json.dumps(data_dict_f))
    print('datadict_f')
    print(resp0)
except YModelError as err:
    print(str(err))

try:
    resp1 = codec.decode(json_provider, json.dumps(data_dict))
    print('datadict')
    print(resp1)
except YModelError as err:
    print(str(err))

