"""

"""
from typing import List, Optional

from pydantic import BaseModel, Field


class CLIEdgeData(BaseModel):
    name: str
    uuid: str = Field('', alias='id')
    dummy: bool = False
    release: Optional[str]
    version: Optional[str]
    tags: List[str] = ['cli.created=True']
    fleets: List[str] = []
    started: bool = False
    vpn_server_id: str = \
        Field('infrastructure-service/eb8e09c2-8387-4f6d-86a4-ff5ddf3d07d7',
              env='VPN_SERVER_ID', alias='vpn-server-id')
    refresh_interval: Optional[int] = Field(30, alias='refresh-interval')
