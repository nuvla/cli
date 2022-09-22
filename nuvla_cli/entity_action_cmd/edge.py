"""

"""
import logging
from typing import List, Tuple

import typer
from rich import print

from nuvla_cli.common.common import NuvlaID, print_success, print_warning
from nuvla_cli.common.geo_location import generate_random_coordinate, locate_nuvlaedge
from nuvla_cli.nuvlaio.edge import Edge
from nuvla_cli.nuvlaio.device import DeviceTypes
from nuvla_cli.nuvlaio.nuvlaedge_engine import NuvlaEdgeEngine


app = typer.Typer()
logger: logging.Logger = logging.getLogger(__name__)


@app.command(name='create')
def create(name: str = typer.Option('', help='Edges name to be created'),
           description: str = typer.Option('', help='Edge descriptions'),
           dummy: bool = typer.Option(False, help='Create a dummy Edge'),
           fleet_name: str = typer.Option('', help='Attach created Edge to existent '
                                                   'fleet')):
    """
    Creates a new NuvlaEdge
    """
    if name:
        logger.debug(f'Creating new Edge with name {name}')
        print(f'Creating new Edge with name {name}')
    else:
        logger.debug(f'Creating new Edge with default name {name}')
        print(f'Creating new Edge with default name {name}')

    it_edge: Edge = Edge()
    uuid: NuvlaID = it_edge.create_edge(
        name=name,
        description=description,
        dummy=dummy,
        fleet_name=fleet_name)

    if uuid:
        print_success(f'Edge created: {uuid}')


@app.command(name='delete')
def remove(nuvla_id: str = typer.Option('', help='Unique Nuvla ID of the NuvlaEdge'
                                                 'identifier')):
    """
    Removes a NuvlaEdge from Nuvla
    """
    if nuvla_id:
        logger.debug(f'Creating new Edge with name {nuvla_id}')
        print(f'Creating new Edge with nuvla_id {nuvla_id}')
    else:
        logger.debug(f'Creating new Edge with default nuvla_id {nuvla_id}')
        print(f'Creating new Edge with default nuvla_id {nuvla_id}')

    it_edge: Edge = Edge()

    it_edge.remove_edge(nuvla_id)


@app.command(name='list')
def list_edges():
    """
    Lists the CLI created edges in the logged-in user
    """
    it_edge: Edge = Edge()
    it_edge.list_edges()


@app.command(name='start')
def start_edge(nuvla_id: str = typer.Option('', help='Unique Nuvla ID of the NuvlaEdge '
                                                     'identifier')):
    """
    Starts a NuvlaEdge engine in the device running this CLI.

    If the NuvlaEdge entity is created as dummy, it will perform the activation and
    commissioning process
    """
    if nuvla_id:
        logger.debug(f'Starting new Edge with name {nuvla_id}')
        print(f'Starting new Edge with nuvla_id {nuvla_id}')
    else:
        logger.debug(f'Starting new Edge with default nuvla_id {nuvla_id}')
        print(f'Starting new Edge with default nuvla_id {nuvla_id}')

    deployer: NuvlaEdgeEngine = NuvlaEdgeEngine()

    deployer.start_engine(NuvlaID(nuvla_id), DeviceTypes.LOCAL)


@app.command(name='stop')
def stop_edge(nuvla_id: str = typer.Option('', help='Unique Nuvla ID of the NuvlaEdge '
                                                    'identifier')):
    """
    Stops a local NuvlaEdge with the Nuvla ID
    """

    deployer: NuvlaEdgeEngine = NuvlaEdgeEngine()

    deployer.stop_edge(nuvla_id)


@app.command(name='geolocate')
def geolocate_edge(nuvla_id: str = typer.Option(..., help='Unique Nuvla ID of the '
                                                          'NuvlaEdge identifier'),
                   country: str = typer.Option(..., help='Country to generate a random'
                                                         'coordinates within')):
    """
    Generates a random coordinate within the provided country and locates the provided
    NuvlaEdge on those coordinates
    """

    edge: Edge = Edge()

    if nuvla_id not in edge.edges.keys():
        print_warning(f'NuvlaEdge {nuvla_id} not present')
        return

    coords: List[Tuple] = generate_random_coordinate(
        count=1,
        country=country
    )

    locate_nuvlaedge(edge.nuvla_api, coords[0], nuvla_id)
