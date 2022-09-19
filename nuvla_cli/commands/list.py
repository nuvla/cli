""" Create command for Edge, Fleet and Device (Remote) """
import logging

import typer

from ..common.common import NuvlaID
from ..nuvlaio.nuvlaedge_engine import NuvlaEdgeEngine
from ..nuvlaio.edge import Edge

app = typer.Typer()
logger: logging.Logger = logging.getLogger(__name__)


@app.command(name='edge')
def list_edges() -> None:
    """
    Retrieves and prints the list of NuvlaEdge created by CLI

    """
    it_edge: Edge = Edge()
    it_edge.list_edges()


@app.command(name='fleet')
def list_fleets() -> None:
    """
    Retrieves and prints the list of fleet names created by CLI

    """
    it_edge: Edge = Edge()
    it_edge.list_fleets()


# @app.command(name='engine')
# def list_engines():
#     """
#
#     :return:
#     """
#     deployer: NuvlaEdgeEngine = NuvlaEdgeEngine()
#
#     ...

