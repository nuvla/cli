"""

"""
import json
import os
import logging
from typing import Dict, List, NoReturn

from pydantic import BaseModel, validator
from nuvla.api import Api
from nuvla.api.models import CimiResponse, CimiCollection

from nuvla_cli.helpers.edge import CLIEdgeData
from nuvla.api.api import NuvlaError


class CLISettings(BaseModel):
    CLI_VERSION: str = '1.0.0'
    NUVLA_CLI_PATH: str = os.path.expanduser('~/.nuvla/cli/')
    DEVICES_FILE: str = '{}.devices'
    UUIDS_FILE: str = '{}.nuvla_uuids'
    DEPLOYMENTS_FILE: str = '{}.deployments'
    STATUS_FILE: str = '{}.status'
    BASE_DEPLOYMENT_COMMAND: str = 'docker-compose -p {project_name} {files} {action}'

    @validator('NUVLA_CLI_PATH')
    def expand_path(cls, v):
        if v.startswith('~'):
            return os.path.expanduser(v)
        else:
            return v

    @property
    def status_file(self):
        return self.STATUS_FILE.format(self.NUVLA_CLI_PATH)

    @property
    def devices_file(self):
        return self.DEVICES_FILE.format(self.NUVLA_CLI_PATH)


class CLIStatus(BaseModel):
    default_edge_count: int = 0
    edges: Dict[str, CLIEdgeData] = {}
    fleets: Dict[str, List[str]] = {}


class CLIConstants(BaseModel):
    DEFAULT_NAME: str = '[CLI] NuvlaEdge_'
    CLI_TAG: str = 'cli.created=True'
    CLI_DUMMY_TAG: str = 'cli.dummy=True'
    CLI_FLEET_PREFIX: str = 'cli.fleet.name='
    FLEET_DEFAULT_NAME: str = '[{fleet_name}] NuvlaEdge_{cnt}'


class CLINuvlaHandler:
    """

    """
    NUVLA_IO_ADDRESS: str = "https://nuvla.io"

    def __init__(self):
        """
        Class constructor
        """
        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

        # Nuvla API Instance
        self.nuvla_client: Api = Api(self.NUVLA_IO_ADDRESS)

        # CLI Status
        self.cli_constants: CLIConstants = CLIConstants()
        self.cli_status: CLIStatus = self.gather_cli_status()

    def parse_edge_into_feet(self, it_status: CLIStatus, edge_data: CLIEdgeData,
                             tag_name: str):
        fleet_name: str = tag_name.replace(self.cli_constants.CLI_FLEET_PREFIX, '')
        edge_data.fleets.append(fleet_name)
        if it_status.fleets.get(fleet_name, []):
            it_status.fleets[fleet_name].append(edge_data.uuid)
        else:
            it_status.fleets[fleet_name] = [edge_data.uuid]

    def gather_cli_status(self) -> CLIStatus:
        """

        :return:
        """
        cli_edges: CimiCollection = \
            self.nuvla_client.search('nuvlabox',
                                     filter={f"tags=='{self.cli_constants.CLI_TAG}'"})
        it_status: CLIStatus = CLIStatus()

        for i in cli_edges.resources:
            it_data = i.data
            it_edge: CLIEdgeData = CLIEdgeData.parse_obj(it_data)
            it_status.edges[it_edge.uuid] = it_edge
            edge_fleets: List[str] = [i for i in it_edge.tags
                                      if self.cli_constants.CLI_FLEET_PREFIX in i]
            for it_fleet in edge_fleets:
                self.parse_edge_into_feet(it_status, it_edge, it_fleet)

        return it_status

    def get_nuvlaedge_state(self, ne_id: str) -> str:
        """
        Gathers the state of the self NuvlaEdge in Nuvla.io if no id is provided.

        :param ne_id: Optional alternative NE id to gather the state from
        :return: the state of the local or provided ne id in Nuvla.ioo
        """
        state = self.nuvla_client.search(
            'nuvlabox', filter=f'id=="{ne_id}"').resources[0].data['state']

        return state

    def create_new_edge(self, edge_data: CLIEdgeData) -> NoReturn:
        """
        Creates a new Edge instance in nuvla and retrieves its unique id

        :return: The uuid of the created NuvlaEdge instance
        """
        # create the instance with the latest release
        edge_data.release = self.nuvla_client.search(
            'nuvlabox-release',
            orderby="created:desc",
            last=1).resources[0].data['release']

        # Version corresponds to the first digit of the release
        edge_data.version = int(edge_data.release.split('.')[0])

        response: CimiResponse = self.nuvla_client.add(
            'nuvlabox',
            data=edge_data.dict(exclude={'dummy', 'uuid', 'fleets', 'started',
                                         'release'},
                                by_alias=True))

        edge_data.uuid = response.data.get('resource-id')

    def decommission(self, uuid: str) -> bool:
        """
        Decommissions the created Edge instances

        :return: true if the decommission process was successful
        """
        try:
            self.logger.debug(f'Decommissioning Edge {uuid}')
            self.nuvla_client.get(uuid + "/decommission")
            return True
        except NuvlaError:
            self.logger.debug('Decommission not possible')
            return False

    def delete(self, uuid: str) -> NoReturn:
        """
        Removes the created Edge instance. It should be decommissioned before deleting

        :return: None
        """
        self.logger.debug(f'Deleting NuvlaEdge {uuid}')
        self.nuvla_client.delete(uuid)
