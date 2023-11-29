import subprocess
import tomllib
from pathlib import Path

import requests

from ..DataModels.versionmodel import VersionInfo


class VersionChecker:
    def __init__(self, software_name: str):
        self.base_url = (
            f'https://efscode.com.br/atualizacoes/verifica_versao/{software_name}'
        )

        self.version_infos = self.check_atual_version_info()

        self.new_version_available = False

    def check_version(self) -> None:
        try:
            response = requests.get(self.base_url).json()
            new_version_info = VersionInfo(**response)

            (
                current_version,
                current_release,
                current_patch,
            ) = self.version_infos.version.split('.')
            new_version, new_release, new_patch = new_version_info.version.split('.')

            if any(
                (
                    int(current_version) < int(new_version),
                    int(current_release) < int(new_release),
                    int(current_patch) < int(new_patch),
                )
            ):
                self.new_version_available = True

        except requests.ConnectionError:
            raise ConnectionError('Sem conexão com o servidor para atualizações.')

    def update(self) -> None:
        subprocess.call(
            ['../SUT.exe', f'--name {self.version_infos.name}'],
            stdout=False,
            shell=True,
        )

    @staticmethod
    def check_atual_version_info() -> VersionInfo:
        path = Path(__file__).resolve().parent.parent.parent / 'pyproject.toml'
        with open(path, 'rb') as toml_file:
            infos = tomllib.load(toml_file)['tool']['poetry']
            return VersionInfo(**infos)
