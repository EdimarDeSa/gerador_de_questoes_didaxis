import requests


class VersionChecker:
    def __init__(self, software_name: str):
        self.id = None
        self.name = software_name
        self.pud_date = None
        self.__version__ = None

        self.url = f'https://efscode.com.br/atualizacoes/verifica_versao/{self.name}'

        self._check_version()

    def _check_version(self):
        try:

            response = requests.get(self.url).json()

            self.id = response['ID']
            self.name = response['Nome']
            self.pud_date = response['Publicação']
            self.__version__ = response['Versão']

        except requests.ConnectionError:
            raise ConnectionError('Sem conexão com o servidor para atualizações.')
