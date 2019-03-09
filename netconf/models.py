from ydk.services import NetconfService
from ydk.services import Datastore
from ydk.providers import NetconfServiceProvider

from ydk.services import CodecService
from ydk.providers import CodecServiceProvider

json_provider = CodecServiceProvider(type='json')
xml_provider = CodecServiceProvider(type='xml')
codec = CodecService()
nc = NetconfService()


class NetConf:
    def __init__(self, address, port, username, password):
        self.address = address
        self.port = port
        self.username = username
        self.password = password
        self.session = self.create_session()

    def create_session(self):
        return NetconfServiceProvider(
            address=self.address,
            port=self.port,
            username=self.username,
            password=self.password
        )

    def get(self, read_filter=[]):
        return nc.get(provider=self.session, read_filter=read_filter)

    def get_config(self, source=Datastore.candidate, read_filter=[]):
        return nc.get_config(provider=self.session, source=source, read_filter=read_filter)
