from kivymd.app import MDApp # Base do aplicativo
from kivy.lang import Builder # Permite o carregamento das pastas .kv
from kivymd.uix.floatlayout import MDFloatLayout # Permite editar o layout do app
from kivy.properties import StringProperty, BooleanProperty # Permite criar o temporizador em formato de string
from kivy.uix.screenmanager import Screen, ScreenManager #Screen (tela individual) ScreenManager (Gerenciar as telas individuais)
from kivy.clock import Clock # Permite controlar ações repetitivas usado no temporizador
from datetime import datetime # Permite a criação de datas nas checklists
from kivymd.uix.selectioncontrol import MDCheckbox # Permite a criação de checkbox nas tarefas
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout # Cria layout para as tarefas
from kivymd.uix.button import MDRaisedButton, MDIconButton # Cria botões para a tarefa
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp


class TelaTarefas(Screen): # Tela principal do app
    def adicionar_tarefa(self):
        self.dialog = MDDialog(
        title = "Adicionar Tarefa",
        type = "custom",
        content_cls = MDTextField(hint_text="Digite a tarefa"),
        buttons = [
            MDRaisedButton(
                text = "Cancelar",
                on_release = self.fecha_dialog
             ),
            MDRaisedButton(
                text = "Adicionar",
                on_release = self.salvar_tarefa
            )
        ]
    )
        self.dialog.open()

    def fecha_dialog(self, instance):
        self.dialog.dismiss()

    def salvar_tarefa(self, instance):
        texto_tarefa = self.dialog.content_cls.text
        
        if texto_tarefa.strip():
            tarefa = Tarefa(texto = texto_tarefa)
            self.ids.tarefas_container.add_widget(tarefa)
            self.dialog.dismiss()
        else:  
             print("Digite uma tarefa!")

class TelaTemporizador(Screen): # Definindo a tela do temporizador
    pass


class TelaHistorico(Screen): # Definindo a tela de histórico
    pass    


class GerenciadorDeTelas(ScreenManager): # Definindo a classe que gerencia todas as telas
    pass


class Temporizador: # Classe do temporizador com suas determinadas funções de tempo usando strings
    def __init__(self, tempo):  # Criando uma nova instância da classe temporizador.
        self.tempo = tempo * 60 # Converte o tempo fornecido em minutos para segundos armazenando em self.tempo
        
    def DiminuiTempo(self):
        self.tempo -= 1 # Diminui o valor de self.tempo de 1 em 1 segundo
        return self.tempo
    
    def __str__(self):  # usando formatação de string para formatar o tempo.
        return '{:02d}:{:02d}'.format(*divmod(self.tempo, 60)) # A função divmod recebe dois valores e retorna uma tupla com dois valores.


class MostraTemporizador(MDFloatLayout): # Classe que mostra o temporizador utilizando o StringProperty
    tempo_string = StringProperty('25:00') # Define o tempo padrão, de 25 minutos.
    botao_string = StringProperty('Iniciar') 
    running = BooleanProperty(False) # Identifica se o temporizador está rodando ou não. ( Inicia como False)

    def __init__(self, **kwargs): # Método construtor da classe
        super().__init__(**kwargs) # Chamada do construtor da classe 'MDFloatLayout' 
        self._time = Temporizador(tempo = 25) #Cria um objeto 'Temporizador' herdando da classe já criada, inicializando com 25min
        self.atualiza_tempo_na_tela() # Chama a função para exibir o tempo inicial da tela

    def inicia(self): # Função do iniciador
        self.botao_string = 'Pausar' # Altera a string para 'Pausar' quando é iniciado.
        if not self.running: # Verifica se o temporizador não está rodando
            self.running = True 
            Clock.schedule_interval(self.atualizar_tempo, 1) # Usando o relógio do kivy para chamar o método 'atualizar_tempo' a cada 1s

    def pausa(self):
        self.botao_string = 'Reiniciar'
        if self.running:
            self.running = False
            Clock.unschedule(self.atualizar_tempo)

    def zerar(self):
        if self.running:
            self.pausa()  # Pausa o temporizador, se estiver rodando
        self._time = Temporizador(tempo = 25)  # Redefine o tempo para 25 minutos
        self.atualiza_tempo_na_tela()  # Atualiza o tempo na tela
        self.botao_string = 'Iniciar'  # Muda o texto do botão de controle para "Iniciar"

    def click(self):
        if self.running:
            self.pausa()
        else:
            self.inicia()
    
    def atualizar_tempo(self, *args):
        time = self._time.DiminuiTempo()
        self.tempo_string = str(self._time)
        if time <= 0:
            self.pausa()

    def atualiza_tempo_na_tela(self):
        self.tempo_string = str(self._time)


class Tarefa(MDBoxLayout):
    texto = StringProperty('Nova Tarefa')
    data_criacao = StringProperty('')
    completo = BooleanProperty(False)

    def __init__(self, texto='', **kwargs):
        super().__init__(**kwargs)
        self.texto = texto
        self.data_criacao = datetime.now().strftime('%d-%m-%y')
        self.orientation = 'horizontal'
        self.spacing = dp(10)  # Espaçamento entre os elementos
        self.size_hint_y = None
        self.height = dp(60)
      
         # Checkbox com tamanho fixo e centralização vertical
        self.checkbox = MDCheckbox(size_hint_x = None, width = dp(40), size_hint_y = None, height = dp(40))
        self.checkbox.pos_hint = {'center_y': 0.5}
        self.add_widget(self.checkbox)

        # Texto da tarefa centralizado verticalmente
        self.label = MDLabel(text = self.texto, size_hint_x = 0.6, valign = 'middle', halign = 'left')
        self.label.bind(size=self.label.setter('text_size'))  # Ajusta o texto para caber no espaço
        self.label.pos_hint = {'center_y': 0.5}
        self.add_widget(self.label)

        # Data de criação centralizada verticalmente
        self.data_label = MDLabel(text = self.data_criacao, size_hint_x = 0.2, valign = 'middle', halign = 'right')
        self.data_label.bind(size=self.data_label.setter('text_size'))
        self.data_label.pos_hint = {'center_y': 0.5}
        self.add_widget(self.data_label)

        # Botão de excluir com tamanho fixo e centralização vertical
        self.delete_botao = MDIconButton(icon = "delete", size_hint_x = None, width = dp(40), size_hint_y = None, height = dp(40))
        self.delete_botao.pos_hint = {'center_y': 0.5}
        self.delete_botao.bind(on_release = self.excluir_tarefa)
        self.add_widget(self.delete_botao)

    def excluir_tarefa(self, instance): # Remove o widget atual (a tarefa) do container pai
        self.parent.remove_widget(self)


class QuickTarefas(MDApp):
    def build(self):
        return Builder.load_file('QuickTarefas.kv')
    
    def tela1(self, *args): # Tela do histórico
        self.root.current = 'tela_historico'

    def tela2(self, *args): # Tela do temporizador
        self.root.current = 'tela_temporizador'


QuickTarefas().run()
