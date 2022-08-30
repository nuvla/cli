"""

"""
import json
import logging
import time
from abc import ABC, abstractmethod
from typing import Optional, Dict, Callable
from enum import Enum

from fabric import Connection
from fabric.runners import Result
from pydantic import BaseModel
from nuvla.api import Api

from nuvla_cli.helpers.engine import EngineDeploymentConfig


class DeviceTypes(Enum):
    REMOTE = 'REMOTE'
    LOCAL = 'LOCAL'
    DUMMY = 'DUMMY'


class DeviceConfiguration(BaseModel):
    address: str
    user: str
    port: int = 22
    hostname: Optional[str]
    docker: Optional[str]
    docker_compose: Optional[str]
    pub_key: Optional[str]
    deployments: Dict[str, EngineDeploymentConfig] = {}
    online: bool = False
    device_type: Optional[str]


class Device(ABC):

    def __init__(self, device_config: DeviceConfiguration):
        """

        :param device_config:
        """
        self.device_config: DeviceConfiguration = device_config

    @abstractmethod
    def start(self, uuid: str):
        """
        Starts a nuvlaedge engine
        :param uuid: engine unique id
        :return: None
        """
        ...

    @abstractmethod
    def stop(self, uuid: str):
        """
        Stops a nuvlaedge engine
        :param uuid: Engine unique id
        :return: None
        """
        ...


class RemoteDevice(Device):
    def __init__(self, device_config: DeviceConfiguration):
        super().__init__(device_config)
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

        self.dev_connection: Connection = Connection(
            self.device_config.address,
            self.device_config.user,
            self.device_config.port,
            connect_kwargs={"password": 'pi'})

        if not device_config.hostname:
            hostname: str = self.reachable()
            if hostname:
                self.device_config.hostname = hostname
                self.device_config.online = True
            self.check_dev_requirements()

    def reachable(self):
        """

        :return:
        """
        response: Result = self.dev_connection.run('hostname', hide=True)
        if self.dev_connection.is_connected:
            return response.stdout
        else:
            return ''

    def check_dev_requirements(self) -> bool:
        """

        :return:
        """
        result: Result = self.dev_connection.run('docker -v', hide=True)
        if result.return_code != 0:
            return False
        docker_version: str = result.stdout.split(',')[0].split(' ')[-1]

        result: Result = self.dev_connection.run('docker-compose -v', hide=True)
        docker_compose_version: str = result.stdout
        if result.return_code != 0:
            return False

        self.device_config.docker = docker_version
        self.device_config.docker_compose = docker_compose_version
        return True

    def start(self, uuid: str):
        # 1.- Copy docker-compose
        # 2.- Parse config to env variables
        # 3.- Launch
        pass

    def stop(self, uuid: str):
        pass


class LocalDevice(Device):
    def __init__(self, device_config: DeviceConfiguration):
        super().__init__(device_config)
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

    def start(self, uuid: str):
        pass

    def stop(self, uuid: str):
        pass


class DummyDevice(Device):
    def __init__(self, device_config: DeviceConfiguration):
        super().__init__(device_config)
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

    def start(self, uuid: str):
        self.logger.info(f'Starting dummy device')
        nuvla_client: Api = Api()
        info = nuvla_client._cimi_post('{}/activate'.format(uuid))

        self.logger.info(f'{uuid} Activated')
        nuvla_client: Api = Api(persist_cookie=False, reauthenticate=True, login_creds={
            'key': info.get('api-key'),
            'secret': info.get('secret-key')
        })
        commission_payload = {"swarm-endpoint": "https://10.1.1.1:5000",
                              "swarm-client-ca": "fake",
                              "swarm-client-cert": "fake",
                              "swarm-client-key": "fake",
                              "swarm-token-manager": "fake",
                              "swarm-token-worker": "fake",
                              "capabilities": ["NUVLA_JOB_PULL"]}
        nuvla_client._cimi_post('{}/commission'.format(uuid),
                                json=commission_payload)

        res = nuvla_client.get(uuid)
        nuvlabox_status_id = res.data.get('nuvlabox-status')
        self.logger.debug(f'{nuvlabox_status_id} Commissioned')

        nuvla_client.edit(nuvlabox_status_id, data={'status': 'OPERATIONAL'})

    def stop(self, uuid: str):
        pass


DEVICE_FACTORY: Dict[str, Callable] = {
    DeviceTypes.DUMMY.name: DummyDevice,
    DeviceTypes.LOCAL.name: LocalDevice,
    DeviceTypes.REMOTE.name: RemoteDevice,
}
