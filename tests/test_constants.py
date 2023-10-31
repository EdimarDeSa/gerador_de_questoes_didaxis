from re import fullmatch

from requests import get

from src.Constants import *


def test_verifica_se_shortcuts_esta_em_formato_de_lista():
    entrada = SHORTCUTS
    esperado = list
    resultado = isinstance(entrada, esperado)
    assert resultado


def test_verifica_se_cada_shortcut_esta_em_formato_de_tupla():
    entrada = SHORTCUTS
    esperado = True
    resultado = all([(isinstance(shortcut, tuple) == 1) for shortcut in entrada]) == esperado
    assert resultado


def test_se_colortheme_list_tem_os_valores_padoes():
    entrada = COLORTHEMELIST
    esperado = ['dark-blue', 'blue', 'green']
    resultado = entrada == esperado
    assert resultado


def test_se_scalelist_tem_apenas_strings_de_porcentagens():
    entrada = SCALELIST
    esperado = True
    resultado = all([bool(fullmatch(r'^\d+%$', valor)) for valor in entrada]) == esperado
    print(resultado)
    assert resultado


def test_se_appearancemodetheme_tem_os_valores_padroes():
    entrada = APPEARANCEMODETHEME
    esperado = ['Light', 'Dark', 'System']
    resultado = entrada == esperado
    assert resultado


def test_se_categorylist_tem_valores_padroes():
    entrada = CATEGORYLIST
    esperado = ['Astec', 'Comunicação', 'Controle de acesso', 'Energia', 'Exportação', 'Gestão',
                'Incêndio e iluminação', 'Negócios', 'Redes', 'Segurança eletrônica', 'Solar',
                'Soluções', 'Varejo', 'Verticais',]
    resultado = entrada == esperado
    assert resultado


def test_constante_d_dissertativa():
    entrada = D
    esperado = 'Dissertativa'
    resultado = entrada == esperado
    assert resultado


def test_constante_me_multipla_escolha_1_correta():
    entrada = ME
    esperado = 'Multipla escolha 1 correta'
    resultado = entrada == esperado
    assert resultado


def test_constante_men_multipla_escolha_n_corretas():
    entrada = MEN
    esperado = 'Multipla escolha n corretas'
    resultado = entrada == esperado
    assert resultado


def test_constante_vf_verdadeiro_ou_falso():
    entrada = VF
    esperado = 'Verdadeiro ou falso'
    resultado = entrada == esperado
    assert resultado


def test_place_holder_tempo_tem_formato_padrao_hh_mm_ss():
    entrada = PLACE_HOLDER_TEMPO
    esperado = '00:00:00'
    resultado = entrada == esperado
    assert resultado


def test_se_link_de_feedback_esta_funcionando():
    entrada = LINK_FEEDBACK_FORM
    esperado = 200
    resultado = get(entrada).status_code == esperado
    assert resultado


def test_filetypes_tem_apenas_excel():
    entrada = FILETYPES
    esperado = (('Pasta de Trabalho do Excel', '*.xlsx'),)
    resultado = entrada == esperado
    assert resultado


def test_extension_tem_apenas_xlsx():
    entrada = EXTENSION
    esperado = '.xlsx'
    resultado = entrada == esperado
    assert resultado


def test_questioheader_tem_os_valores_necessarios_na_sequencia_correta():
    entrada = QUESTIOHEADER
    esperado = [
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
    resultado = any([entrada[i] == titulo for i, titulo in enumerate(esperado)])
    assert resultado
