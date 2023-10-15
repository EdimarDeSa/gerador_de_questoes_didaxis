from tkinter.constants import *

__version__ = '3.2.1'


D = 'Dissertativa'
ME = 'Multipla escolha 1 correta'
MEN = 'Multipla escolha n corretas'
VF = 'Verdadeiro ou falso'

LINK_FEEDBACK_FORM = 'https://forms.office.com/r/xpjpRED6KK'

SHORTCUTS: list[tuple[str, str]] = [
    ('Abre tela de atalhos:', 'F1'),
    ('Salvar como:', 'F12'),
    ('Salva questão:', 'Ctrl + S'),
    ('Abrir:', 'Ctrl + O'),
    ('Exportar:', 'Ctrl + E'),
    ('Adiciona opção:', 'Ctrl + "+" ou Ctrl + "="'),
    ('Remover opção:', 'Ctrl + "-"'),
    ('Alterar tipo da questão:', 'Ctrl + 1, 2 ou 3'),
    ('Alterar dificuldade:', 'Ctrl + 4, 5 ou 6'),
    ('Desfazer:', 'Ctrl + Z'),
    ('Refazer:', 'Ctrl + Y'),
    ('Pular campos:', 'Ctrl + TAB ou TAB'),
    ('Voltar campos:', 'Ctrl + Shift + TAB ou Shift + TAB'),
]

FILETYPES: tuple[tuple[str, str]] = (
    ('Pasta de Trabalho do Excel', '*.xlsx'),
)

DEFAULT_EXTENSION: str = '.xlsx'

CONFIGURACOES: dict = {
    'cor_da_borda': 'darkgreen',
    'cor_de_fundo': 'lightgreen',
    'fonte': 'Arial',
    'tamanho_texto': 8,
    'tamanho_titulo': 10,
    'fonte_estilo': 'bold',
    'tipos': ['Multipla escolha 1 correta', 'Multipla escolha n corretas', 'Verdadeiro ou falso'],
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
        'Astec',
        'Exportação',
    ],
    'dificuldades': ['Fácil', 'Médio', 'Difícil']
}

PERFIL: dict = {
    'unidade_padrao': '',
    'apagar_enunciado': False,
    'aparencia_do_sistema': 'System',
    'escala_do_sistema': '100%'
}

ENCODER: str = 'UTF-8'

CABECALHO: list[str] = [
    'ID', 'TIPO', 'PESO', 'TEMPO', 'CONTROLE', 'PERGUNTA', 'ALTERNATIVA',
    'CORRETA', 'CATEGORIA', 'SUBCATEGORIA', 'DIFICULDADE'
]

# Place Holders
PLACE_HOLDER_CODIGO = 'TELEC-PXXXX'
PLACE_HOLDER_TEMPO = '00:00:00'
PLACE_HOLDER_PESO = '1'

ADD = 'Adicionar'
RED = '#FA0000'

MAXIMO_DE_CARACTERES = 255
PORCENTAGENS = ["80%", "90%", "100%", "110%", "120%"]
APARENCIAS_DO_SISTEMA = ["Light", "Dark", "System"]

