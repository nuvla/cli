""" Create command for Edge, Fleet and Device (Remote) """
import logging

import typer

from ..nuvlaio.nuvlaedge_engine import NuvlaEdgeEngine


app = typer.Typer()
logger: logging.Logger = logging.getLogger(__name__)


@app.command(name='edge')
def stop_edge(uuid: str):
    """

    :param uuid:
    :return:
    """
    deployer: NuvlaEdgeEngine = NuvlaEdgeEngine()

    deployer.stop_edge(uuid)


@app.command(name='fleet')
def stop_fleet(fleet_name: str):
    deployer: NuvlaEdgeEngine = NuvlaEdgeEngine()
    deployer.stop_fleet(fleet_name)
