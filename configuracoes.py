from json import dump, load
from os.path import abspath, exists

class Configs:
    @classmethod
    def verifica_dependencias(cls):
        config_path = abspath('./configs/configs.json')
        if not exists(config_path):
            infos = {
                'root': {
                    'background': 'green',
                },
                'param_labels': {
                    'background': 'lightgreen',
                    'font': 'Arial 10 bold',
                },
                'param_lists': {
                    'selectmode': 'single',
                    'height': 3,
                    'font': 'Arial 8 bold',
                    'relief': 'sunken',
                    'selectbackground': 'lightgreen',
                    'exportselection': False,
                },
                'tipos': [
                    'Multipla escolha 1 correta',
                    'Multipla escolha n corretas',
                    'Verdadeiro ou falso'
                ],
                'unidades': [
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
                    'Astec'
                ]
            }
            cls.salva_configs(infos)

    @classmethod
    def salva_configs(cls, infos):
        config_path = abspath('./configs/configs.json')
        with open(file = config_path, mode = 'r', encoding = 'UTF-8') as arquivo_configuracoes:
            dump(infos, arquivo_configuracoes, indent = 4)

    @classmethod
    def abre_configs(cls, chave):
        config_path = abspath('./configs/configs.json')
        with open(file = config_path, mode = 'r', encoding = 'UTF-8') as arquivo_configuracoes:
            infos = load(arquivo_configuracoes)
            return infos[chave]

