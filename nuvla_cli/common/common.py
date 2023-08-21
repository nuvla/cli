""" Common utilities for CLI """
import logging
from typing import List, NoReturn, Any
from dataclasses import dataclass

from pydantic_core import CoreSchema, core_schema
from typing_extensions import get_args, get_origin
from pydantic import BaseModel, GetCoreSchemaHandler, ValidatorFunctionWrapHandler
from pydantic_core import core_schema


logger: logging.Logger = logging.getLogger('tests')


class NuvlaID(str):
    id: str

    @classmethod
    def __get_pydantic_core_schema__(
            cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(cls, handler(str))


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
