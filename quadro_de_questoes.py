from tkinter import Toplevel
from tkinter.ttk import Treeview, Frame

from os.path import exists

from back_end import BackEnd


class Questoes(BackEnd):
    def abre_quadro_questoes(self):
        # Inicia a janela de top level
        self.cria_janela()
        # Inicia o Frame dos widgets
        self.cria_frame()
        # Inicia a treeview
        self.cria_tree_view()

        self.add_infos_na_tabela()

    def cria_janela(self):
        # Cria um objeto que será nossa janela
        top_lvl = Toplevel(master = self.root)
        # Defini o nome da janela
        top_lvl.title("Questões")
        # Define o tamanho e posicionamento da janela na tela do usuário
        top_lvl.geometry(
            f"{int(self.largura_tela(top_lvl) * 1.05)}x{self.altura_tela(top_lvl)}+{self.largura_tela(top_lvl)}+0"
        )
        # Define a cor de fundo da janela
        top_lvl.configure(**self.root_param)

        top_lvl.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.top_lvl = top_lvl

    def disable_event(self):
        pass

    def cria_frame(self):
        self.frame = Frame(self.top_lvl)
        self.frame.place(relx = 0.02, rely = 0.03, relwidth = 0.96, relheight = 0.94)

    def cria_tree_view(self):
        self.tree_view = Treeview(self.frame, selectmode = 'browse', show = 'tree headings')

        # Cria as colunas
        self.tree_view['columns'] = ('Pergunta', 'Tipo', 'Unidade')

        # Formata as colunas
        self.tree_view.column("#0", width = 50, minwidth = 20)
        self.tree_view.column("#1", anchor = 'w', width = 300)
        self.tree_view.column("#2", anchor = 'center', width = 50)
        self.tree_view.column("#3", anchor = 'w', width = 100)

        # Define os cabeçalhos das colunas
        self.tree_view.heading("#0", text = "Opções", anchor = 'w')
        self.tree_view.heading("#1", text = "Pergunta", anchor = 'w')
        self.tree_view.heading("#2", text = "Tipo", anchor = 'center')
        self.tree_view.heading("#3", text = "Dificuldade", anchor = 'w')

        self.tree_view.pack(side = 'left', fill = 'both', expand = True)

        self.tree_view.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, _):
        self.limpa_formulario()
        # Puxa o número do iid registrado no momento na treeview para indicar qual linha será lida inicialmente
        # Posteriormente qual linha será editada

        selecao = self.tree_view.selection()[0]

        if not self.tree_view.parent(f'{selecao}'):
            self.linha = index = int(selecao)
        else:
            self.linha = index = int(self.tree_view.parent(f'{selecao}'))

        # Carrega informações que serão escritas no cabeçalho do formulário e retorna a pergunta
        pergunta = self.carrega_cabecalho_para_edicao(index)

        # Conta a quantidade de opções a serem carregadas
        quantidade_opcoes_atual = len(self.tree_view.get_children(str(index)))
        quantidade_opcoes = len(self.tree_view.get_children(str(index)))

        for opcao in range(quantidade_opcoes):
            infos = self.carrega_linha(index + opcao)
            if infos[5] != pergunta:
                break

            self.add_alternativa()
            self.seleciona_correta(infos[1], infos[7])
            self.list_opcoes[len(self.list_opcoes) - 1].insert(0, infos[6])

    def seleciona_correta(self, tipo, correta):
        tipos = {
            'me':  self.seleciona_me,
            'men': self.seleciona_men,
            'vf':  self.seleciona_vf
        }
        return tipos[tipo.lower()](correta)

    def seleciona_me(self, correta):
        if correta:
            return self.rad_bt.select()

    def seleciona_men(self, correta):
        if correta:
            return self.ck_bt.select()

    def seleciona_vf(self, correta):
        if correta == 'V':
            return self.ck_bt.select()

    def limpa_formulario(self):
        self.root.children['frame_infos'].children['codigo_curso'].delete(0, 'end')
        self.root.children['frame_infos'].children['tempo'].delete(0, 'end')
        self.root.children['frame_infos'].children['peso'].delete(0, 'end')
        self.root.children['frame_infos'].children['pergunta'].delete(0.0, 'end')
        self.reset_opcs()

    def carrega_cabecalho_para_edicao(self, index):
        frame_info_child = self.root.children['frame_infos'].children
        linha_a_carregar = self.carrega_linha(index)
        # self.unidades = list()
        frame_info_child['unidade'].current(self.unidades.index(linha_a_carregar[8]))
        frame_info_child['codigo_curso'].insert(
            0, '' if str(linha_a_carregar[9]) == 'None' else str(linha_a_carregar[9])
        )
        frame_info_child['tempo'].insert(0, '' if not linha_a_carregar[3] else linha_a_carregar[3])
        frame_info_child['tipo'].current(self.verifica_id_tipo(linha_a_carregar[1]))
        frame_info_child['dificuldade'].current(self.verifica_id_dificuldade(linha_a_carregar[10]))
        frame_info_child['peso'].insert(0, linha_a_carregar[2])
        frame_info_child['pergunta'].insert(0.0, linha_a_carregar[5])
        return linha_a_carregar[5]

    @staticmethod
    def verifica_id_tipo(tipo):
        tipos = {'me': 0, 'men': 1, 'vf': 2}
        return tipos[tipo.lower()]

    @staticmethod
    def verifica_id_dificuldade(dificuldade):
        dificuldades = {
            'fácil':   0, 'facil': 0,
            'médio':   1, 'média': 1, 'medio': 1, 'media': 1,
            'difícil': 2, 'dificil': 2,
        }
        return dificuldades[dificuldade.lower()]

    def add_infos_na_tabela(self):
        numero_de_questoes = 0
        index = 2
        par = ultima_pergunta = ''
        while True:
            infos = self.carrega_linha(index)
            pergunta = infos[5]
            if not pergunta:
                break
            elif ultima_pergunta != pergunta:
                par = ''
                self.add_parent(infos[1], pergunta, infos[10], par, index)
                par = index
                self.add_parent('<-- opcao', infos[6], infos[7], par, index + 0.1)
                numero_de_questoes += 1
            else:  # ultima_pergunta == pergunta
                self.add_parent('<-- opcao', infos[6], infos[7], par, index)

            index += 1
            ultima_pergunta = pergunta


        self.root.children['frame_infos'].children['numero_questao'].config(
            text = f'Questões:\n'
                   f'      {numero_de_questoes}     '
        )

    def add_parent(self, tipo, pergunta, dificuldade, par, index):
        self.tree_view.insert(par, 'end', iid = index, text = "", values = (pergunta, tipo, dificuldade))

    def reset_infos(self):
        self.tree_view.delete(*self.tree_view.get_children())

    def refresh_infos(self):
        self.reset_infos()
        self.add_infos_na_tabela()
