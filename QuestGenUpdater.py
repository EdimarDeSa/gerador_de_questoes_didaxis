import customtkinter as ctk
import urllib.request
import urllib.parse
import urllib.error
import tempfile
import zipfile
import os
import argparse
import shutil
from pathlib import Path
import tkinter as tk


class Atualizacao(ctk.CTk):
    def __init__(self, args=None):
        self.url_base = 'https://www.efscode.com.br/atualizacoes/'
        self.url_download = 'downloads/'
        self.software_name = args.name
        self.url_encodada = self.__gera_url_atualizacao()

        self.verifica_conexao_com_internet()
        self.inicia_widgets()
        self.gera_bkp()
        self.baixar_nova_versao()

    def verifica_conexao_com_internet(self) -> bool:
        try:
            urllib.request.urlopen(self.url_encodada, timeout=4)
            return True
        except urllib.error.URLError:
            exit('Não foi possível se conectar à internet.')

    def __gera_url_atualizacao(self) -> str:
        url_versao = self.url_base + self.url_download + self.software_name
        encoded_url_versao = urllib.parse.quote(url_versao, safe=':/')
        return encoded_url_versao

    def gera_bkp(self):
        arquivo_origem = Path(__file__).parent.parent / 'gerador_de_questoes_didaxis'

        print(arquivo_origem)

        # arquivo_origem = os.path.dirname(__file__).parent
        # arquivo_temporario = tempfile.mktemp(suffix='.bak')
        # total_bytes = os.path.getsize(arquivo_origem)
        # bytes_copiados = 0
        #
        # try:
        #     with open(arquivo_origem, 'rb') as origem, open(arquivo_temporario, 'wb') as temp:
        #         chunk_size = 1024
        #         while True:
        #             chunk = origem.read(chunk_size)
        #             if not chunk:
        #                 break
        #             temp.write(chunk)
        #             bytes_copiados += len(chunk)
        #             percentual = (bytes_copiados / total_bytes) * 100
        #             progressbar['value'] = percentual
        #             root.update_idletasks()
        #
        #     shutil.move(arquivo_temporario, destino_backup)
        #     print("Backup realizado com sucesso!")
        # except Exception as e:
        #     print(f"Erro ao fazer o backup: {str(e)}")
        #     # Lidar com o erro adequadamente

    # def atualiza(self):
    #     arquivo = self.data.get('Arquivo')
    #     url_atualizacao = self.url_base + self.url_download + arquivo
    #     encoded_url = urllib.parse.quote(url_atualizacao, safe=':/')
    #     with tempfile.NamedTemporaryFile(prefix=self.software_name, suffix='.zip', delete=False) as tmp_file:
    #         response = urllib.request.urlopen(encoded_url)
    #         data = response.read()
    #         tmp_file.write(data)
    #         tmp_file_path = tmp_file.name
    #         print(tmp_file_path)
    #         if zipfile.is_zipfile(tmp_file_path):
    #             with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
    #                 software_path = os.path.dirname(__file__)
    #                 zip_ref.extractall(software_path)
    #                 print(software_path)
    #                 print('Atualização finalizada!!!')

    def baixar_nova_versao(self):
        pass

    def inicia_widgets(self):
        ctk.CTk.__init__(self)
        self.geometry('400x400+400+400')

        self.var_info = tk.StringVar()

        self.barra_de_progresso = ctk.CTkProgressBar(
            self,
            # progress_color='green',
            mode='determinate',
            # height=40,
            # width=300,
            orientation='horizontal',
        )
        self.barra_de_progresso.pack(fill='x')
        self.barra_de_progresso.set(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, help='Name of the software')
    args = parser.parse_args()

    app = Atualizacao(args)
    app.mainloop()