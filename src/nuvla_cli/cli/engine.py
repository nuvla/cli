"""
Module for Edge handling engine deployments
"""
import logging

import typer


app = typer.Typer()
logger: logging.Logger = logging.getLogger(__name__)


@app.command(name='start', help='Given a UUID, starts an engine. If no address is '
                                'provided it will be started locally')
def engine_start(uuid: str, address: str = ''):
    if not address:
        print(f'Starting edge {uuid} in the local machine')
        return

    print(f'Starting edge {uuid} in {address}')


@app.command(name='stop', help='Stops an engine given its UUID.')
def engine_stop(uuid: str):
    ...
