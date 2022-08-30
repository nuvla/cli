"""
Module for Edge handling local and remote devices
"""
import logging

import typer
from rich.table import Table
from rich.console import Console

from nuvla_cli.helpers.device.manager import DeviceManager
from nuvla_cli.helpers.device import DeviceConfiguration

app = typer.Typer()
logger: logging.Logger = logging.getLogger(__name__)
console: Console = Console()


@app.command(name='add')
def add_device(address: str, user: str, port: int = 22, pub_key: str = '',
               dummy: bool = False):
    # TODO: Add support for pub key parsing
    dev_manager: DeviceManager = DeviceManager()

    dev_manager.add_device(DeviceConfiguration(address=address,
                                               user=user,
                                               port=port,
                                               pub_key=pub_key),
                           dummy=dummy)


@app.command(name='remove')
def remove_device(address: str):
    dev_manager: DeviceManager = DeviceManager()
    dev_manager.remove_device(address)


@app.command(name='list')
def list_devices():
    dev_manager: DeviceManager = DeviceManager()
    print(dev_manager.devices_map)
    print('\n\tCurrently registered devices: \n')
    table = Table("Hostname", "Address", "User", "Online")
    for k, v in dev_manager.manager_data.devices.items():
        table.add_row(v.hostname, k, v.user, str(v.online))

    console.print(table)
