"""

"""
import logging
from typing import Dict
import toml
from typing import NoReturn


logger: logging.Logger = logging.getLogger(__name__)


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


colors: Colors = Colors()


def import_env_variables(envs_file: str = 'configuration.toml') -> Dict:
    """

    :param envs_file:
    :return:
    """
    return toml.load(envs_file)['nuvla']


def print_warning(message: str) -> NoReturn:
    """

    :param message:
    :return:
    """
    print(f'\n{Colors.WARNING} \tWARNING:{Colors.ENDC} {message}\n')


def print_success(message: str) -> NoReturn:
    """

    :param message:
    :return:
    """
    print(f'\n{Colors.OKGREEN} \tSuccess:{Colors.ENDC} {message}\n')
