from customtkinter import *

from Modules.arquivos import Arquivos
from Modules.configuracoes import Configuracoes
from Modules.constants import *
from Modules.perfil import Perfil
from Modules.imagens import Imagens
from Modules.models.caixa_de_texto import CaixaDeTexto
from Modules.models.questao import ModeloQuestao
from Modules.corretor_ortografico import CorretorOrtografico


class VariaveisGlobais:
    def __init__(self, arquivos: Arquivos, configs: Configuracoes, perfil: Perfil, imagens: Imagens):
        # Geral
        self.arquivos = arquivos
        self.configs = configs
        self.perfil = perfil
        self.imagens = imagens

        # Variáveis de perfil
        self.var_unidade_padrao = None
        self.var_apagar_enunciado: BooleanVar | None = None
        self.var_dark_mode: StringVar | None = None
        self.altera_escala_do_sistema = None

        # Variáveis de controle
        self.contador_de_opcoes: IntVar | None = None
        self.questao_em_edicao: ModeloQuestao | None = None
        self.opcao_correta_radio_bt: IntVar | None = None
        self.display_quantidade_de_questoes: IntVar | None = None
        self.exportado: BooleanVar | None = None

        # Funcoes de Controle
        self.cmd_add_alternativa = None
        self.cmd_rm_alternativa = None
        self.cmd_reseta_informacoes = None
        self.cmd_editar_questao = None
        self.cmd_delete_event = None
        self.cmd_exit: None = None
        self.cmd_salver_como: None = None
        self.cmd_abrir: None = None
        self.corretor_ortografico: CorretorOrtografico | None = None

        # Campos da questao
        self.campo_unidade: CTkOptionMenu | None = None
        self.campo_codigo_do_curso: CTkEntry | None = None
        self.campo_tempo: CTkEntry | None = None
        self.campo_tipo: CTkOptionMenu | None = None
        self.campo_dificuldade: CTkOptionMenu | None = None
        self.campo_peso: CTkEntry | None = None
        self.campo_pergunta: CaixaDeTexto | None = None
        self.lista_txt_box: list[CaixaDeTexto | None] | None = None
        self.lista_rd_bts: list[CTkRadioButton | None] | None = None
        self.lista_ck_bts: list[CTkCheckBox | None] | None = None

        # Quadro de questões
        self.quadro_de_questoes = None
