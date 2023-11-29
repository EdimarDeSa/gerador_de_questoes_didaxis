import subprocess
import tomllib

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
            print(response)

            new_version_info = VersionInfo(**response)

            current_version, current_release, current_patch = self.version_infos.version.split('.')
            new_version, new_release, new_patch = new_version_info.version.split('.')

            if not any((
                    current_version < new_version,
                    current_release < new_release,
                    current_patch < new_patch
            )):
                self.new_version_available = True

        except requests.ConnectionError:
            raise ConnectionError('Sem conexão com o servidor para atualizações.')

    def update(self) -> None:
        subprocess.call(['../SUT.exe', f'--name {self.version_infos.name}'], stdout=False, shell=True)

    @staticmethod
    def check_atual_version_info() -> VersionInfo:
        with open('./pyproject.toml', 'rb') as toml_file:
            infos = tomllib.load(toml_file)['tool']['poetry']
            return VersionInfo(**infos)
