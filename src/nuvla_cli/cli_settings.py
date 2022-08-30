import os

from pydantic import BaseModel, validator


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


class CLIConstants(BaseModel):
    DEFAULT_NAME: str = '[CLI] NuvlaEdge_'
    CLI_TAG: str = 'cli.created=True'
    CLI_DUMMY_TAG: str = 'cli.dummy=True'
    CLI_FLEET_PREFIX: str = 'cli.fleet.name='
    FLEET_DEFAULT_NAME: str = '[{fleet_name}] NuvlaEdge_{cnt}'
