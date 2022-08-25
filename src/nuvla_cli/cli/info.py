"""
Module for Edge handling command
"""
import logging

import typer


app = typer.Typer()
logger: logging.Logger = logging.getLogger(__name__)


@app.command(name='info', help='Print a global Nuvla system information')
def print_info():
    print('This is some info')
