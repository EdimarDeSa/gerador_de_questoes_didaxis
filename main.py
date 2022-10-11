from os.path import abspath, exists
from json import dump, load
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename

from estiloWidgets.entryPlaceHolder import EntPlaceHold as eph


class Configs:
    @classmethod
    def verifica_dependencias(cls):
        config_path = abspath('./configs/configs.json')
        if not exists(config_path):
            infos = {
                'root': {
                    'background': 'green',
                },
                'param_labels': {
                    'background': 'lightgreen',
                    'font': 'Arial 10 bold',
                },
                'param_lists': {
                    'selectmode': 'single',
                    'height': 3,
                    'font': 'Arial 8 bold',
                    'relief': 'sunken',
                    'selectbackground': 'lightgreen',
                    'exportselection': False,
                },
                'tipos': [
                    "Multipla escolha 1 correta",
                    "Multipla escolha n corretas",
                    "Verdadeiro ou falso"
                ],
                'unidades': [
                    "Comunicação",
                    "Redes",
                    "Segurança eletrônica",
                    "Controle de acesso",
                    "Incêndio e iluminação",
                    "Varejo",
                    "Verticais",
                    "Soluções",
                    "Solar",
                    "Negócios",
                    "Gestão",
                    "Energia",
                    "Astec"
                ]
            }
            cls.salva_configs(infos)

    @classmethod
    def salva_configs(cls, config_path, infos):
        config_path = abspath('./configs/configs.json')
        with open(config_path, 'w') as arquivo_configuracoes:
            dump(infos, arquivo_configuracoes, indent = 4)

    @classmethod
    def abre_configs(cls, chave):
        config_path = abspath('./configs/configs.json')
        with open(config_path, 'r') as arquivo_configuracoes:
            infos = load(arquivo_configuracoes)
            return infos[chave]


class FuncoesFrontEnd:
    @property
    def largura_tela(self):
        return int(self.root.winfo_screenwidth() / 2.15)

    @property
    def altura_tela(self):
        return int(self.root.winfo_screenheight() / 1.1)


class Interface(FuncoesFrontEnd):
    def __init__(self):
        Configs.verifica_dependencias()
        # Inicia variáveis gerais
        self.parametros_e_variaveis()
        # Inicia a janela principal
        self.inicia_tela()

        self.inicia_menu()

        # Inicia os frames e widgets do layout
        self.inicia_frames()
        # # Inicia os frames das alternativas
        # self.inicia_frames_opcoes()
        # # Abre o módulo de questões
        # self.iniciar_quadro_questoes(self.root, self.cor_background, self.largura_tela, self.altura_tela)
        # # Cria o ‘loop’ de exibição da janela principal
        self.root.mainloop()

    def parametros_e_variaveis(self):
        # param == parâmetros
        self.root_param = Configs.abre_configs('root')

        self.frame_param = Configs.abre_configs('param_frames')

        # Inicia os parâmetros básicos de todos os labels usados
        self.label_param = Configs.abre_configs('param_labels')

        # Inicia os parâmetros básicos de todas as listas usadas
        self.list_param = Configs.abre_configs('param_lists')

        # Cria a lista de tipos das questões
        self.tipos = Configs.abre_configs('tipos')

        self.unidades = Configs.abre_configs('unidades')

    def inicia_tela(self):
        # Inicia a tela principal do formulário
        self.root = Tk('Gerador de banco de questões')

        # Cria as proporções da tela principal
        # Configura as dimenções da tela principal e onde ela inicia
        self.root.geometry(f"{self.largura_tela}x{self.altura_tela}+0+0")
        # Define uma cor de fundo para o backgroud da janela principal
        self.root.configure(**self.root_param)

        self.frame_param['master'] = self.root

    def inicia_menu(self):
        menubar = Menu(self.root)
        helpmenu = Menu(menubar, tearoff = 0)
        helpmenu.add_command(label = "Ajuda", command = lambda: Configs())
        helpmenu.add_command(label = "Sobre...", command = lambda: Configs())
        menubar.add_cascade(label = "Ajuda", menu = helpmenu)

        self.root.config(menu = menubar)

    def inicia_frames(self):
        # Cria o frame onde ficarão os parâmetros da questão
        frame_infos = Frame(**self.frame_param)
        # Posiciona o frame de parâmetros
        frame_infos.place(relx = 0.02, rely = 0.03, relwidth = 0.96, relheight = 0.5)

        # Cria o frame onde ficará o botão de salvar a questão
        frame_salvar = Frame(**self.frame_param)
        # Posiciona o frame do botão salvar
        frame_salvar.place(relx = 0.02, rely = 0.93, relwidth = 0.96, relheight = 0.04)

        self.frame_infos = frame_infos
        self.label_param['master'] = self.frame_infos
        self.list_param['master'] = self.frame_infos

        # Inicia o número da questão para efeito de contabilidade
        self.numero_questao()
        # Inicia captura de categoria
        self.categoria()
        # # Inicia captura de sub categoria
        # self.sub_categoria()
        # # Inicia captura de tempo para responder questão
        # self.tempo()
        # # Inicia captura de tipo das alternativas
        # self.tipo()
        # # Inicia captura de peso da questão
        # self.peso()
        # # Inicia captura de dificuldade da questão
        # self.dificuldade()
        # # Inicia captura de pergunta
        # self.pergunta()
        # # Inicia o botão de retirar alternativa
        # self.bt_remove_alternativa()
        # # Inicia o botão de alternativa
        # self.bt_add_alternativa()
        #
        # super(GeradorDeQuestoes, self).__init__()
        #
        # # Inicia o botão de salvar
        # self.bt_salvar()

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
        print(self.unidades)

        # Cria a label com a descrição da categoria
        self.categoria_label = Label(text = "Unidade", **self.label_param)
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
        self.codigo_curso_label = Label(self.frame_infos, text = "Código do curso", **self.label_param)
        # Posiciona a label da sub categoria
        self.codigo_curso_label.place(relx = 0.5, rely = 0.00)

        # Cria a Entry da categoria
        self.codigo_curso_entry = Entry(self.frame_infos)
        # Posiciona a Entry da categoria
        self.codigo_curso_entry.place(relx = 0.5, rely = 0.06)

    def tempo(self):
        # Cria a label de tempo
        self.tempo_label = Label(self.frame_infos, text = "Tempo de resposta", **self.label_param)
        # Posiciona a label de tempo
        self.tempo_label.place(relx = 0.75, rely = 0.00)

        # Cria a entry de tempo
        self.tempo_entry = eph(self.frame_infos, "00:00:00")
        # Posiciona a entry de tempo
        self.tempo_entry.place(relx = 0.75, rely = 0.06)

    def tipo(self):
        # Cria a label do tipo
        self.tipo_label = Label(self.frame_infos, text = "Tipo da questão", **self.label_param)
        # Posiciona a label de tempo
        self.tipo_label.place(relx = 0.2, rely = 0.2)

        # Cria listbox para as questões disponíveis
        self.tipo_list = Listbox(self.frame_infos, **self.list_param)
        # Posiciona a listbox dos tipos da questão
        self.tipo_list.place(relx = 0.2, rely = 0.26, width = 165)
        # Insere as opções de tipops
        self.tipo_list.insert(0, *self.tipos)
        # Ativa o primeiro tipo
        self.tipo_list.activate(0)

        # Aciona a reinicialização das opções sempre que o usuário clicar numa opção dentro da listbox
        self.tipo_list.bind("<<ListboxSelect>>", self.altera_tipo_opcao)

    def dificuldade(self):
        # Cria a tabela de dificuldades
        dificuldades = ["Fácil", "Médio", "Difícil"]

        # Cria a label da dificuldade
        self.dificuldade_label = Label(self.frame_infos, text = "Dificuldade", **self.label_param)
        # Posiciona a label da dificuldade
        self.dificuldade_label.place(relx = 0.5, rely = 0.2)

        # Cria a listbox da dificuldade
        self.dificuldade_list = Listbox(self.frame_infos, **self.list_param)
        # Posiciona a listbox da dificuldade
        self.dificuldade_list.place(relx = 0.5, rely = 0.26)
        # Insere a lista de dificuldades na listbox
        self.dificuldade_list.insert(0, *dificuldades)

    def peso(self):
        #  Cria label do peso da questão
        self.peso_label = Label(self.frame_infos, text = "Peso da questão", **self.label_param)
        #  Posiciona o label do peso da questão
        self.peso_label.place(relx = 0.75, rely = 0.2)

        #  Cria Entry do peso da questão
        self.peso_entry = eph(self.frame_infos, "1")
        #  Posiciona a Entry do peso da questão
        self.peso_entry.place(relx = 0.75, rely = 0.26)

    def pergunta(self):
        # Cria a label da pergunta
        self.pergunta_label = Label(self.frame_infos, text = "Enunciado da questão.", **self.label_param)
        # Posiciona a label da pergunta
        self.pergunta_label.place(relx = 0.05, rely = 0.45)

        # Cria a Textbox da pergunta
        self.pergunta_entry = Text(self.frame_infos, wrap = "word", height = 4, undo = True)
        # Posiciona a Textbox da pergunta
        self.pergunta_entry.place(relx = 0.05, rely = 0.56, relwidth = 0.9)

    def bt_add_alternativa(self):
        # Cria o botão para adicionar alternativa/opção
        bt_add = Button(self.frame_infos, text = "+ opção", command = self.add_alternativa)
        # Posiciona o botão de alternativas, o relwidth é para combinar com o tamanho da caixa de texto
        bt_add.place(relx = 0.7, rely = 0.8, relwidth = 0.1)

    def bt_remove_alternativa(self):
        # Cria o botão para adicionar alternativa/opções
        bt_remove = Button(self.frame_infos, text = "- opção", command = self.remove_alternativa)
        # Posiciona o botão de alternativas, o relwidth é para combinar com o tamanho da caixa de texto
        bt_remove.place(relx = 0.85, rely = 0.8, relwidth = 0.1)

    def bt_salvar(self):
        # Cria botão de salvar
        self.salvar = Button(self.frame_salvar, text = "Salvar", command = self.salvar)
        # Posiciona o botão de salvar
        self.salvar.pack(fill = 'x', side = 'bottom')

    def inicia_frames_opcoes(self):
        # Cria a frame das alternativas/opções
        self.frame_opcs = Frame(self.root, bg = self.cor_geral)
        # Posiciona a frame das alternativas/opções
        self.frame_opcs.place(relx = 0.02, rely = 0.5, relwidth = 0.96, relheight = 0.44)

        self.inicia_frame_bts()

    def inicia_frame_bts(self):
        # Cria a frame para botões de seleção das corretas
        self.frame_bts = Frame(self.root, bg = self.cor_geral)
        self.frame_bts.place(relx = 0.9, rely = 0.5, relwidth = 0.05, relheight = 0.44)


if __name__ == '__main__':
    Interface()
