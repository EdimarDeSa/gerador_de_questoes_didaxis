import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
import json
import subprocess


class Atualizacao:
    def __init__(self, versao_atual: float, local: Path):
        self.url_base = 'https://www.efscode.com.br/atualizacoes/'
        self.url_versao = 'verifica_versao/'
        self.software_name = 'gerador_de_questoes_didaxis'
        self.data = None
        self.atualizacao = False
        self.versao_atual = versao_atual
        self.local = local.parent

        if self.verifica_conexao_com_internet():
            self.atualizacao = self.verifica_versao()

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
        data = json.loads(response.read().decode('utf-8'))
        self.data = data
        return self.versao_atual < self.versao_recente

    @property
    def versao_recente(self):
        return self.data.get('Versão')

    def atualiza(self):
        # Comando para iniciar o programa secundário
        comando = None
        if str(self.local) == r'C:\Users\Edimar\Documents\GitHub\gerador_de_questoes_didaxis':
            comando = ['.venv/Scripts/python', 'QuestGenUpdater.py', f'-n {self.software_name}']
        else:
            comando = [self.local / 'QuestGenUpdater/QuestGenUpdater.exe', f'-n {self.software_name}']

        # Iniciar o programa secundário usando subprocess
        subprocess.Popen(comando)

