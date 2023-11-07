TRANSPARENT = 'transparent'
RED = 'red'
DARKGRAY = ('GRAY66', 'GRAY37')
BLUE = ('#3B8ED0', '#1F6AA5')
HOVER_BLUE = ('#36719F', '#144870')
BORDER_BLUE = ('#3E454A', '#949A9F')
GREEN = ('#2CBE79', '#2FA572')
GRAY = ('GRAY81', 'GRAY20')

TABOPCAO = 'Opção'
TABAJUDA = 'Ajuda'
ADD = 'Adicionar'

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
    ('Voltar campos:', 'Ctrl + Shift + TAB ou Shift + TAB'),
]

COLORTHEMELIST = ['dark-blue', 'blue', 'green']

SCALELIST = [
    '80%',
    '85%',
    '90%',
    '95%',
    '100%',
    '105%',
    '110%',
    '115%',
    '120%',
]

APPEARANCEMODETHEME = ['Light', 'Dark', 'System']

CATEGORYLIST = [
    'Astec',
    'Comunicação',
    'Controle de acesso',
    'Energia',
    'Exportação',
    'Gestão',
    'Incêndio e iluminação',
    'Negócios',
    'Redes',
    'Segurança eletrônica',
    'Solar',
    'Soluções',
    'Varejo',
    'Verticais',
]

D = 'Dissertativa'
ME = 'Multipla escolha 1 correta'
MEN = 'Multipla escolha n corretas'
VF = 'Verdadeiro ou falso'
QUESTIONTYPELIST = [D, ME, MEN, VF]

PLACE_HOLDER_CODIGO = 'TELEC-PXXXX'
PLACE_HOLDER_TEMPO = '00:00:00'
PLACE_HOLDER_PESO = '1'

LINK_FEEDBACK_FORM = 'https://forms.office.com/r/xpjpRED6KK'

# Tipos de arquivo permitidos
FILETYPES = (('Pasta de Trabalho do Excel', '*.xlsx'),)

# Extensão padrão de arquivo
EXTENSION = '.xlsx'

EASY = 'Fácil'
MEDIUM = 'Médio'
HARD = 'Difícil'
DIFFICULTLIST = [EASY, MEDIUM, HARD]

MAX_CHARACTER_LIMIT = 255

QUESTIOHEADER = [
    'id',
    'tipo',
    'peso',
    'tempo',
    'controle',
    'pergunta',
    'alternativa',
    'correta',
    'categoria',
    'subcategoria',
    'dificuldade',
]

TYPESCONVERTER = {
    'me': ME,
    ME: 'me',
    'men': MEN,
    MEN: 'men',
    'vf': VF,
    VF: 'vf',
    'd': D,
    D: 'd',
}
