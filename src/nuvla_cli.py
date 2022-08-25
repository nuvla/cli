#!/usr/bin/python3
"""

"""
from sys import platform
import logging

import typer

from nuvla_cli.cli import fleet, edge, info, user, device, deploy
from nuvla_cli.cli.edge import remove_edge
from nuvla_cli.cli_nuvla_handler import CLINuvlaHandler, CLISettings

# Main command line interface app
from nuvla_cli.common.cli_common import Colors

app_cli = typer.Typer()

app_cli.add_typer(fleet.app, name='fleet')
app_cli.add_typer(edge.app, name='edge')
app_cli.add_typer(user.app, name='user')
app_cli.add_typer(info.app, name='info')
app_cli.add_typer(device.app, name='device')
app_cli.add_typer(deploy.app, name='deploy')

logger: logging.Logger = logging.getLogger()
cli_settings: CLISettings = CLISettings()


@app_cli.command(name='clear')
def clear_edges():
    """

    :return:
    """
    print('\n' + Colors.WARNING + '\tWARNING:' + Colors.ENDC +
          'This command removes all the Edges created in\n')

    delete: bool = typer.confirm('Are you sure you want to decommission and delete all '
                                 'the Edges created by the CLI in Nuvla?')

    if delete:
        logger.info('Deleting and decommissioning all Edges in Nuvla')
        # Create NuvlaIO instance
        nuvla: CLINuvlaHandler = CLINuvlaHandler()
        edges_in_nuvla = nuvla.nuvla_client.search('nuvlabox',
                                                   filter={"tags=='cli.created=True'"})

        for nuvla_edge in edges_in_nuvla.resources:

            remove_edge(nuvla_edge.data.get('id'))


@app_cli.command(name='version')
def print_cli_version():
    logger.debug('Version print')
    print(f'Nuvla CLI Version {cli_settings}')


def check_os():
    if platform == 'linux' or platform == 'linux2':
        pass
    elif platform == 'darwin':
        pass
    else:
        logging.error(f'Running on a non compatible OS: {platform}')
        raise OSError


if __name__ == '__main__':
    # Check os compatibility for the CLI
    check_os()

    # set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s - %(levelname)s] (%(filename)s, %(funcName)s(), line "
               "%(lineno)d): %(message)s",
        datefmt='%H:%M:%S'
    )
    app_cli()
