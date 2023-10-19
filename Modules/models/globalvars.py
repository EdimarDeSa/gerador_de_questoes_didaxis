from pathlib import Path

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
        self.var_unidade_padrao = StringVar(value=self.perfil.unidade_padrao)
        self.var_apagar_enunciado: BooleanVar = BooleanVar(value=self.perfil.apagar_enunciado)
        self.var_exportar_automaticamente: BooleanVar = BooleanVar(value=False)
        self.var_dark_mode: StringVar = StringVar(value=self.perfil.aparencia_do_sistema)

        # Variáveis de controle
        self.caminho_atual: Path | None = None
        self.contador_de_opcoes: IntVar = IntVar(value=0)
        self.questao_em_edicao: ModeloQuestao | None = None
        self.opcao_correta_radio_bt: IntVar = IntVar(value=0)
        self.display_quantidade_de_questoes: IntVar = IntVar(value=0)
        self.exportado: bool = True

        # Funcoes de Controle
        self.corretor_ortografico: CorretorOrtografico | None = None
        self.reseta_informacoes = None
        self.add_alternativa = None
        self.rm_alternativa = None
        self.editar_questao = None
        self.delete_event = None
        self.exportar = None
        self.exit = None
        self.atualiza_titulo = None

        # Campos da questao
        self.unidade: CTkOptionMenu | None = None
        self.codigo_do_curso: CTkEntry | None = None
        self.tempo: CTkEntry | None = None
        self.tipo: CTkOptionMenu | None = None
        self.dificuldade: CTkOptionMenu | None = None
        self.peso: CTkEntry | None = None
        self.pergunta: CaixaDeTexto | None = None
        self.lista_txt_box: list[CaixaDeTexto | None] = list()
        self.lista_rd_bts: list[CTkRadioButton | None] = list()
        self.lista_ck_bts: list[CTkCheckBox | None] = list()

        # Quadro de questões
        self.quadro_de_questoes = None