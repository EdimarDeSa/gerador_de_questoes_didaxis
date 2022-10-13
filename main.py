from subprocess import call
from tkinter import Tk, Frame, Label, Menu
from tkinter import Entry, Text, Listbox, OptionMenu, Button, Checkbutton, Radiobutton
from tkinter import BooleanVar, IntVar, StringVar
from tkinter import messagebox

from estiloWidgets.entryPlaceHolder import EntPlaceHold

from configuracoes import Configs
from quadro_de_questoes import Questoes
from selecao_de_diretorio import SelecionaPasta as SP


class FuncoesFrontEnd:
    @property
    def largura_tela(self):
        return int(self.root.winfo_screenwidth() / 2.15)

    @property
    def altura_tela(self):
        return int(self.root.winfo_screenheight() / 1.1)

    def altera_tipo_opcao(self, _):
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
        entrada = Entry(self.frame_opcs)
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
            'Multipla escolha 1 correta': self.cria_radio_bt,
            'Multipla escolha n corretas': self.cria_check_bt,
            'Verdadeiro ou falso': self.cria_check_bt
        }
        tipos[self.tipo_list.get('active')]()
        self.rely_bts += 0.09

    def cria_radio_bt(self):
        # Cria botão para seleção de alternativa correta no modo RadioButton
        self.rad_bt = Radiobutton(
            **self.buttons_param,
            value = self.valor_radio_button,
            variable = self.var_radio_button
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
            **self.buttons_param,
            variable = correta
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
        # Cria dicionário para ser repassado ao back end
        api_dict = {
            'Tipo': self.tipo_list.get('active'),
            'Peso': self.peso_entry.get(),
            'Tempo': self.tempo_entry.get(),
            'Pergunta': self.perguntas,
            'Alternativa': self.lista_alternativas,
            'Correta': self.listar_corretas(),
            'Categoria': self.var_unidade.get(),
            'SubCategoria': self.codigo_curso_entry.get(),
            'Dificuldade': self.dificuldade_list.get('active'),
            'linha': self.linha,
            'diretorio': self.diretorio
        }
        # Envia informações para back end
        self.gravar(api_dict)

        # Limpa dicionário após salvar no excel
        api_dict.clear()

        # Limpa formulário de opções para nova questão e TextBox
        self.reset_opcs()

        if not self.top_lvl.winfo_exists():
            self.abre_quadro_questoes()
        else:
            self.refresh_infos()

    # Verrifica se existe algo no campo de pergunta e opções
    def verifica_informacoes(self):
        self.perguntas = self.pergunta_entry.get('0.0', 'end').rstrip('\n')
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
        messagebox.showerror(
            title = 'Falha na estrutura',
            message = '''
            Não será possível prosseguir \n 
            com a gravação da questão, \n
            existem informações faltando.
             '''
        )

    def listar_corretas(self):
        tipo = self.tipo_list.get('active')
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
        resposta = messagebox.askquestion(title = 'Seleção de arquivo', message = 'Editar banco existente?')
        if resposta == 'no':
            return './Novo banco.xlsx'
        else:
            return SP.abrir_arquivo()
    def salvar_novo(self):
        diretorio = SP.salvar_como()
        extensao = '.xlsx'
        if diretorio[-5:] != extensao:
            self.diretorio = diretorio + extensao
        else:
            self.diretorio = diretorio

        self.refresh_infos()


# ---------------------------------------------------------------------------------------------------------------------#


class Interface(FuncoesFrontEnd, Questoes):
    def __init__(self):
        Configs.verifica_dependencias()
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
        # param == parâmetros
        self.root_param = Configs.abre_configs('root')

        self.frame_param = Configs.abre_configs('param_frames')

        # Inicia os parâmetros básicos de todos os labels usados
        self.label_param = Configs.abre_configs('param_labels')

        # Inicia os parâmetros básicos de todas as listas usadas
        self.list_param = Configs.abre_configs('param_lists')

        self.buttons_param = Configs.abre_configs('param_buttons')

        # Cria a lista de tipos das questões
        self.tipos = Configs.abre_configs('tipos')

        self.unidades = Configs.abre_configs('unidades')

        self.dificuldades = Configs.abre_configs('Dificuldades')

        # Cria o parâmetro inicial de posicionamento 'y' das Entrys de opções
        self.rely_entry_opcoes = 0
        self.rely_bts = 0

        # Cria a lista para armazenar as variáveis das entrys de opções
        self.list_opcoes = []
        # Cria a lista para armazenar as variáveis dos Buttons de corretas
        self.list_bt_corretas, self.list_corretas = [], []
        # Cria o dicionário que será usado para enviar informações ao Back End
        self.connector_dict = {}

        self.linha = None

        # Cria valor para ser atribuído ao radiobutton
        self.valor_radio_button = 0

    def inicia_tela(self):
        # Inicia a tela principal do formulário
        self.root = Tk('Gerador de banco de questões')

        # Cria as proporções da tela principal
        # Configura as dimenções da tela principal e onde ela inicia
        self.root.geometry(f'{self.largura_tela}x{self.altura_tela}+0+0')
        # Define uma cor de fundo para o backgroud da janela principal
        self.root.configure(**self.root_param)

        self.frame_param['master'] = self.root

    def inicia_menu(self):
        menubar = Menu(self.root)
        helpmenu = Menu(menubar, tearoff = 0)
        helpmenu.add_command(label = 'Salvar novo', command = self.salvar_novo)
        helpmenu.add_command(label = 'Feedbacks', command = self.abre_feedback)
        menubar.add_cascade(label = 'Opções', menu = helpmenu)

        self.root.config(menu = menubar)

    def inicia_frames(self):
        # Cria o frame onde ficarão os parâmetros da questão
        frame_infos = Frame(**self.frame_param)
        # Posiciona o frame de parâmetros
        frame_infos.place(relx = 0.02, rely = 0.03, relwidth = 0.96, relheight = 0.5)

        # Cria o frame onde ficará o botão de salvar a questão
        frame_salvar = Frame(**self.frame_param)
        # Posiciona o frame do botão salvar
        frame_salvar.place(relx = 0.02, rely = 0.94, relwidth = 0.96)

        self.frame_infos = frame_infos
        self.label_param['master'] = self.frame_infos
        self.list_param['master'] = self.frame_infos

        self.frame_salvar = frame_salvar

        # Cria a variável de alternativa correta do RadioButton, usado nas questões 'ME'
        self.var_radio_button = IntVar()

        # Inicia o número da questão para efeito de contabilidade
        self.numero_questao()
        # Inicia captura de categoria
        self.categoria()
        # Inicia captura de sub categoria
        self.sub_categoria()
        # Inicia captura de tempo para responder questão
        self.tempo()
        # Inicia captura de tipo das alternativas
        self.tipo()
        # Inicia captura de peso da questão
        self.peso()
        # Inicia captura de dificuldade da questão
        self.dificuldade()
        # Inicia captura de pergunta
        self.pergunta()
        # Inicia o botão de retirar alternativa
        self.bt_remove_alternativa()
        # Inicia o botão de alternativa
        self.bt_add_alternativa()
        # Inicia o botão de salvar
        self.bt_salvar()

    def numero_questao(self):
        # Cria uma variável para escrever o número da questão na janela
        self.contador_questao = StringVar()
        # Cria a label onde será impresso o número da questão
        questao_label = Label(**self.label_param, textvariable = self.contador_questao)
        # Posiciona o label do número da questão
        questao_label.place(relx = 0.0, rely = 0.0)
        # Verifica o número da questão que será criada
        self.contador_questao.set('Questões: \n'
                                  f'      {1}     ')

    def categoria(self):
        # Ordena as unidades por nome
        self.unidades.sort()

        # Cria a label com a descrição da categoria
        self.categoria_label = Label(text = 'Unidade', **self.label_param)
        # Posiciona a label de descrição na tela
        self.categoria_label.place(relx = 0.2, rely = 0.0)

        # Cria a variável do OptionMenu
        self.var_unidade = StringVar()
        # Cria a lista de OptionMenu
        self.unidade = OptionMenu(self.frame_infos, self.var_unidade, *self.unidades)
        # Posiciona a optinMenu
        self.unidade.place(relx = 0.2, rely = 0.06, width = 165)
        # Seleciona a primeira unidade da OptionMenu como padrão
        self.var_unidade.set(self.unidades[1])

    def sub_categoria(self):
        # Cria a label com a descrição da sub categoria
        codigo_curso_label = Label(text = 'Código do curso', **self.label_param)
        # Posiciona a label da sub categoria
        codigo_curso_label.place(relx = 0.5, rely = 0.00)

        # Cria a Entry da categoria
        self.codigo_curso_entry = Entry(self.frame_infos)
        # Posiciona a Entry da categoria
        self.codigo_curso_entry.place(relx = 0.5, rely = 0.06)

    def tempo(self):
        # Cria a label de tempo
        tempo_label = Label(text = 'Tempo de resposta', **self.label_param)
        # Posiciona a label de tempo
        tempo_label.place(relx = 0.75, rely = 0.00)

        # Cria a entry de tempo
        self.tempo_entry = EntPlaceHold(self.frame_infos, '00:00:00')
        # Posiciona a entry de tempo
        self.tempo_entry.place(relx = 0.75, rely = 0.06)

    def tipo(self):
        # Cria a label do tipo
        tipo_label = Label(text = 'Tipo da questão', **self.label_param)
        # Posiciona a label de tempo
        tipo_label.place(relx = 0.2, rely = 0.2)

        # Cria listbox para as questões disponíveis
        self.tipo_list = Listbox(**self.list_param)
        # Posiciona a listbox dos tipos da questão
        self.tipo_list.place(relx = 0.2, rely = 0.26, width = 165)
        # Insere as opções de tipops
        self.tipo_list.insert(0, *self.tipos)
        # Ativa o primeiro tipo
        self.tipo_list.activate(0)

        # Aciona a reinicialização das opções sempre que o usuário clicar numa opção dentro da listbox
        self.tipo_list.bind('<<ListboxSelect>>', self.altera_tipo_opcao)

    def dificuldade(self):
        # Cria a label da dificuldade
        dificuldade_label = Label(text = 'Dificuldade', **self.label_param)
        # Posiciona a label da dificuldade
        dificuldade_label.place(relx = 0.5, rely = 0.2)

        # Cria a listbox da dificuldade
        self.dificuldade_list = Listbox(**self.list_param)
        # Posiciona a listbox da dificuldade
        self.dificuldade_list.place(relx = 0.5, rely = 0.26)
        # Insere a lista de dificuldades na listbox
        self.dificuldade_list.insert(0, *self.dificuldades)
        self.dificuldade_list.activate(0)

    def peso(self):
        #  Cria label do peso da questão
        peso_label = Label(text = 'Peso da questão', **self.label_param)
        #  Posiciona o label do peso da questão
        peso_label.place(relx = 0.75, rely = 0.2)

        #  Cria Entry do peso da questão
        self.peso_entry = EntPlaceHold(self.frame_infos, '1')
        #  Posiciona a Entry do peso da questão
        self.peso_entry.place(relx = 0.75, rely = 0.26)

    def pergunta(self):
        # Cria a label da pergunta
        pergunta_label = Label(text = 'Enunciado da questão.', **self.label_param)
        # Posiciona a label da pergunta
        pergunta_label.place(relx = 0.05, rely = 0.45)

        # Cria a Textbox da pergunta
        self.pergunta_entry = Text(self.frame_infos, wrap = 'word', height = 4, undo = True)
        # Posiciona a caixa de texto da pergunta
        self.pergunta_entry.place(relx = 0.05, rely = 0.56, relwidth = 0.9)

    def bt_add_alternativa(self):
        # Cria o botão para adicionar alternativa/opção
        bt_add = Button(self.frame_infos, text = '+ opção', command = self.add_alternativa)
        # Posiciona o botão de alternativas, o relwidth é para combinar com o tamanho da caixa de texto
        bt_add.place(relx = 0.7, rely = 0.8, relwidth = 0.1)

    def bt_remove_alternativa(self):
        # Cria o botão para adicionar alternativa/opções
        bt_remove = Button(self.frame_infos, text = '- opção', command = self.remove_alternativa)
        # Posiciona o botão de alternativas, o relwidth é para combinar com o tamanho da caixa de texto
        bt_remove.place(relx = 0.85, rely = 0.8, relwidth = 0.1)

    def inicia_frames_opcoes(self):
        # Cria a frame das alternativas/opções
        self.frame_opcs = Frame(**self.frame_param)
        # Posiciona a frame das alternativas/opções
        self.frame_opcs.place(relx = 0.02, rely = 0.5, relwidth = 0.96, relheight = 0.44)

        self.inicia_frame_bts()

    def inicia_frame_bts(self):
        # Cria a frame para botões de seleção das corretas
        self.frame_bts = Frame(**self.frame_param)
        self.frame_bts.place(relx = 0.9, rely = 0.5, relwidth = 0.05, relheight = 0.44)

        self.buttons_param['master'] = self.frame_bts

    def bt_salvar(self):
        # Cria botão de salvar
        self.salvar = Button(self.frame_salvar, text = 'Salvar', relief = 'solid',
                             command = self.salvar, activebackground = '#F00BA4')
        # Posiciona o botão de salvar
        self.salvar.pack(fill = 'x', side = 'bottom')


# ---------------------------------------------------------------------------------------------------------------------#


if __name__ == '__main__':
    Interface()
