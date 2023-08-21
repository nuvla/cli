""" Schema for Nuvla User configuration """

from datetime import datetime
from typing import Optional
from typing_extensions import Annotated

from pydantic import Field, BaseModel, Extra
from pydantic_settings import BaseSettings, SettingsConfigDict

from ..common.common import NuvlaID


class UserSchema(BaseSettings):
    model_config = SettingsConfigDict(populate_by_name=True, extra=Extra.ignore, arbitrary_types_allowed=True)

    API_KEY: str = Field('', env='NUVLA_API_KEY')
    API_SECRET: str = Field('', env='NUVLA_API_SECRET')
    name: Optional[str] = None
    updated: Optional[datetime] = None
    created: Optional[datetime] = None
    state: Optional[str] = None
    resource_type: str = Field('', alias='resource-type', env='')
    id: Optional[NuvlaID] = None


class SessionSchema(BaseModel):
    model_config = SettingsConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    # Session tools
    method: str = ''
    id: NuvlaID = NuvlaID('')
    resource_type: str = Field('', alias='resource-type', env='')

    # User data
    roles: Optional[str] = ''
    client_ip: str = Field('', alias='client-ip')
    created_by: str = Field('', alias='created-by')
    identifier: NuvlaID = NuvlaID('')
    user: NuvlaID = NuvlaID('')

    # Dates
    expiry: Optional[datetime]  = None
    updated: Optional[datetime] = None
    created: Optional[datetime] = None
