""" Create command for Edge, Fleet and Device (Remote) """
import logging

import typer

from ..common.common import NuvlaID, print_success, print_warning
from ..nuvlaio.device import DeviceTypes
from ..nuvlaio.nuvlaedge_engine import NuvlaEdgeEngine
from ..schemas.edge_schema import EdgeSchema
from ..nuvlaio.edge import Edge


app = typer.Typer()
logger: logging.Logger = logging.getLogger(__name__)


@app.command(name='edge')
def start_edge(uuid: str, target_type: DeviceTypes = DeviceTypes.LOCAL):
    """

    :param uuid:
    :param target_type:
    :return:
    """
    deployer: NuvlaEdgeEngine = NuvlaEdgeEngine()

    deployer.start_engine(NuvlaID(uuid), target_type)


@app.command(name='fleet')
def start_fleet(fleet_name: str, target_type: DeviceTypes = DeviceTypes.LOCAL):
    """

    :param target_type:
    :param fleet_name:
    :return:
    """
    deployer: NuvlaEdgeEngine = NuvlaEdgeEngine()

    deployer.start_fleet(fleet_name, target_type)
