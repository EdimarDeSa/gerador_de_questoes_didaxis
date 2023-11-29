from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class VersionInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(alias='Nome')
    version: str = Field(validation_alias='Versão')
    id: Optional[int] = Field(default=None, validation_alias='ID')
    pubdate: Optional[str] = Field(default=None, validation_alias='Publicação')
    file: Optional[str] = Field(default=None, validation_alias='Arquivo')
