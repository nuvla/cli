"""
Module for Edge handling command
"""
import logging
from datetime import datetime
from typing import Optional
import warnings

import typer
from pydantic import BaseSettings, Field
from rich import print

from nuvla_cli.cli_nuvla_handler import CLINuvlaHandler
from nuvla_cli.common.validators import NuvlaID
from nuvla_cli.common.cli_common import print_warning, print_success

warnings.filterwarnings("ignore")
app = typer.Typer()
logger: logging.Logger = logging.getLogger(__name__)


class UserSchema(BaseSettings):
    API_KEY: str = Field('', env='API_KEY')
    API_SECRET: str = Field('', env='API_SECRET')
    name: Optional[str]
    updated: Optional[datetime]
    created: Optional[datetime]
    state: Optional[str]
    resource_type: str = Field('', alias='resource-type')
    id: Optional[NuvlaID]

    class Config:
        allow_population_by_field_name = True


@app.command(name='login')
def login(config_file: str = ''):
    """
    Login to Nuvla. The login is persistent and only with API keys

    :param config_file: Optional configuration file path where the keys are stored.
    :return: None
    """
    nuvla: CLINuvlaHandler = CLINuvlaHandler()

    if nuvla.nuvla_client.is_authenticated():
        session_info = nuvla.nuvla_client.get(nuvla.nuvla_client.current_session())
        user_info = nuvla.nuvla_client.get(session_info.data.get('user'))
        print_success(f'Session already authenticated as {user_info.data.get("name")}')
        return

    user_data: UserSchema = UserSchema()
    if user_data.API_KEY and user_data.API_SECRET:
        nuvla.nuvla_client.login_apikey(user_data.API_KEY, user_data.API_SECRET)

    elif config_file:
        print_warning('API keys not provided. Use API_KEY and API_SECRET to parse the '
                      'nuvla API keys')
        print(f'Credentials not provided by environmental variable, loading {config_file}'
              f' file')

    print_success(f'Successfully logged in as {user_data.name}')


@app.command(name='logout', help='Logout from nuvla')
def logout():
    nuvla: CLINuvlaHandler = CLINuvlaHandler()

    if not nuvla.nuvla_client.is_authenticated():
        print_warning('Currently not logged in')

    else:
        logger.debug('Logging out')
        user_data: UserSchema = UserSchema()
        nuvla.log_to_nuvla(user_data.API_KEY, user_data.API_SECRET)
