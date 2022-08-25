"""
Module for Edge handling command
"""
import logging
import time
import typer
from typing import List, Tuple

from nuvla_cli.cli_nuvla_handler import CLINuvlaHandler
from tabulate import tabulate

from nuvla_cli.helpers.edge import CLIEdgeData
from nuvla_cli.common import geo_location


app = typer.Typer()
logger: logging.Logger = logging.getLogger(__name__)


def generate_default_name(nuvla: CLINuvlaHandler):
    logger.info(f'Generating new name')

    current_names: List[str] = \
        [i.name.replace(nuvla.cli_constants.DEFAULT_NAME, '')
         for i in nuvla.cli_status.edges.values()
         if i.name.startswith(nuvla.cli_constants.DEFAULT_NAME)]
    logger.info(f'Current names {current_names}')
    if current_names:
        current_names.sort()
        return nuvla.cli_constants.DEFAULT_NAME + str(int(current_names[-1]) + 1)
    else:
        return nuvla.cli_constants.DEFAULT_NAME + '0'


@app.command(name='create', help='Creates a single edge instance in Nuvla')
def create_edge(name: str = '', description: str = '', dummy: bool = False,
                fleet_name: str = ''):
    logger.debug(f'Creating {name} NuvlaEdge')

    # Create NuvlaIO instance
    nuvla: CLINuvlaHandler = CLINuvlaHandler()

    if not name:

        name = generate_default_name(nuvla)
        logger.info(f'Name not provided, auto-generating {name}')

    new_edge: CLIEdgeData = CLIEdgeData(name=name,
                                        description=description,
                                        dummy=dummy)
    if fleet_name:
        new_edge.tags.append(nuvla.cli_constants.CLI_FLEET_PREFIX + fleet_name)

    if dummy:
        new_edge.tags.append(nuvla.cli_constants.CLI_DUMMY_TAG)

    nuvla.create_new_edge(new_edge)


@app.command(name='remove', help='Removes a single edge instance from Nuvla. Only removes'
                                 'instances created by CLI')
def remove_edge(uuid: str):
    logger.debug(f'Removing {uuid} NuvlaEdge')

    # Create NuvlaIO instance
    nuvla: CLINuvlaHandler = CLINuvlaHandler()

    nuvla.decommission(uuid)

    while nuvla.get_nuvlaedge_state(uuid) not in ['DECOMMISSIONED', 'NEW']:
        time.sleep(1)

    nuvla.delete(uuid)


@app.command(name='list', help='Lists all edges created by CLI')
def list_edges():
    # Create NuvlaIO instance
    nuvla: CLINuvlaHandler = CLINuvlaHandler()

    edge_list: List = []
    for uuid, edge in nuvla.cli_status.edges.items():
        edge_list.append([edge.name, uuid, edge.fleets])
    print(tabulate(edge_list,
                   headers=['Name', 'NuvlaEdge UUID', 'Fleets'],
                   tablefmt='orgtbl',
                   showindex=True))


@app.command(name='glocate', help='Randomly geo-locate an edge within the borders of a '
                                  'selected country')
def geo_locate_edge(uuid: str, country: str):
    # Create NuvlaIO instance
    nuvla: CLINuvlaHandler = CLINuvlaHandler()
    if uuid not in nuvla.cli_status.edges.keys():
        print(f'Edge with ID: {uuid} does not exist')
    coordinates: List = geo_location.generate_random_coordinate(count=1, country=country)
    geo_location.locate_nuvlaedge(nuvla, coordinates[0], uuid)
