import subprocess

from requests import get

from BackEndFunctions.FileManagerLib.json_serializer import *


class Atualizacao:
    url_base = 'https://www.efscode.com.br/atualizacoes/'

    def __init__(self):
        self.url_versao = 'verifica_versao/'
        self.software_name = 'gerador_de_questoes_didaxis'
        self.json_data = None
        self.atualizacao_disponivel = False

        if self.verifica_conexao_com_internet():
            self.atualizacao_disponivel = self.verifica_versao()

    def verifica_conexao_com_internet(self):
        try:
            urllib.request.urlopen(self.__gera_url_versao(), timeout=4)
            return True
        except urllib.error.URLError:
            return False

    def __gera_url_versao(self) -> str:
        url_versao = self.url_base + self.url_versao + self.software_name
        encoded_url_versao = urllib.parse.quote(url_versao, safe=':/')
        return encoded_url_versao

    def verifica_versao(self):
        response = urllib.request.urlopen(self.__gera_url_versao())
        self.json_data = json.loads(response.read().decode('utf-8'))

        versao_atual, revisao_atual, alteracao_atual = self.versao_atual.split('.')
        versao_nova, revisao_nova, alteracao_nova = self.versao_nova.split('.')

        return versao_nova > versao_atual or revisao_nova > revisao_atual or alteracao_nova > alteracao_atual

    def atualiza(self):
        # Comando para iniciar o programa secundário
        if str(self.arquivos.base_dir) == 'C:/Users/Edimar/Documents/GitHub/gerador_de_questoes_didaxis':
            comando = ['.venv/Scripts/python', 'QuestGenUpdater.py', f'-n {self.software_name}']
        else:
            comando = [self.arquivos.base_dir / 'QuestGenUpdater/QuestGenUpdater.exe', f'-n {self.software_name}']

        subprocess.Popen(comando)

    @property
    def versao_nova(self) -> str:
        return str(self.json_data.get('Versão')) + '.0'

