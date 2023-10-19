from tkinter.constants import *


# Constantes para tipos de questão
D = 'Dissertativa'
ME = 'Multipla escolha 1 correta'
MEN = 'Multipla escolha n corretas'
VF = 'Verdadeiro ou falso'

# Constantes para respostas
V = 'V'
F = 'F'
CORRETA = 'CORRETA'
ERRADA = ''

# Link para o formulário de feedback
LINK_FEEDBACK_FORM = 'https://forms.office.com/r/xpjpRED6KK'

# Atalhos do teclado
SHORTCUTS = [
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
    ('Voltar campos:', 'Ctrl + Shift + TAB ou Shift + TAB')
]

# Tipos de arquivo permitidos
FILETYPES = (('Pasta de Trabalho do Excel', '*.xlsx'),)

# Extensão padrão de arquivo
EXTENSIONS = '.xlsx'

# Configurações gerais
CONFIGURACOES = {
    'cor_da_borda': 'darkgreen',
    'cor_de_fundo': 'lightgreen',
    'fonte': 'Arial',
    'tamanho_texto': 8,
    'tamanho_titulo': 10,
    'fonte_estilo': 'bold',
    'tipos': ['Multipla escolha 1 correta', 'Multipla escolha n corretas', 'Verdadeiro ou falso'],
    'unidades': [
        'Astec', 'Comunicação', 'Controle de acesso', 'Energia', 'Exportação', 'Gestão', 'Incêndio e iluminação',
        'Negócios', 'Redes', 'Segurança eletrônica', 'Solar', 'Soluções', 'Varejo', 'Verticais'
    ],
    'dificuldades': ['Fácil', 'Médio', 'Difícil']
}

# Perfil do usuário
PERFIL = {
    'unidade_padrao': '',
    'apagar_enunciado': False,
    'aparencia_do_sistema': 'System',
    'escala_do_sistema': '100%'
}

# Configurações para codificação de caracteres
ENCODER = 'UTF-8'

# Cabeçalhos das colunas
CABECALHO_DIDAXIS = ['ID', 'TIPO', 'PESO', 'TEMPO', 'CONTROLE', 'PERGUNTA', 'ALTERNATIVA', 'CORRETA',
                     'CATEGORIA', 'SUBCATEGORIA', 'DIFICULDADE']

CABECALHO_DIDAXIS_LOWER = ['id', 'tipo', 'peso', 'tempo', 'controle', 'pergunta', 'alternativas',
                           'categoria', 'subcategoria', 'dificuldade']

CABECALHO_PERGUNTA = ['ID', 'TIPO', 'PESO', 'TEMPO', 'CONTROLE', 'PERGUNTA', 'CATEGORIA', 'SUBCATEGORIA', 'DIFICULDADE']

CABECALHO_ALTERNATIVAS = ['ALTERNATIVA', 'CORRETA']

# Placeholders
PLACE_HOLDER_CODIGO = 'TELEC-PXXXX'
PLACE_HOLDER_TEMPO = '00:00:00'
PLACE_HOLDER_PESO = '1'

# Outras constantes
ADD = 'Adicionar'
RED = '#FA0000'
VERDE = ['#2cbe79', '#2FA572']
TRANSPARENTE = 'transparent'
MAXIMO_DE_CARACTERES = 255
PORCENTAGENS = ["80%", "90%", "100%", "110%", "120%"]
APARENCIAS_DO_SISTEMA = ["Light", "Dark", "System"]

# Motor (engine) para manipulação de arquivos Excel
ENGINE = 'openpyxl'
