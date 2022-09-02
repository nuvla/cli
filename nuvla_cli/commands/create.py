""" Create command for Edge, Fleet and Device (Remote) """
import logging

import typer

from ..common.common import NuvlaID, print_success, print_warning
from ..schemas.edge_schema import EdgeSchema
from ..nuvlaio.edge import Edge


app = typer.Typer()
logger: logging.Logger = logging.getLogger(__name__)


@app.command(name='edge')
def create_edge(name: str = typer.Option('', help='Edges name to be created'),
                description: str = typer.Option('', help='Edge descriptions'),
                dummy: bool = typer.Option(False, help='Create a dummy Edge'),
                fleet_name: str = typer.Option('', help='Attach created Edge to existent '
                                                        'fleet')):
    """
    Creates a new Edge instance in Nuvla

    """
    logger.debug(f'Creating {name} NuvlaEdge')

    it_edge: Edge = Edge()
    uuid: NuvlaID = it_edge.create_edge(
        name=name,
        description=description,
        dummy=dummy,
        fleet_name=fleet_name)

    if uuid:
        print_success(f'Edge created: {uuid}')


@app.command(name='fleet', help='Creates a new Fleet of Edges in Nuvla')
def create_fleet(name: str, count: int = 10, dummy: bool = False):
    """

    :param name:
    :param count:
    :param dummy:
    :return:
    """
    logger.debug(f'Creating {name} NuvlaEdge')

    it_edge: Edge = Edge()
    it_edge.create_fleet(name=name, count=count, dummy=dummy)


@app.command(name='device', help='Creates a new CLI device instance.')
def create_device(address: str, user: str, port: int = 22):
    ...
