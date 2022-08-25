"""

"""
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Callable
from enum import Enum

from fabric import Connection
from fabric.runners import Result
from pydantic import BaseModel

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
        pass

    def stop(self, uuid: str):
        pass


DEVICE_FACTORY: Dict[str, Callable] = {
    DeviceTypes.DUMMY.name: DummyDevice,
    DeviceTypes.LOCAL.name: LocalDevice,
    DeviceTypes.REMOTE.name: RemoteDevice,
}
