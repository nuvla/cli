""" Create command for Edge, Fleet and Device (Remote) """
import logging

import typer

from nuvla_cli.nuvlaio.nuvlaio_cli import NuvlaIO

app = typer.Typer()
logger: logging.Logger = logging.getLogger(__name__)


@app.command(name='login')
def login(key: str = '', secret: str = '', config_file: str = ''):
    """
    Login to Nuvla. The login is persistent and only with API keys

    :param key:
    :param secret:
    :param config_file: Optional configuration file path where the keys are stored.
    :return: None
    """
    nuvla: NuvlaIO = NuvlaIO()

    nuvla.log_to_nuvla(key, secret, config_file)


@app.command(name='logout')
def logout():
    """

    :return:
    """
    nuvla: NuvlaIO = NuvlaIO()

    nuvla.logout()
