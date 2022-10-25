from subprocess import call
from tkinter import Tk, Frame, Label, Menu
from tkinter import Entry, Text, Button, Checkbutton, Radiobutton
from tkinter import BooleanVar, IntVar
from tkinter.ttk import Combobox
from tkinter.messagebox import askquestion, showerror

from configuracoes import Configs
from quadro_de_questoes import Questoes
from selecao_de_diretorio import SelecionaPasta as sp


class PlaceHolder(Entry):
    def __init__(self, master=None, placeholder="Texto padrão", color='gray30', **kw):
        super().__init__(master, kw)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", lambda e: self.foc_in())
        self.bind("<FocusOut>", lambda e: self.foc_out())

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self):
        if not self.get():
            self.put_placeholder()


class FuncoesFrontEnd:
    @staticmethod
    def largura_tela(root):
        return int(root.winfo_screenwidth() / 2.15)

    @staticmethod
    def altura_tela(root):
        return int(root.winfo_screenheight() / 1.1)

    def altera_tipo_opcao(self):
        self.frame_bts.destroy()
        self.inicia_frame_bts()
        # Reseta a lista de referências de respostas corretas
        self.list_corretas.clear()
        # Reseta a lista de botões de opções
        self.list_bt_corretas.clear()
        # Reseta valor do RadioButton, para que novas questões reiniciem os valores
        self.valor_radio_button = 0
        # Redefine posicionamento inicial dos botões de correta
        self.rely_bts = 0

        # Inicia botões de correta pelo número de alternativas já criadas
        self.frame_bts.after(250, self.repoe_bts_opcoes)

    def repoe_bts_opcoes(self):
        for _ in self.list_opcoes:
            self.tipo_alternativa()
        return

    def add_alternativa(self):
        # Cria variável da Entry das opções
        entrada = Entry(master = self.frame_opcs)
        # Posiciona a Entry das opções
        entrada.place(relx = 0.05, rely = self.rely_entry_opcoes, relwidth = 0.85)

        # Adiciona a referência da variável da entry na lista de variáveis correspondente
        self.list_opcoes.append(entrada)
        # Executa a criação de botão conforme o tipo da questão
        self.tipo_alternativa()
        # Adiciona distância no eixo 'Y' para a próxima caixa que será criada
        self.rely_entry_opcoes += 0.09

    def tipo_alternativa(self):
        # Primeira verificação do tipo da questão
        tipos = {
            'Multipla escolha 1 correta':  self.cria_radio_bt,
            'Multipla escolha n corretas': self.cria_check_bt,
            'Verdadeiro ou falso':         self.cria_check_bt
        }
        tipo = self.root.children['frame_infos'].children['tipo'].get()
        tipos[tipo]()
        self.rely_bts += 0.09

    def cria_radio_bt(self):
        # Cria botão para seleção de alternativa correta no modo RadioButton
        self.rad_bt = Radiobutton(
            master = self.frame_bts,
            value = self.valor_radio_button,
            variable = self.var_radio_button,
            **self.buttons_param,
        )
        # Posiciona os botões no Frame de opções
        self.rad_bt.place(relx = 0, rely = self.rely_bts)
        # Adiciona 1 no valor do próximo botão criado
        self.valor_radio_button += 1
        self.list_bt_corretas.append(self.rad_bt)

    def cria_check_bt(self):
        # Cria variável para se a resposta é a correta
        correta = BooleanVar()
        # Cria botão para seleção de alternativa correta no modo CheckButton
        self.ck_bt = Checkbutton(
            master = self.frame_bts,
            variable = correta,
            **self.buttons_param,
        )
        # Posiciona os botões no Frame de opções
        self.ck_bt.place(relx = 0, rely = self.rely_bts)
        # Adiciona a referência da variável do botão na lista de variáveis correspondente
        self.list_corretas.append(correta)
        self.list_bt_corretas.append(self.ck_bt)

    def remove_alternativa(self):
        if self.rely_entry_opcoes > 0.05:
            self.rely_entry_opcoes -= 0.09
            self.rely_bts -= 0.09
        else:
            self.rely_entry_opcoes = 0
            self.rely_bts = 0

        if self.valor_radio_button:
            self.valor_radio_button -= 1

        if self.list_opcoes:
            self.list_opcoes[len(self.list_opcoes) - 1].place_forget()
            self.list_opcoes.pop()

        if self.list_bt_corretas:
            self.list_bt_corretas[len(self.list_bt_corretas) - 1].place_forget()
            self.list_bt_corretas.pop()

        if self.list_corretas:
            self.list_corretas.pop()

    def salvar(self):
        if not self.verifica_informacoes():
            return self.faltam_informacoes()

        fram_info_get = self.root.children['frame_infos'].children
        # Cria dicionário para ser repassado ao back end
        api_dict = {
            'Tipo':         fram_info_get['tipo'].get(),
            'Peso':         fram_info_get['peso'].get(),
            'Tempo':        fram_info_get['tempo'].get(),
            'Pergunta':     self.perguntas,
            'Alternativa':  self.lista_alternativas,
            'Correta':      self.listar_corretas(),
            'Categoria':    fram_info_get['unidade'].get(),
            'SubCategoria': fram_info_get['codigo_curso'].get(),
            'Dificuldade':  fram_info_get['dificuldade'].get(),
            'linha':        self.linha,
            'diretorio':    self.diretorio
        }
        # Envia informações para back end
        self.gravar(api_dict)

        # Limpa dicionário após salvar no excel
        api_dict.clear()

        # Limpa formulário de opções para nova questão e TextBox
        self.reset_opcs()

        self.refresh_infos()

    # Verrifica se existe algo no campo de pergunta e opções
    def verifica_informacoes(self):
        self.perguntas = self.root.children['frame_infos'].children['pergunta'].get('0.0', 'end').rstrip('\n')
        if not self.perguntas:
            return False

        # Cria uma lista verificando se cada uma das entrys de opções estão preenchidas
        self.lista_alternativas = [opc.get() for opc in self.list_opcoes]
        if '' in self.lista_alternativas:
            return False

        return True

    @staticmethod
    def faltam_informacoes():
        # Se encontrarmos algum False, retorna a messagebox de atenção
        showerror(
            title = 'Falha na estrutura',
            message = '''
            Não será possível prosseguir \n 
            com a gravação da questão, \n
            existem informações faltando.
             '''
        )

    def listar_corretas(self):
        tipo = self.root.children['frame_infos'].children['tipo'].get()
        if tipo == self.tipos[0]:
            return self.var_radio_button.get()
        else:
            return [correta.get() for correta in self.list_corretas]

    @staticmethod
    def abre_feedback():
        return call(
            'start https://forms.office.com/Pages/ResponsePage.aspx?id='
            'M083D5gGVkaWZUrSp05YCkZTqk471oVCrP11vG53XR5UN1FQM1c0VlVHNk0xRUZQR0RROE5FT1pHQS4u',
            shell = True,
            stdout = False,
        )

    def reset_opcs(self):
        # Destroy o frame de opções e todos os widgets vinculados a ele
        self.frame_opcs.destroy()
        # # Destroy o frame dos botões de seleção da opção correta
        self.frame_bts.destroy()

        # Reseta o parâmetro de posicionamento 'y' das entrys de opções
        self.rely_entry_opcoes = 0
        self.linha = None
        # Reseta o parâmetro de posicionamento 'y' dos botões de opções
        self.rely_bts = 0

        # Reseta a lista de referências de opções
        self.list_opcoes.clear()
        # Reseta a lista de referências de respostas corretas
        self.list_corretas.clear()
        # Reseta a lista de botões de opções
        self.list_bt_corretas.clear()
        # Reseta valor do RadioButton, para que novas questões reiniciem os valores
        self.valor_radio_button = 0

        # Inicia novamente os frames das opções
        self.inicia_frames_opcoes()

        # Reseta o dicionário da api para integração com Back End
        self.connector_dict.clear()

    @staticmethod
    def selecionar_arquivo_pasta():
        resposta = askquestion(title = 'Seleção de arquivo', message = 'Editar banco existente?')

        if resposta == 'no' or not resposta:
            return './Novo banco.xlsx'
        else:
            diretorio = sp.abrir_arquivo()
            extensao = '.xlsx'
            if diretorio[-5:] != extensao:
                return diretorio + '/Novo banco.xlsx'
            else:
                return diretorio

    def criar_novo(self):
        diretorio = sp.salvar_como()
        self.diretorio = diretorio

        self.refresh_infos()

    def abrir_novo(self):
        diretorio = sp.abrir_arquivo()
        extensao = '.xlsx'
        if diretorio[-5:] != extensao:
            return 1
        else:
            self.diretorio = diretorio
            self.refresh_infos()
            return 0

    def on_root_ctrl_s(self):
        self.salvar()


class Interface(FuncoesFrontEnd, Questoes, Configs):
    def __init__(self):
        Configs.__init__(self)
        # Inicia variáveis gerais
        self.parametros_e_variaveis()
        # Inicia a janela principal
        self.inicia_tela()

        self.diretorio = self.selecionar_arquivo_pasta()

        self.inicia_menu()

        # Inicia os frames e widgets do layout
        self.inicia_frames()
        # Inicia os frames das alternativas
        self.inicia_frames_opcoes()

        # Abre o módulo de questões
        self.abre_quadro_questoes()

        self.top_lvl.focus_force()

        # Cria o ‘loop’ de exibição da janela principal
        self.root.mainloop()

    def parametros_e_variaveis(self):
        # Cria o parâmetro inicial de posicionamento 'y' das Entrys de opções
        self.rely_entry_opcoes = 0
        self.rely_bts = 0
        # Cria a lista para armazenar as variáveis das entrys de opções
        self.list_opcoes = list()
        # Cria a lista para armazenar as variáveis dos Buttons de corretas
        self.list_bt_corretas, self.list_corretas = list(), list()
        # Cria o dicionário que será usado para enviar informações ao Back End
        self.connector_dict = dict()
        # Este parâmetro é preenchido caso seja uma questão editada
        self.linha = None
        # Cria valor para ser atribuído ao radiobutton
        self.valor_radio_button = 0

    def inicia_tela(self):
        # Inicia a tela principal do formulário
        root = Tk()

        # Cria as proporções da tela principal
        # Configura as dimenções da tela principal e onde ela inicia
        root.geometry(f'{self.largura_tela(root)}x{self.altura_tela(root)}+0+0')
        # Define uma cor de fundo para o backgroud da janela principal
        root.configure(**self.root_param)

        self.frame_param['master'] = root
        root.bind('<Control-s>', lambda e: self.on_root_ctrl_s())
        root.bind('<<F12>>', lambda e: self.criar_novo())
        self.root = root

    def inicia_menu(self):
        menubar = Menu(self.root)
        helpmenu = Menu(menubar, tearoff = 0)
        helpmenu.add_command(label = 'Abrir', command = self.abrir_novo)
        helpmenu.add_command(label = 'Criar novo', command = self.criar_novo)
        helpmenu.add_separator()
        helpmenu.add_command(label = 'Feedbacks', command = self.abre_feedback)
        menubar.add_cascade(label = 'Opções', menu = helpmenu)

        self.root.config(menu = menubar)

    def inicia_frames(self):
        frames = {
            'frame_infos':  dict(
                param = dict(name = 'frame_infos'),
                place = dict(relx = 0.02, rely = 0.03, relwidth = 0.96, relheight = 0.5)
            ),
            'frame_salvar': dict(
                param = dict(name = 'frame_salvar'),
                place = dict(relx = 0.02, rely = 0.94, relwidth = 0.96)
            )
        }
        # Cria o frame onde ficarão os parâmetros da questão
        for frame in frames:
            Frame(**self.frame_param, **frames[frame]['param']).place(**frames[frame]['place'])

        # Cria a variável de alternativa correta do RadioButton, usado nas questões 'ME'
        self.var_radio_button = IntVar()

        self.inicia_formulario_superior()

        # Inicia o botão de salvar
        self.bt_salvar()

    def inicia_formulario_superior(self):
        frame_infos = self.root.children['frame_infos']
        widgets = {
            'labels':       {
                'contador_questao':  {
                    'param': dict(
                        master = frame_infos, **self.label_param,
                        text = f'Questões:\n      {1}     ', name = 'numero_questao'
                    ),
                    'place': dict(relx = 0.02, rely = 0.0)
                },
                'categoria':         {
                    'param': dict(master = frame_infos, text = 'Unidade', **self.label_param),
                    'place': dict(relx = 0.2, rely = 0.0)
                },
                'Código_do_curso':   {
                    'param': dict(
                        master = frame_infos, text = 'Código do curso', **self.label_param
                    ),
                    'place': dict(relx = 0.5, rely = 0.00)
                },
                'Tempo_de_resposta': {
                    'param': dict(
                        master = frame_infos, text = 'Tempo de resposta', **self.label_param
                    ),
                    'place': dict(relx = 0.75, rely = 0.00)
                },
                'Tipo_da_questão':   {
                    'param': dict(
                        master = frame_infos, text = 'Tipo da questão', **self.label_param
                    ),
                    'place': dict(relx = 0.2, rely = 0.2)
                },
                'dificuldade':       {
                    'param': dict(master = frame_infos, text = 'Dificuldade', **self.label_param),
                    'place': dict(relx = 0.5, rely = 0.2)
                },
                'Peso_da_questão':   {
                    'param': dict(
                        master = frame_infos, text = 'Peso da questão', **self.label_param
                    ),
                    'place': dict(relx = 0.75, rely = 0.2)
                },
                'Enunciado':         {
                    'param': dict(
                        master = frame_infos, text = 'Enunciado da questão.', **self.label_param
                    ),
                    'place': dict(relx = 0.05, rely = 0.45)
                },
            },
            'combo_box':    {
                'Unidade':     {
                    'param': dict(master = frame_infos, name = 'unidade', **self.list_param, value = self.unidades),
                    'place': dict(relx = 0.2, rely = 0.06, width = 165)
                },
                'tipo':        {
                    'param': dict(master = frame_infos, name = 'tipo', **self.list_param, value = self.tipos),
                    'place': dict(relx = 0.2, rely = 0.26, width = 165)
                },
                'dificuldade': {
                    'param': dict(
                        master = frame_infos, name = 'dificuldade', **self.list_param, value = self.dificuldades
                    ),
                    'place': dict(relx = 0.5, rely = 0.26)
                },
            },
            'entrys':       {
                'codigo_curso': {
                    'param': dict(master = frame_infos, name = 'codigo_curso'),
                    'place': dict(relx = 0.5, rely = 0.06)
                },
            },
            'place_holder': {
                'tempo': {
                    'param': dict(master = frame_infos, placeholder = '00:00:00', name = 'tempo'),
                    'place': dict(relx = 0.75, rely = 0.06)
                },
                'peso':  {
                    'param': dict(master = frame_infos, placeholder = '1', name = 'peso'),
                    'place': dict(relx = 0.75, rely = 0.26)
                },
            },
            'texts':        {
                'pergunta': {
                    'param': dict(master = frame_infos, name = 'pergunta', wrap = 'word', height = 4, undo = True),
                    'place': dict(relx = 0.05, rely = 0.56, relwidth = 0.9)
                }
            },
            'buttons':      {
                'add_opção': {
                    'param': dict(master = frame_infos, text = '+ opção', command = self.add_alternativa),
                    'place': dict(relx = 0.7, rely = 0.8, relwidth = 0.1)
                },
                'rmv_opção': {
                    'param': dict(master = frame_infos, text = '- opção', command = self.remove_alternativa),
                    'place': dict(relx = 0.85, rely = 0.8, relwidth = 0.1)
                },
            }
        }
        for widget in widgets:
            if widget == 'labels':
                for label in widgets[widget]:
                    Label(**widgets[widget][label]['param']).place(**widgets[widget][label]['place'])
            elif widget == 'entrys':
                for entry in widgets[widget]:
                    Entry(**widgets[widget][entry]['param']).place(**widgets[widget][entry]['place'])
            elif widget == 'place_holder':
                for holder in widgets[widget]:
                    PlaceHolder(**widgets[widget][holder]['param']).place(**widgets[widget][holder]['place'])
            elif widget == 'combo_box':
                for option in widgets[widget]:
                    Combobox(**widgets[widget][option]['param']).place(**widgets[widget][option]['place'])
                    frame_infos.children[widgets[widget][option]['param']['name']].current(0)
            elif widget == 'texts':
                for texto in widgets[widget]:
                    Text(**widgets[widget][texto]['param']).place(**widgets[widget][texto]['place'])
            elif widget == 'buttons':
                for botao in widgets[widget]:
                    Button(**widgets[widget][botao]['param']).place(**widgets[widget][botao]['place'])

        frame_infos.children['tipo'].bind('<<ComboboxSelected>>', lambda e: self.altera_tipo_opcao())
        frame_infos.after(100, lambda: frame_infos.children['unidade'].focus_force())

        todos_widgets = (
            frame_infos.children['unidade'],
            frame_infos.children['codigo_curso'],
            frame_infos.children['tempo'],
            frame_infos.children['tipo'],
            frame_infos.children['dificuldade'],
            frame_infos.children['peso'],
            frame_infos.children['pergunta'],
        )
        for widget in todos_widgets:
            widget.lift()

    def inicia_frames_opcoes(self):
        # Cria a frame das alternativas/opções
        self.frame_opcs = Frame(master = self.root, **self.frame_param)
        # Posiciona a frame das alternativas/opções
        self.frame_opcs.place(relx = 0.02, rely = 0.5, relwidth = 0.96, relheight = 0.44)

        self.inicia_frame_bts()

    def inicia_frame_bts(self):
        # Cria a frame para botões de seleção das corretas
        self.frame_bts = Frame(master = self.root, **self.frame_param)
        self.frame_bts.place(relx = 0.9, rely = 0.5, relwidth = 0.05, relheight = 0.44)

    def bt_salvar(self):
        # Cria botão de salvar
        salvar = Button(
            master = self.root.children.get('frame_salvar'), text = 'Salvar', relief = 'solid',
            command = self.salvar, activebackground = '#F00BA4'
        )
        # Posiciona o botão de salvar
        salvar.pack(fill = 'x', side = 'bottom')


if __name__ == '__main__':
    Interface()
