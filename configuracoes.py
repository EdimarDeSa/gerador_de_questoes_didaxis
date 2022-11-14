from json import dump, load
from os.path import abspath, exists

class Configs:
    __config_path = abspath('./configs/configs.json')
    def __init__(self):
        self.__verifica_dependencias()
        self.__abre_configs()

    def __verifica_dependencias(self):
        infos = dict(
            cor_da_borda = 'green',
            cor_de_fundo = 'lightgreen',
            fonte = 'Arial',
            tamanho_texto = 8,
            tamanho_titulo = 10,
            fonte_estilo = 'bold',
            tipos = [
                'Multipla escolha 1 correta',
                'Multipla escolha n corretas',
                'Verdadeiro ou falso'
            ],
            unidades = [
                'Comunicação',
                'Redes',
                'Segurança eletrônica',
                'Controle de acesso',
                'Incêndio e iluminação',
                'Varejo',
                'Verticais',
                'Soluções',
                'Solar',
                'Negócios',
                'Gestão',
                'Energia',
                'Astec',
            ],
            dificuldades = ['Fácil', 'Médio', 'Difícil'],
        )
        config_path = abspath('./configs/configs.json')
        try:
            with open(file = self.__config_path, mode = 'r+', encoding = 'UTF-8') as arquivo_configuracoes:
                arquivos: dict = load(arquivo_configuracoes)
                arquivo_configuracoes.close()
            for info in infos.keys():
                if not arquivos.get(info, False):
                    self.salva_configs(param = info, value = infos[info])

        except:
            with open(file = self.__config_path, mode = 'w', encoding = 'UTF-8') as arquivo_configuracoes:
                dump(infos, arquivo_configuracoes, indent = 2)
                arquivo_configuracoes.close()

    def __abre_configs(self):
        with open(file = self.__config_path, mode = 'r', encoding = 'UTF-8') as arquivo_configuracoes:
            self.configs: dict = load(arquivo_configuracoes)
            arquivo_configuracoes.close()

    def salva_configs(self, param, value):
        with open(file = self.__config_path, mode = 'r+', encoding = 'UTF-8') as arquivo_configuracoes:
            self.configs[param] = value
            dump(self.configs, arquivo_configuracoes, indent = 2)
            arquivo_configuracoes.close()

    @property
    def root_param(self):
        return {'background': self.configs['cor_da_borda']}

    @property
    def frame_param(self):
        return {'background': self.configs['cor_de_fundo']}

    @property
    def label_param(self):
        return {
            'background': self.configs['cor_de_fundo'],
            'font': (self.configs['fonte'], self.configs['tamanho_titulo'], self.configs['fonte_estilo']),
        }

    @property
    def list_param(self):
        return {
            'font':             (self.configs['fonte'], self.configs['tamanho_texto'], self.configs['fonte_estilo']),
            'exportselection':  True,
            'state':            'readonly',
            'justify': 'left',

        }

    @property
    def buttons_param(self):
        return {
            'relief': 'flat',
            'background': self.configs['cor_de_fundo'],
            'compound': 'center',
            'activebackground': self.configs['cor_de_fundo'],
            'anchor': 'center'
        }

    @property
    def tipos(self):
        return self.configs['tipos']

    @property
    def unidades(self):
        unidades:list = self.configs['unidades']
        unidades.sort()
        return unidades

    @property
    def dificuldades(self):
        return self.configs['dificuldades']

    @property
    def versao(self):
        return self.configs['Versão']
