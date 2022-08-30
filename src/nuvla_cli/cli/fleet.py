"""
Module for Edge handling command
"""
import logging
from typing import List, Tuple

import typer
from tabulate import tabulate

from nuvla_cli.cli import edge
from nuvla_cli.cli_nuvla_handler import CLINuvlaHandler
from nuvla_cli.common import geo_location
from nuvla_cli.common.cli_common import print_warning


app = typer.Typer()
logger: logging.Logger = logging.getLogger(__name__)


@app.command(name='create', help='Creates a new fleet if does not exist and its'
                                 'corresponding count of devices')
def create_fleet(name: str, count: int = 10, dummy: bool = False):
    """

    :param name:
    :param count:
    :param dummy:
    :return:
    """
    logger.info(f'Creating fleet {name} with {count} devices')

    nuvla: CLINuvlaHandler = CLINuvlaHandler()
    if name in nuvla.cli_status.edges.keys():
        response: bool = typer.confirm(f'Fleet name {name} already exists, do you want '
                                       f'to add {count} edges to the currently '
                                       f'existing fleet?')
        if not response:
            return

    edge_name: str = nuvla.cli_constants.FLEET_DEFAULT_NAME.format(fleet_name=name,
                                                                   cnt='{}')

    for i in range(count):
        edge.create_edge(name=edge_name.format(i), fleet_name=name, dummy=dummy)


@app.command(name='remove', help='Deletes all Edge instances attached to the given fleet'
                                 'name.')
def remove_fleet(name: str = ''):
    """

    :param name:
    :return:
    """
    logger.info(f'Deleting {name} fleet')
    if not name:
        print('Please select a fleet from the following available')
        list_fleets()
        return

    nuvla: CLINuvlaHandler = CLINuvlaHandler()
    if name not in nuvla.cli_status.fleets.keys():
        print(f'Provided name does not match any of the existent fleets: ')
        list_fleets()
        return

    for edge_uuid in nuvla.cli_status.fleets.get(name):
        logger.info(f'Removing edge with UUID {edge_uuid}')
        edge.remove_edge(edge_uuid)


@app.command(name='list', help='Lists CLI created fleets')
def list_fleets():
    """

    :return:
    """
    nuvla: CLINuvlaHandler = CLINuvlaHandler()

    fleets: List = []
    for k, v in nuvla.cli_status.fleets.items():
        fleets.append([k, len(v)])

    print(tabulate(fleets,
                   headers=['Name', 'Device Count'],
                   tablefmt='orgtbl',
                   showindex=True))


@app.command(name='glocate', help='Randomly geo locates a fleet within the borders of a '
                                  'chosen country')
def geo_locate_fleet(name: str, country: str, create: bool = False, count: int = 10,
                     dummy: bool = False):
    """

    :param name:
    :param country:
    :param create:
    :param count
    :param dummy
    :return:
    """
    nuvla: CLINuvlaHandler = CLINuvlaHandler()
    if name not in nuvla.cli_status.fleets.keys():
        print(f'Fleet name {name} provided not in currently present in fleets')
        if not create:
            print(f'\nIf you want to create the fleet as well call the command '
                  f'with --create flag, else chose a fleet from the following:')
            list_fleets()
            return
        print(f'Creating fleet...')

        create_fleet(name, count=count)

    else:
        count = len(nuvla.cli_status.fleets.get(name))

    coords: List[Tuple] = geo_location.generate_random_coordinate(count, country)
    logger.info(f'Coordinates {coords}')

    for uuid, geo in zip(nuvla.cli_status.fleets.get(name), coords):
        geo_location.locate_nuvlaedge(nuvla, geo, uuid)


@app.command(name='start')
def start_fleet(fleet_name: str):
    """

    :param fleet_name:
    :return:
    """
    nuvla: CLINuvlaHandler = CLINuvlaHandler()
    if fleet_name not in nuvla.cli_status.fleets.keys():
        print_warning(f'Fleet {fleet_name} not present. Create it first...')
        return
