import re
from os.path import basename
from pathlib import Path
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror, showinfo, showwarning, askyesnocancel, askyesno

from customtkinter import *

from Modules import FILETYPES, DEFAULT_EXTENSION
from Modules.arquivo import Arquivos, Imagens
from Modules.configuracoes import Configs
from Modules.quadro_de_questoes.quadro_de_questoes import QuadroDeQuestoes
from Modules.painel_de_configuracoes import PainelDeConfiguracoes
from Modules.corretor_ortografico import PowerfullSpellChecker
from Modules.models.questao import ModeloQuestao
from Modules.models.caixa_de_texto import CaixaDeTexto
from Modules.atualizacao import Atualizacao


D = 'Dissertativa'
ME = 'Multipla escolha 1 correta'
MEN = 'Multipla escolha n corretas'
VF = 'Verdadeiro ou falso'


# noinspection PyAttributeOutsideInit
class Main(CTk, Configs):
    __version__ = 3.1
    __author__ = 'Edimar Freitas de Sá'
    __annotations__ = 'edimarfreitas95@gmail.com'

    def __init__(self):
        self.local = Path(__file__).resolve().parent
        self.caminho_arquivo: str = ''

        Configs.__init__(self, self.local)
        self.arquivos = Arquivos(self.local)
        self.imagens = Imagens(self.local)
        self.init_root()

        self.var_opcao_correta_radio_bt = IntVar()
        self.var_quantidade_de_questoes = StringVar()

        # Variaveis do perfil do usuario
        self.var_apagar_enunciado = BooleanVar()
        self.var_dark_mode = StringVar()
        self.var_escala_do_sistema = StringVar()
        self.var_nova_unidade_padrao = StringVar()

        self.bt_salvar: CTkButton
        self.bt_exportar: CTkButton
        self.bt_configs: CTkButton
        self.bt_rm_opcao: CTkButton
        self.bt_add_opcao: CTkButton
        self.options_frame: CTkFrame
        self.pergunta: CaixaDeTexto
        self.unidade: CTkOptionMenu
        self.tempo: CTkEntry
        self.codigo_do_curso: CTkEntry
        self.tipo: CTkOptionMenu
        self.dificuldade: CTkOptionMenu
        self.peso: CTkEntry

        self.questao_em_edicao: [ModeloQuestao, None] = None
        self.exportado: bool = True
        self.painel_de_configuracoes: PainelDeConfiguracoes
        self.corretor_ortografico = PowerfullSpellChecker(timeout=500, dicionario_pessoal=self.dicionario_pessoal)
        self.atualizador: Atualizacao

        self.init_frames()
        self.configure_form()
        self.init_binds()

        self.after(500, self.verifica_atualizacao)

    def init_root(self):
        CTk.__init__(self)
        self.abre_configuracoes_e_perfil()
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        largura_do_quadro = int(largura_tela * 0.95)
        altura_do_quadro = int(altura_tela * 0.9)
        x_inicial = int((largura_tela - largura_do_quadro) / 2)
        y_inicial = int((altura_tela - altura_do_quadro - 50) / 10)
        self.geometry(f'{largura_do_quadro}x{altura_do_quadro}+{x_inicial}+{y_inicial}')
        self.minsize(largura_do_quadro, altura_do_quadro)
        self.configure(**self.root_configs)
        self.set_titulo()

        set_default_color_theme('green')
        self.altera_escala_do_sistema(self.perfil_escala_do_sistema)

    def init_frames(self):
        n_question_frame = CTkFrame(self)
        n_question_frame.place(relx=0.01, rely=0.02, relwidth=0.08, relheight=0.19)
        self.create_n_questoes_frame_widgets(n_question_frame)

        question_configs_frame = CTkFrame(self)
        question_configs_frame.place(relx=0.1, relwidth=0.395, rely=0.02, relheight=0.19)
        self.create_question_configs_frame_widgets(question_configs_frame)

        question_frame = CTkFrame(self)
        question_frame.place(relx=0.01, rely=0.23, relwidth=0.485, relheight=0.19)
        self.create_question_frame_widgets(question_frame)

        texto_opcao_frame = CTkFrame(self)
        texto_opcao_frame.place(relx=0.01, rely=0.44, relwidth=0.485, relheight=0.46)
        self.create_options_frame_widgets(texto_opcao_frame)

        bts_frame = CTkFrame(self)
        bts_frame.place(relx=0.01, rely=0.92, relwidth=0.485, relheight=0.06)
        bts_frame.rowconfigure(0, weight=1)
        bts_frame.columnconfigure((1, 2), weight=3)
        self.create_bts_frame_widgets(bts_frame)

        self.create_questions_frame()

    def create_questions_frame(self):
        questions_frame = CTkFrame(self)
        questions_frame.place(relx=0.505, rely=0.02, relwidth=0.485, relheight=0.96)
        self.questions_board = QuadroDeQuestoes(questions_frame, self.imagens, **self.scrollable_label_configs)

    def create_n_questoes_frame_widgets(self, frame):
        CTkLabel(frame, textvariable=self.var_quantidade_de_questoes, **self.label_configs, wraplength=85).pack(
            expand=True)

    def create_question_configs_frame_widgets(self, frame):
        CTkLabel(frame, **self.label_configs, text='Unidade').grid(column=0, row=0, padx=20)
        self.unidade = CTkOptionMenu(frame, **self.list_configs, values=self.unidades, width=165,
                                     dynamic_resizing=False)
        self.unidade.grid(column=0, row=1, padx=20, pady=(0, 20))

        CTkLabel(frame, **self.label_configs, text='Código do curso').grid(column=1, row=0, padx=20)
        self.codigo_do_curso = CTkEntry(frame, **self.entry_configs, placeholder_text=f'TELEC-XXXX')
        self.codigo_do_curso.grid(column=1, row=1, padx=20, pady=(0, 20))

        CTkLabel(frame, **self.label_configs, text='Tempo de resposta').grid(column=2, row=0, padx=20)
        self.tempo = CTkEntry(frame, **self.entry_configs, placeholder_text='00:00:00')
        self.tempo.grid(column=2, row=1, padx=20, pady=(0, 20))

        CTkLabel(frame, **self.label_configs, text='Tipo da questão').grid(column=0, row=2, padx=20)
        self.tipo = CTkOptionMenu(frame, **self.list_configs, values=self.tipos, width=165,
                                  command=self.altera_alternativa, dynamic_resizing=False)
        self.tipo.grid(column=0, row=3, padx=20, pady=(0, 20))

        CTkLabel(frame, **self.label_configs, text='Dificuldade').grid(column=1, row=2, padx=20)
        self.dificuldade = CTkOptionMenu(frame, **self.list_configs, values=self.dificuldades,
                                         dynamic_resizing=False)
        self.dificuldade.grid(column=1, row=3, padx=20, pady=(0, 20))

        CTkLabel(frame, **self.label_configs, text='Peso da questão').grid(column=2, row=2, padx=20)
        self.peso = CTkEntry(frame, **self.entry_configs, placeholder_text='1')
        self.peso.grid(column=2, row=3, padx=20, pady=(0, 20))

    def create_question_frame_widgets(self, frame):
        CTkLabel(frame, **self.label_configs, text='Enunciado da questão').grid(row=0, column=0, padx=20)
        self.pergunta = CaixaDeTexto(frame, **self.text_configs, height=90)
        self.pergunta.grid(row=1, column=0, rowspan=2, padx=10, pady=10, ipadx=260)

        CTkLabel(frame, **self.label_configs, text='Opção').grid(row=0, column=1)
        self.bt_add_opcao = CTkButton(frame, **self.buttons_configs, text='+', command=self.add_alternativa,
                                      width=30, height=30)
        self.bt_add_opcao.grid(row=1, column=1, padx=10)
        self.bt_rm_opcao = CTkButton(frame, **self.buttons_configs, text='-',
                                     command=self.rm_alternativa, width=30, height=30)
        self.bt_rm_opcao.grid(row=2, column=1, padx=10)

    def create_options_frame_widgets(self, frame):
        CTkLabel(frame, text='Opções', **self.label_configs).place(relx=0.47, rely=0.01)

        for index in range(5):
            texto = CaixaDeTexto(frame, **self.text_configs, height=50)
            setattr(self, f'txt_opcao{index}', texto)
            self.corretor_ortografico.monitora_textbox(texto)

            rd_button = CTkRadioButton(frame, text='', value=index, variable=self.var_opcao_correta_radio_bt)
            setattr(self, f'rd_button_opcao{index}', rd_button)

            ck_button = CTkCheckBox(frame, text='')
            setattr(self, f'ck_button_opcao{index}', ck_button)

        self.contador_de_opcoes = 0

    def create_bts_frame_widgets(self, frame):
        self.bt_configs = CTkButton(frame, **self.buttons_configs, text='', width=30, height=30,
                                    image=self.imagens.bt_configs_img(), command=self.abre_menu_configuracoes)
        self.bt_configs.grid(column=0, row=0, pady=10, padx=5)

        self.bt_exportar = CTkButton(frame, **self.buttons_configs, text='Exportar', width=400, height=30,
                                     command=self.exportar)
        self.bt_exportar.grid(column=1, row=0, pady=10)

        self.bt_salvar = CTkButton(frame, **self.buttons_configs, text='Salvar', width=400, height=30,
                                   command=self.salvar)
        self.bt_salvar.grid(column=2, row=0, pady=10, padx=5)

    def configure_form(self):
        self.set_quantidade_de_questoes()
        self.corretor_ortografico.monitora_textbox(self.pergunta)
        self.after(100, self.pergunta.focus_set)
        self.unidade.set(self.configuracao_unidade_padrao)
        self.dificuldade.set(self.dificuldades[0])
        self.tipo.set(self.tipos[1])
        self.organiza_ordem_tabulacao()

    def abre_menu_configuracoes(self):
        busca = re.findall(r'(paineldeconfiguracoes)', ', '.join([str(widget) for widget in self.winfo_children()]))
        if busca:
            return self.painel_de_configuracoes.focus_force()

        self.painel_de_configuracoes = PainelDeConfiguracoes(self)

    def altera_dark_mode(self, modo: str):
        set_appearance_mode(modo)
        self.salva_informacao('perfil', 'dark_mode', self.var_dark_mode.get())

    def altera_escala_do_sistema(self, nova_escala):
        nova_escala_float = int(nova_escala.replace("%", "")) / 100
        set_widget_scaling(nova_escala_float)
        if getattr(self, 'var_escala_do_sistema', False):
            self.salva_informacao('perfil', 'escala_do_sistema', self.var_escala_do_sistema.get())

    def altera_opcao_apagar_enunciado(self):
        self.salva_informacao('perfil', 'apagar_enunciado', self.var_apagar_enunciado.get())

    def add_alternativa(self, texto_alternativa=None):
        if self.contador_de_opcoes == 5 or self.get_tipo == D:
            return

        texto: CaixaDeTexto = self.txt_opcao(self.contador_de_opcoes)
        texto.place(relx=0.01, rely=self.calcula_posicao_y(self.contador_de_opcoes), relwidth=0.92)

        if texto_alternativa:
            texto.insert(0.0, texto_alternativa)

        self.show_opcao(self.contador_de_opcoes)

        self.contador_de_opcoes += 1

    def rm_alternativa(self):
        if self.contador_de_opcoes:
            self.contador_de_opcoes -= 1
            texto: CaixaDeTexto = self.txt_opcao(self.contador_de_opcoes)
            texto.place_forget()

            ck_bt: CTkCheckBox = getattr(self, f'ck_button_opcao{self.contador_de_opcoes}')
            ck_bt.deselect()
            ck_bt.place_forget()

            rd_bt: CTkRadioButton = getattr(self, f'rd_button_opcao{self.contador_de_opcoes}')
            rd_bt.place_forget()

    def exportar(self):
        if not self.caminho_arquivo:
            self.caminho_arquivo = self.arquivos.caminho_salvar_para_salvar('Exportar para')

        retorno = self.arquivos.exportar(self.caminho_arquivo, self.questions_board.lista_de_questoes())
        if not retorno:
            showerror('Não foi possível exportar', 'Para exportar é necessário que o arqivo esteja fechado.'
                                                   '\nConfirme que nenhum arquivo xlsx com mesmo nome esteja aberto.')
        self.exportado = True
        showinfo('Exportado', 'O banco de dados foi criado com sucesso!')
        self.reseta_geral()

    def salvar(self):
        self.exportado = False

        if not self.get_pergunta or self.verifica_texto_opcoes():
            return showwarning('Pergunta em branco', 'Para salvar uma questão é necessário que a pergunta e as '
                                                     'alternativas ativas não esteja em branco.')

        if self.questao_em_edicao:
            self.salvar_edicao()
            return

        if self.questions_board.verifica_se_pergunta_ja_existe(self.get_pergunta):
            return showinfo('Pergunta repetida', 'Já existe uma questão com a mesma pergunta')

        questao = ModeloQuestao(self.get_unidade, self.get_codigo, self.get_tempo, self.get_tipo,
                                self.get_dificuldade, self.get_peso, self.get_pergunta, self.get_opcoes)
        self.questions_board.adiciona_questao(questao)
        self.set_quantidade_de_questoes()

        self.reseta_informacoes()

    def abrir(self):
        if self.contador_de_opcoes:
            resposta = askyesno(
                'Questão em edição',
                'Você tem questões em edição, deseja salva-la antes de abrir um novo arquivo?'
            )
            if resposta:
                self.salvar_como()

        self.reseta_question_board()
        self.exportado = True
        self.reseta_informacoes()

        self.caminho_arquivo = self.arquivos.buscar_arquivo_para_abrir()
        if not self.caminho_arquivo:
            return
        questoes = self.arquivos.carrega_banco_de_dados(self.caminho_arquivo)

        for questao in questoes:
            self.questions_board.adiciona_questao(questao)

        self.set_quantidade_de_questoes()
        self.set_titulo()

    def salvar_como(self):
        self.caminho_arquivo = self.arquivos.caminho_salvar_para_salvar('Salvar como')
        self.exportar()
        self.set_titulo()

    def seleciona_caminho(self, titulo: str):
        self.caminho_arquivo = asksaveasfilename(confirmoverwrite=True, defaultextension=DEFAULT_EXTENSION,
                                                 filetypes=FILETYPES, initialdir=self.local, title=titulo)

    def altera_unidade_padrao(self):
        nova_unidade = self.var_nova_unidade_padrao.get()
        self.unidade.set(nova_unidade)
        self.salva_informacao('perfil', 'unidade_padrao', nova_unidade)

    def altera_alternativa(self, e=None):
        quantidade_de_questoes = self.contador_de_opcoes
        for indice in range(quantidade_de_questoes):
            self.rm_alternativa()
        for indice in range(quantidade_de_questoes):
            self.add_alternativa()
        self.organiza_ordem_tabulacao()

    def set_titulo(self):
        self.title(f'Gerador de questões - {basename(self.caminho_arquivo)}' if self.caminho_arquivo else 'Gerador de questões')

    def set_quantidade_de_questoes(self):
        self.var_quantidade_de_questoes.set(f'Número de questões: '
                                            f'{self.questions_board.quantidade_de_questoes_registradas()}')

    def organiza_ordem_tabulacao(self):
        ordem_widgets = [
            self.codigo_do_curso,
            self.tempo,
            self.peso,
            self.pergunta,
        ]

        for widget in ordem_widgets:
            widget.lift()

    def get_opcao_bt(self, indice) -> [CTkRadioButton, CTkCheckBox]:
        def show_rd_bt() -> CTkRadioButton:
            rd_bt = getattr(self, f'rd_button_opcao{indice}')
            return rd_bt

        def show_ck_bt() -> CTkCheckBox:
            ck_bt = getattr(self, f'ck_button_opcao{indice}')
            return ck_bt

        def show_dissert():
            pass

        tipos_btn = {
            ME: show_rd_bt,
            MEN: show_ck_bt,
            VF: show_ck_bt,
            D: show_dissert
        }
        return tipos_btn[self.get_tipo]()

    def show_opcao(self, indice):
        pos_y = self.calcula_posicao_y(indice) + 0.04
        pos_x = 0.95

        self.get_opcao_bt(indice).place(relx=pos_x, rely=pos_y)

    def editar_questao(self, questao: ModeloQuestao):
        self.reseta_informacoes()
        self.questao_em_edicao = questao
        self.codigo_do_curso.insert(0, questao.codigo)
        self.tempo.insert(0, questao.tempo)
        self.tipo.set(questao.tipo)
        self.dificuldade.set(questao.dificuldade)
        self.peso.insert(0, questao.peso)
        self.pergunta.insert(0.0, questao.pergunta)
        for alternativa, correta in questao.alternativas:
            self.add_alternativa(alternativa)
            if correta:
                opcao_bt = self.get_opcao_bt(self.contador_de_opcoes - 1)
                opcao_bt.select()

    @property
    def get_opcoes(self) -> list[tuple[str, bool]]:
        def verifica_correta(botao, indice):
            if self.get_tipo == ME:
                return self.var_opcao_correta_radio_bt.get() == indice
            return botao.get()

        opcoes = list()
        for indice in range(self.contador_de_opcoes):
            texto: CaixaDeTexto = self.txt_opcao(indice)
            alternativa = texto.get_texto_completo()
            correta = verifica_correta(self.get_opcao_bt(indice), indice)
            opcoes.append((alternativa, correta))
        return opcoes

    @property
    def get_tipo(self):
        return self.tipo.get()

    @property
    def get_unidade(self):
        return self.unidade.get()

    @property
    def get_codigo(self):
        return self.codigo_do_curso.get()

    @property
    def get_tempo(self):
        tempo = self.tempo.get()
        if not tempo:
            tempo = '00:00:00'
        return tempo

    @property
    def get_dificuldade(self):
        return self.dificuldade.get()

    @property
    def get_peso(self):
        peso = self.peso.get()
        if not peso:
            peso = 1
        return peso

    @property
    def get_pergunta(self):
        return self.pergunta.get_texto_completo()

    @staticmethod
    def calcula_posicao_y(multiplo):
        return (0.18 * multiplo) + 0.1

    def reseta_informacoes(self):
        self.unidade.set(self.configuracao_unidade_padrao)
        self.codigo_do_curso.delete(0, 'end')
        self.tempo.delete(0, 'end')
        self.peso.delete(0, 'end')
        self.var_opcao_correta_radio_bt.set(0)

        if self.var_apagar_enunciado:
            self.pergunta.delete(0.0, 'end')

        for indice in range(5):
            self.txt_opcao(indice).delete(0.0, 'end')
            self.rm_alternativa()

        self.pergunta.focus()
        self.set_quantidade_de_questoes()

    def salvar_edicao(self):
        self.questao_em_edicao.unidade = self.get_unidade
        self.questao_em_edicao.codigo = self.get_codigo
        self.questao_em_edicao.tempo = self.get_tempo
        self.questao_em_edicao.tipo = self.get_tipo
        self.questao_em_edicao.dificuldade = self.get_dificuldade
        self.questao_em_edicao.peso = self.get_peso
        self.questao_em_edicao.pergunta = self.get_pergunta
        self.questao_em_edicao.alternativas = self.get_opcoes

        self.questions_board.editar_questao(self.questao_em_edicao)

        self.questao_em_edicao = None
        self.reseta_informacoes()

    def init_binds(self):
        def ctrl_events(e):
            key = str(e.keysym).lower()

            def seleciona_tipo(indice: int):
                self.tipo.set(self.tipos[indice])
                self.altera_alternativa()

            def seleciona_dificuldade(indice: int):
                self.dificuldade.set(self.dificuldades[indice - 4])

            events = {
                'e': self.exportar,
                's': self.salvar,
                'o': self.abrir,
                'equal': self.add_alternativa,
                'plus': self.add_alternativa,
                'minus': self.rm_alternativa,
                '1': seleciona_tipo,
                '2': seleciona_tipo,
                '3': seleciona_tipo,
                '4': seleciona_dificuldade,
                '5': seleciona_dificuldade,
                '6': seleciona_dificuldade,
            }

            if key in events:
                if key.isdigit():
                    return events[key](int(key))
                else:
                    return events[key]()

        def key_events(e):
            key = e.keysym
            events = {
                'F1': self.abre_atalhos,
                'F4': self.evento_de_fechamento_da_tela,
                'F12': self.salvar_como,
            }
            if key in events.keys():
                return events[key]()

        self.bind('<Control-KeyRelease>', ctrl_events)
        self.bind('<KeyRelease>', key_events)
        self.protocol(self.protocol()[0], self.evento_de_fechamento_da_tela)

    def evento_de_fechamento_da_tela(self):
        if not self.exportado:
            tittle = 'Salvamento pendente'
            information = 'Uma ou mais questões estão em edição e não foram exportadas.\n' \
                          'Deseja exportar as alterações antes de sair?'
            resposta = askyesnocancel(tittle, information)
            if resposta is None:  # Se resposta for cancelar
                return
            elif resposta:  # Se resposta for sim
                self.exportar()
        # Se resposta for não ou se arquivo já estiver sido exportado
        self.quit()

    def abre_atalhos(self):
        self.abre_menu_configuracoes()
        self.painel_de_configuracoes.abre_ajuda()

    def reseta_question_board(self):
        self.questions_board.destroy()
        self.create_questions_frame()

    def reseta_geral(self):
        self.reseta_informacoes()
        self.reseta_question_board()
        self.caminho_arquivo = None
        self.questao_em_edicao = None
        self.set_titulo()
        self.set_quantidade_de_questoes()

    def verifica_digito(self, keysym):
        pass

    def verifica_atualizacao(self):
        if not getattr(self, 'atualizador', False):
            self.atualizador = Atualizacao(self.__version__, self.local)

        resposta = None
        if self.atualizador.atualizacao:
            resposta = askyesno(
                'Nova atualização disponível',
                f'O programa está atualmente na versão {self.__version__}.\n'
                f'A versão disponível é a {self.atualizador.versao_recente}.\n'
                f'Deseja atualizar agora?'
            )

        if resposta:
            self.atualizador.atualiza()
            self.after(1200, self.evento_de_fechamento_da_tela)

    def verifica_texto_opcoes(self):
        if self.get_tipo == D:
            return False
        for indice in range(self.contador_de_opcoes):
            opcao: CaixaDeTexto = self.txt_opcao(indice)
            texto = opcao.get_texto_completo()
            if not texto:
                return True
        return False

    def txt_opcao(self, indice):
        return getattr(self, f'txt_opcao{indice}')


if __name__ == '__main__':
    app = Main()
    app.mainloop()
