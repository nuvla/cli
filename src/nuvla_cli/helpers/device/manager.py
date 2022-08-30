"""

"""
import os
import re
import json
import socket
import logging
from typing import Dict, NoReturn

from pydantic import BaseModel

from nuvla_cli.cli_settings import CLISettings
from nuvla_cli.helpers.device.device import (DeviceConfiguration, Device, DEVICE_FACTORY,
                                             DeviceTypes)
from nuvla_cli.common.cli_common import print_success, print_warning


class DeviceManagerData(BaseModel):
    devices: Dict[str, DeviceConfiguration] = {}


class DeviceManager:
    """
    Wrapper for device handling
    """
    cli_settings: CLISettings = CLISettings()

    def __init__(self):
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.manager_data: DeviceManagerData = self.load_devices_file()

        self.devices_map: Dict[str, Device] = {}  # Device map with address as Key
        self.populate_devices()

        self.add_dummy(DeviceConfiguration(
            address='dummy',
            user='dummy'
        ))

    def add_dummy(self, dev_config: DeviceConfiguration):
        self.logger.info('Adding default dummy device')
        self.devices_map[DeviceTypes.DUMMY.name] = \
            DEVICE_FACTORY[DeviceTypes.DUMMY.name](dev_config)
        self.manager_data.devices[dev_config.address] = dev_config

    def populate_devices(self):
        """

        :return:
        """
        for k, v in self.manager_data.devices.items():
            self.devices_map[k] = DEVICE_FACTORY[v.device_type](v)

    def load_devices_file(self) -> DeviceManagerData:
        """

        :return:
        """
        self.logger.info('Loading saved devices')
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
        self.logger.info(f'Saving {self.manager_data.dict()} to'
                         f' {self.cli_settings.devices_file}')
        if not os.path.exists(self.cli_settings.NUVLA_CLI_PATH):
            os.makedirs(self.cli_settings.NUVLA_CLI_PATH)

        with open(self.cli_settings.devices_file, 'w') as dev_file:
            json.dump(self.manager_data.dict(), dev_file, indent=4)

    def is_local(self, ip) -> bool:
        """

        :param ip: Address to check
        :return: True if the address corresponds with local standard addresses
        """
        self.logger.info(f'Checking if {ip} is a local address')
        private_lo = re.compile("^127\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        private_str = re.compile("localhost")

        result = private_lo.match(ip) or private_str.match(ip)
        return result is not None

    def add_device(self, device_config: DeviceConfiguration, dummy: bool = False):
        if device_config.address in self.manager_data.devices.keys():
            print_warning(f'Address already registered {device_config.address}')

        dev_type: DeviceTypes = DeviceTypes.REMOTE
        if dummy:
            return

        elif self.is_local(device_config.address):
            return

        self.logger.info(f'Creating {dev_type.name} device with address '
                         f'{device_config.address}')

        device_config.device_type = dev_type.name
        self.devices_map[device_config.address] = \
            DEVICE_FACTORY[dev_type.name](device_config)
        self.manager_data.devices[device_config.address] = device_config

        self.save_devices_to_file()

    def remove_device(self, address: str):
        if address not in self.manager_data.devices.keys():
            print_warning(f'Address {address} not registered, nothing to do')

        self.devices_map.pop(address)
        self.manager_data.devices.pop(address)
        self.save_devices_to_file()
        print_success(f'Device {address} removed from local registry')
