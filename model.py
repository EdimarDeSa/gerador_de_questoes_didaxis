from icecream import ic


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
CATEGORYLIST = [ASTEC, COMUNICACAO, CONTROLE, ENERGIA, EXPORTACAO, GESTAO, INCENDIO, NEGOCIOS, REDES, SEGURANCA, SOLAR,
                SOLUCOES, VAREJO, VERTICAIS]

# Constantes para tipos de questão
D = 'Dissertativa'
ME = 'Multipla escolha 1 correta'
MEN = 'Multipla escolha n corretas'
VF = 'Verdadeiro ou falso'
TYPELIST = [D, ME, MEN, VF]

# Subcategorias
FACIL = 'Fácil'
MEDIO = 'Médio'
DIFICIL = 'Difícil'
SUBCATEGORYLIST = [FACIL, MEDIO, DIFICIL]


# Theme settings
COLORTHEMELIST = ['dark-blue', 'blue', 'green']
SCALESTHEMELIST = ['80%', '90%', '100%', '110%', '120%', '130%', '140%', '150%']
APPEARANCEMODETHEME = ["Light", "Dark", "System"]


class Model:
    # User settings
    titles_font_settings = {'font': ('Roboto', 15, 'bold')}
    default_font_settings = {'font': ('Roboto', 12)}
    user_color_theme = COLORTHEMELIST[2]
    user_scaling = SCALESTHEMELIST[2]
    user_appearance_mode = APPEARANCEMODETHEME[2]

    # Options list
    category_options = CATEGORYLIST
    question_type_list = TYPELIST
    difficulty_list = SUBCATEGORYLIST

    def __init__(self):
        pass
