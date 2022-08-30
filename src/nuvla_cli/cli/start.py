"""
Module for Edge handling command
"""
import json
import logging

import typer

from nuvla_cli.cli_nuvla_handler import CLINuvlaHandler
from nuvla_cli.common.cli_common import print_warning
from nuvla_cli.helpers.edge import CLIEdgeData

app = typer.Typer()
logger: logging.Logger = logging.getLogger(__name__)


@app.command(name='edge', help='Starts new edge engine')
def start_edge(uuid: str):
    """

    :param uuid:
    :return:
    """
    # Create NuvlaIO instance
    nuvla: CLINuvlaHandler = CLINuvlaHandler()

    it_edge: CLIEdgeData = nuvla.cli_status.edges.get(uuid)
    if not it_edge:
        print_warning(f'Edge with ID: {uuid} does not exist')
        return

    if it_edge.dummy:
        # print(nuvla.device_manager.devices_map.keys())
        nuvla.device_manager.devices_map['DUMMY'].start(it_edge.uuid)

    else:
        # FUTURE: implement remote deployments
        # Now, it will be deployed locally
        nuvla.device_manager.devices_map['DUMMY'].start(it_edge.uuid)


@app.command(name='fleet', help='Starts edge components of a fleet')
def start_fleet(fleet_name: str):
    ...

