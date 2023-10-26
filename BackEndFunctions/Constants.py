#TODO: Remove não necessárias

# Configurações para codificação de caracteres
ENCODER: str = 'UTF-8'
BINARY_PROTOCOL = 5


# Modo de abertura de arquivo
JSON_READER: str = 'r'
JSON_WRITER: str = 'w'
BINARY_WRITER: str = 'wb'
BINARY_READER: str = 'rb'


# Cosmetics
FONTFAMILY = 'Roboto'


# Subcategorias
FACIL = 'Fácil'
MEDIO = 'Médio'
DIFICIL = 'Difícil'
SUBCATEGORYLIST = [FACIL, MEDIO, DIFICIL]


# Unidades de negócio
ASTEC = 'astec'
COMUNICACAO = 'Comunicação'
CONTROLE = 'Controle de acesso'
ENERGIA = 'Energia'
EXPORTACAO = 'Exportação'
GESTAO = 'Gestão'
INCENDIO = 'Incêndio e iluminação'
NEGOCIOS = 'Negócios'
REDES = 'Redes'
SEGURANCA = 'Segurança eletrônica'
SOLAR = 'Solar'
SOLUCOES = 'Soluções'
VAREJO = 'Varejo'
VERTICAIS = 'Verticais'
UNIDADES = [ASTEC, COMUNICACAO, CONTROLE, ENERGIA, EXPORTACAO, GESTAO, INCENDIO, NEGOCIOS, REDES, SEGURANCA, SOLAR,
            SOLUCOES, VAREJO, VERTICAIS]


# Constantes para tipos de questão
D = 'Dissertativa'
ME = 'Multipla escolha 1 correta'
MEN = 'Multipla escolha n corretas'
VF = 'Verdadeiro ou falso'
TYPESLIST = [D, ME, MEN, VF]


# Constantes para respostas
V = 'V'
F = 'F'
CORRETA = 'CORRETA'
ERRADA = ''


# Link para o formulário de feedback
LINK_FEEDBACK_FORM = 'https://forms.office.com/r/xpjpRED6KK'


# Tipos de arquivo permitidos
FILETYPES = (('Pasta de Trabalho do Excel', '*.xlsx'),)

# Extensão padrão de arquivo
EXTENSION = '.xlsx'


# Cabeçalhos das colunas
CABECALHO_DIDAXIS = ['ID', 'TIPO', 'PESO', 'TEMPO', 'CONTROLE', 'PERGUNTA', 'ALTERNATIVA', 'CORRETA',
                     'CATEGORIA', 'SUBCATEGORIA', 'DIFICULDADE']
# TODO: Verificar necessidade ao finalizar tudo
CABECALHO_DIDAXIS_LOWER = ['id_', 'tipo', 'peso', 'tempo', 'controle', 'pergunta', 'alternativas',
                           'categoria', 'subcategoria', 'dificuldade']
CABECALHO_PERGUNTA = ['ID', 'TIPO', 'PESO', 'TEMPO', 'CONTROLE', 'PERGUNTA', 'CATEGORIA', 'SUBCATEGORIA', 'DIFICULDADE']
CABECALHO_ALTERNATIVAS = ['ALTERNATIVA', 'CORRETA']


# Placeholders
PLACE_HOLDER_CODIGO = 'TELEC-PXXXX'
PLACE_HOLDER_TEMPO = '00:00:00'
PLACE_HOLDER_PESO = '1'


# Outras constantes
ADD = 'Adicionar'


# Motor (engine) para manipulação de arquivos Excel
ENGINE = 'openpyxl'


