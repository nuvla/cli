"""

"""

from pydantic import BaseModel


class EngineDeploymentConfig(BaseModel):
    JOB_PORT: int
    AGENT_PORT: int
    NUVLABOX_UUID: str
    VPN_INTERFACE_NAME: str
    COMPOSE_PROJECT_NAME: str
    EXCLUDED_MONITORS: str = ''


def generate_engine_config(n: int, uuid: str) -> EngineDeploymentConfig:
    it_conf: EngineDeploymentConfig = EngineDeploymentConfig(
        JOB_PORT=5000+n,
        AGENT_PORT=5080+n,
        NUVLABOX_UUID=uuid,
        COMPOSE_PROJECT_NAME='nuvlaedge_{}'.format(n),
        VPN_INTERFACE_NAME='vpn_{}'.format(n),
        EXCLUDED_MONITORS='geolocation'
    )
    return it_conf
