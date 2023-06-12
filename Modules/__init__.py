__all__ = ['atualizacao', 'configuracoes', 'corretor_ortografico', 'arquivo', 'quadro_de_questoes',
           'models']

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
    'unidade_padrao': 'Comunicação',
    'apagar_enunciado': False,
    'aparencia_do_sistema': 'System',
}

ENCODER: str = 'UTF-8'

CABECALHO: list[str] = [
    'ID', 'TIPO', 'PESO', 'TEMPO', 'CONTROLE', 'PERGUNTA', 'ALTERNATIVA',
    'CORRETA', 'CATEGORIA', 'SUBCATEGORIA', 'DIFICULDADE'
]
