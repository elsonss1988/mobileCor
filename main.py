from kivy.app import App 
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
import json
import random


red = [1,0,0,1]
green = [0,1,0,1]
blue =  [0,0,1,1]
purple = [1,0,1,1]

colorList=["amarelo","verde","vermelho","azul"]
colorQuestion=random.choice(colorList)

class Gerenciador(ScreenManager):
    pass

class Menu(Screen):
    def on_pre_enter(self):
        Window.bind(on_request_close=self.confirmacao)


    def confirmacao(self,*args):
        box=BoxLayout(orientation='vertical',padding=10,spacing=10)
        botoes=BoxLayout(padding=10,spacing=10)

        pop=Popup(title="Deseja mesmo sair?",content=box,size_hint=(None,None),size=(300,180))

        sim=Botao(text='Sim',on_release=App.get_running_app().stop)
        nao=Botao(text='Nao',on_release=pop.dismiss)

        botoes.add_widget(sim)
        botoes.add_widget(nao)
        
        atencao=Image(source='atencao.png')

        box.add_widget(atencao)
        box.add_widget(botoes)

        pop.open()
        return True

class Botao(ButtonBehavior,Label):
    cor = ListProperty([0.1,0.5,0.7,1])
    cor2 = ListProperty([0.1,0.1,0.1,1])

    def __init__(self,**kwargs):
        super(Botao,self).__init__(**kwargs)
        self.atualizar()

    def on_pos(self,*args):
        self.atualizar()

    def on_size(self,*args):
        self.atualizar()

    def on_press(self,*args):
        self.cor, self.cor2 = self.cor2, self.cor

    def on_release(self,*args):
        self.cor, self.cor2 = self.cor2, self.cor

    def on_cor(self,*args):
        self.atualizar()

    def atualizar(self,*args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.cor)
            Ellipse(size=(self.height,self.height),
                    pos=self.pos)
            Ellipse(size=(self.height,self.height),
                    pos=(self.x+self.width-self.height,self.y))
            Rectangle(size=(self.width-self.height,self.height),
                      pos=(self.x+self.height/2.0,self.y))


class Tarefas(Screen):
    tarefas=[]
    path=''
    popSound=None
    popapSound=None
    def on_pre_enter(self):
        if self.popSound == None:
            self.popSound=SoundLoader.load('pop.mp3')
            self.popapSound=SoundLoader.load('popap.mp3')
        self.ids.box.clear_widgets()
        self.path=App.get_running_app().user_data_dir+'/'
        self.loadData
        self.ids.box.add_widget(Label(text='Qual o botão com a cor '+colorQuestion+' ?',font_size=30,size_hint_y=None,height=200))
        Window.bind(on_keyboard=self.voltar)
        # for tarefa in self.tarefas:
        #     self.ids.box.add_widget(Tarefa(text=tarefa))

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)

    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current='menu'
            #print(key)
            return True

    def upScore(self,*args):
        # score=self.ids.score.text
        self.ids.score.text= str(int(self.ids.score.text)+1)
        self.popSound.play()
        #colorList=["amarelo","verde","vermelho","azul"]
        colorQuestion=random.choice(colorList)
        self.ids.box.clear_widgets()
        self.ids.box.add_widget(Label(text='Qual o botão com a cor '+colorQuestion+' ?',font_size=30,size_hint_y=None,height=200))
        self.ids.btnBox.clear_widgets()
        #layout=BoxLayout(padding=10)
        colors=[red,green,blue,purple]
        for i in range(5):
            btn=Button(text="Button #%s" % (i+1),background_color=random.choice(colors))
            self.ids.btnBox.add_widget(btn)
        self.ids.btnA.my_color = (1, 0, 0,1)
        self.ids.btnA.canvas.ask_update()
        return Tarefas()
    #   self.popapSound.play() #erro
    #   self.ids.boxScore.Label.text= str(int(self.ids.boxScore.Label.text)+1)
    #   texto = self.ids.boxScore.text
    #   self.ids.texto.text =  str(int(self.boxScore.text)+1)
    #   self.tarefas.append(texto)
    #   # self.saveData()  


    def btns(self):
        layout=BoxLayout(padding=10)        
        red = [1,0,0,1]
        green = [0,1,0,1]
        blue =  [0,0,1,1]
        purple = [1,0,1,1]
        colors={red,green,blue,purple}
        for i in range(5):
            btn=Button(text="Button #%s" % (i+1),
                        background_color=random.choice(colors)
                        )
            layout.add_widget(btn)
        return layout

    def saveData(self,*args):
        with open(self.path+'date.json','w') as data:
            json.dump(self.tarefas,data)
    
    def loadData(self,*args):
        try:
            with open(self.path+'data.json','r') as data:
                self.tarefas=json.load(data)
        except FileNotFoundError:
            pass

    def removerWidget(self,tarefa):
        texto=tarefa.ids.label.text
        self.ids.box.remove_widget(tarefa)
        self.tarefas.remove(texto)
        self.saveData()

    def addWidget(self,button):
        texto = self.ids.texto.text
        self.ids.box.add_widget(Tarefa(text=texto))
        self.ids.texto.text = ''
        self.tarefas.append(texto)
        self.saveData() 
     


class Tarefa(BoxLayout):
    def __init__(self,text='',**kwargs):
        super().__init__(**kwargs)
        self.ids.label.text=text

class Test(App):
    def build(self):
        return Gerenciador() 

Test().run()