"""

"""
import re
import json
import os
import logging
from typing import Dict, Optional, NoReturn, List, Callable

import typer
from pydantic import BaseModel
from fabric import Connection
from fabric.runners import Result

from nuvla_cli.helpers.edge import CLIEdgeData
from nuvla_cli.cli_settings import CLISettings
from nuvla_cli.common.cli_common import print_success
from nuvla_cli.helpers.engine import EngineDeploymentConfig, generate_engine_config


app = typer.Typer()
logger: logging.Logger = logging.getLogger(__name__)


class DeviceData(BaseModel):
    hostname: str
    address: str
    user: str
    port: int = 22
    docker: Optional[str]
    docker_compose: Optional[str]
    pub_key: Optional[str]
    deployments: Dict[str, CLIEdgeData] = {}
    online: bool = False
    starter: Callable


class DeviceManagerData(BaseModel):
    devices: Dict[str, DeviceData] = {}


class DeviceManager:
    """
    Handles local file DB for remote and local device managers
    """
    cli_settings: CLISettings = CLISettings()

    def __init__(self):
        """

        """
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.manager_data: DeviceManagerData = self.load_devices_file()

        self.update_devices_status()

    def update_devices_status(self):
        """

        :return: None
        """
        for k, v in self.manager_data.devices.items():
            it_conn: Connection = Connection(host=k, user=v.user, port=v.port,
                                             connect_kwargs={"password": 'pi'})
            it_conn.open()
            v.online = it_conn.is_connected
            it_conn.close()

    def load_devices_file(self) -> DeviceManagerData:
        """

        :return:
        """
        if os.path.exists(self.cli_settings.devices_file):
            with open(self.cli_settings.devices_file, 'r') as devices_file:
                return DeviceManagerData.parse_obj(json.load(devices_file))
        else:
            os.makedirs(self.cli_settings.NUVLA_CLI_PATH, exist_ok=True)
            return DeviceManagerData()

    def save_devices_to_file(self) -> NoReturn:
        """

        :return: None
        """
        self.logger.info(f'Saving {self.cli_settings.dict()} to'
                         f' {self.cli_settings.devices_file}')
        if not os.path.exists(self.cli_settings.NUVLA_CLI_PATH):
            os.makedirs(self.cli_settings.NUVLA_CLI_PATH)

        with open(self.cli_settings.devices_file, 'w') as dev_file:
            json.dump(self.manager_data.dict(), dev_file, indent=4)

    @staticmethod
    def reachable(connection: Connection) -> str:
        """

        :param connection:
        :return:
        """
        response: Result = connection.run('hostname', hide=True)
        if connection.is_connected:
            return response.stdout
        else:
            return ''

    @staticmethod
    def check_dev_requirements(dev_data: DeviceData, connection: Connection) -> bool:
        """

        :param dev_data:
        :param connection:
        :return:
        """
        result: Result = connection.run('docker -v', hide=True)
        if result.return_code != 0:
            return False
        docker_version: str = result.stdout.split(',')[0].split(' ')[-1]

        result: Result = connection.run('docker-compose -v', hide=True)
        docker_compose_version: str = result.stdout
        if result.return_code != 0:
            return False

        dev_data.docker = docker_version
        dev_data.docker_compose = docker_compose_version
        return True

    @staticmethod
    def is_ip_private(ip):
        """

        :param ip:
        :return:
        """
        private_lo = re.compile("^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        # private_24 = re.compile("^10\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        # private_20 = re.compile("^192\.168\.\d{1,3}.\d{1,3}$")
        # private_16 = re.compile("^172.(1[6-9]|2[0-9]|3[0-1]).[0-9]{1,3}.[0-9]{1,3}$")
        private_str = re.compile("localhost")

        result = private_lo.match(ip) or private_str.match(ip)
        return result is not None

    def add_device(self, address: str, user: str, port: int) -> bool:
        """

        :return: True if the requisites are met and the device is added
        """
        if self.is_ip_private(address):
            print(f'WARNING: Trying to add a local device, not supported here. Call '
                  f'deployments with --local flag to deploy edges in this device')
            return False

        if address in self.manager_data.devices.keys():
            print(f'Device already registered with this address: \n'
                  f'{json.dumps(self.manager_data.devices.get(address).dict())}')
            return False

        dev_connection: Connection = Connection(address, user, port,
                                                connect_kwargs={"password": 'pi'})

        hostname: str = self.reachable(connection=dev_connection)

        if not hostname:
            self.logger.debug(f'Device {address}:{port} not reachable with user '
                              f'{user}')
            print(f'Device {address}:{port} not reachable with user {user}')
            return False

        dev_data: DeviceData = DeviceData(
            hostname=hostname,
            address=address,
            user=user,
            port=port,
            online=True
        )

        if not self.check_dev_requirements(connection=dev_connection, dev_data=dev_data):
            return False

        self.manager_data.devices[dev_data.address] = dev_data
        self.save_devices_to_file()
        dev_connection.close()
        return True

    def remove_device(self, address: str):
        """

        :param address:
        :return:
        """
        if address in self.manager_data.devices.keys():
            self.manager_data.devices.pop(address)

        self.save_devices_to_file()
        print_success(f'Device {address} removed')

    def copy_file(self, device: str, origin_files: List[str], destination_path: str):
        """

        :param device:
        :param origin_files:
        :param destination_path:
        :return:
        """
        it_dev: DeviceData = self.manager_data.devices.get(device)
        dev_connection: Connection = Connection(it_dev.address,
                                                it_dev.user,
                                                it_dev.port,
                                                connect_kwargs={"password": 'pi'})

        for file in origin_files:
            dev_connection.put(local=file, remote=destination_path)

        dev_connection.close()

    def assess_deployment_name(self):
        ...

    def start_engine(self, device: str, uuid: str):
        it_dev: DeviceData = self.manager_data.devices.get(device)
        dev_connection: Connection = Connection(it_dev.address,
                                                it_dev.user,
                                                it_dev.port,
                                                connect_kwargs={"password": 'pi'})

        deployment_config: EngineDeploymentConfig = generate_engine_config(0, uuid)
        logger.info(f'Starting NuvlaEdge engine with UUID:{uuid} and configuration \n'
                    f'{json.dumps(deployment_config.dict(), indent=4)}')


class Device:
    ...


class LocalDevice(Device):
    ...


class RemoteDevice(Device):
    ...


class DummyDevice(Device):
    ...