"""
Module for Edge handling deployments (Apps)
"""

import logging

import typer

from nuvla_cli.cli_nuvla_handler import CLINuvlaHandler
from nuvla_cli.helpers import engine
from nuvla_cli.common.cli_common import print_warning

app = typer.Typer()
logger: logging.Logger = logging.getLogger(__name__)


@app.command(name='app', help='Deploys a new app to Nuvla (App should be available in '
                              'Nuvla and the user must have acces to it')
def deploy_app_to_engine():
    ...

