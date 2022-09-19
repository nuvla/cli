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
def start_edge(uuid: str = typer.Option(..., help='NuvlaEdge uuid to be started')):
    """
    Starts a NuvlaEdge engine in the device running this CLI.

    If the NuvlaEdge entity is created as dummy, it will perform the activation and
    commissioning process
    """
    deployer: NuvlaEdgeEngine = NuvlaEdgeEngine()

    deployer.start_engine(NuvlaID(uuid), DeviceTypes.LOCAL)


@app.command(name='fleet')
def start_fleet(fleet_name: str = typer.Option(..., help='Fleet name to be started')):
    """
    Starts a Fleet in the device running this CLI.

    If the fleet entity is created as dummy, it will perform the activation and
    commissioning process
    """
    deployer: NuvlaEdgeEngine = NuvlaEdgeEngine()

    deployer.start_fleet(fleet_name, DeviceTypes.LOCAL)
