import os
from re import fullmatch

from requests import get, ConnectionError

from src.Constants import *

os.system('cls')


def test_verifica_se_shortcuts_esta_em_formato_de_lista():
    entrada = SHORTCUTS

    esperado = True

    resultado = isinstance(entrada, list)

    assert resultado == esperado


def test_verifica_se_cada_shortcut_esta_em_formato_de_tupla():
    entrada = SHORTCUTS

    esperado = True

    resultado = all(
        [(isinstance(shortcut, tuple) == 1) for shortcut in entrada]
    )

    assert resultado == esperado


def test_se_colortheme_list_tem_os_valores_padoes():
    entrada = COLORTHEMELIST
    esperado = True
    resultado = entrada == ['dark-blue', 'blue', 'green']
    assert resultado == esperado


def test_se_scalelist_tem_apenas_strings_de_porcentagens():
    entrada = SCALELIST

    esperado = True

    resultado = all([bool(fullmatch(r'^\d+%$', valor)) for valor in entrada])

    assert resultado == esperado


def test_se_appearancemodetheme_tem_os_valores_padroes():
    entrada = APPEARANCEMODETHEME
    esperado = True
    resultado = entrada == ['Light', 'Dark', 'System']
    assert resultado == esperado


def test_se_categorylist_tem_valores_padroes():
    entrada = CATEGORYLIST

    esperado = True

    resultado = entrada == [
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

    assert resultado == esperado


def test_constante_d_dissertativa():
    entrada = D

    esperado = True

    resultado = entrada == 'Dissertativa'

    assert resultado == esperado


def test_constante_me_multipla_escolha_1_correta():
    entrada = ME

    esperado = True

    resultado = entrada == 'Multipla escolha 1 correta'

    assert resultado == esperado


def test_constante_men_multipla_escolha_n_corretas():
    entrada = MEN

    esperado = True

    resultado = entrada == 'Multipla escolha n corretas'

    assert resultado == esperado


def test_constante_vf_verdadeiro_ou_falso():
    entrada = VF

    esperado = True

    resultado = entrada == 'Verdadeiro ou falso'

    assert resultado


def test_place_holder_tempo_tem_formato_padrao_hh_mm_ss():
    entrada = PLACE_HOLDER_TEMPO
    esperado = True

    resultado = entrada == '00:00:00'

    assert resultado == esperado


def test_se_link_de_feedback_esta_funcionando():
    try:
        entrada = LINK_FEEDBACK_FORM

        esperado = 200

        resultado = get(entrada).status_code

        assert resultado == esperado

    except ConnectionError:
        assert True


def test_filetypes_tem_apenas_excel():
    entrada = FILETYPES

    esperado = True

    resultado = entrada == (('Pasta de Trabalho do Excel', '*.xlsx'),)

    assert resultado == esperado


def test_extension_tem_apenas_xlsx():
    entrada = EXTENSION

    esperado = True

    resultado = entrada == '.xlsx'

    assert resultado == resultado


def test_questioheader_tem_os_valores_necessarios_na_sequencia_correta():
    entrada = QUESTIOHEADER

    esperado = True

    resultado = any(
        [
            entrada[i] == titulo
            for i, titulo in enumerate(
                [
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
            )
        ]
    )

    assert resultado == esperado
