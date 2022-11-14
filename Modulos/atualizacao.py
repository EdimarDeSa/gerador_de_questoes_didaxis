from datetime import datetime
from os.path import abspath
from pathlib import Path
from subprocess import call
from time import ctime
from main import Interface

class Atualizacao:
    local_atual = abspath('./')
    pasta_atualizacao = 'V:\\Itec\\10 - Treinamentos\\02 - Materiais de Treinamento\\Gerador de ' \
                        'questões\\gerador_questao'

    def __init__(self):
        resp = self.__verifica_ping()
        if resp:
            atualizar = self.__verifica_versao()
            if atualizar:
                self.__gera_bkp()
                self.__atualiza()
                self.__inicia_atualizado()
        else:
            call('py main.py')

    def __verifica_ping(self):
        ping = call('ping -w 200 -n 1 10.1.105.1', shell = False, stdout = False)
        return not ping

    def __verifica_versao(self):
        status_arquivo_atual = Path(self.local_atual).stat()
        cdata_mod_arquivo_atual = status_arquivo_atual.st_mtime

        status_arquivo_atualizacao = Path(self.pasta_atualizacao).stat()
        cdata_mod_arquivo_atualizacao = status_arquivo_atualizacao.st_mtime

        print(cdata_mod_arquivo_atual, cdata_mod_arquivo_atualizacao)

        return cdata_mod_arquivo_atual < cdata_mod_arquivo_atualizacao

    def __atualiza(self):
        call('')


if __name__ == '__main__':
    Atualizacao()