from kivy.app import App 
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ListProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from kivy.utils import get_color_from_hex,hex_colormap
from functools import partial
import json
import random


red = [1,0,0,1]
green = [0,1,0,1]
blue =  [0,0,1,1]
purple = [1,0,1,1]
white = [1,1,1,1]
amarelo = [1,1,0,1]
colors=[red,green,blue,purple,amarelo,white]
colorDict={'red': [1,0,0,1],
        'green':[0,1,0,1],
        'blue':[0,0,1,1],
        'purple':[1,0,1,1],
        'amarelo':[1,1,0,1],
        'white':[1,1,0,1]}
    

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
        #colors=[red,green,blue,purple]
        usedColor=[]
        for i in range(7):
            color=random.choice(colors)
            print(color)          
            if color not in usedColor :
                btn=Button(text="Button #%s" % (i+1),background_color=color,on_release=self.upScore)
                usedColor.append(color)
                self.ids.btnBox.add_widget(btn)
        Window.bind(on_keyboard=self.voltar)
     

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.voltar)

    def voltar(self,window,key,*args):
        if key == 27:
            App.get_running_app().root.current='menu'
            #print(key)
            return True
    def btncolor(self,color,instance):
        print(color)
        print(str(instance.color))
        indexSplit=str(instance.text.split("#"))
        print(indexSplit)
        self.index=indexSplit[1]
        self.btnColor=str(instance.background_color)
        
        print(self.index)
        print(self.btnColor)
        print("==============")

    def upScore(self,*args):
        # score=self.ids.score.text
        self.ids.score.text= str(int(self.ids.score.text)+1)
        self.popSound.play()
        colorQuestion=random.choice(colorList)
        self.ids.box.clear_widgets()
        self.ids.box.add_widget(Label(text='Qual o botão com a cor '+colorQuestion+' ?',font_size=30,size_hint_y=None,height=200))
        self.ids.btnBox.clear_widgets()
       
        k=0
        usedColor=[]
        for i in range(7):
            color=random.choice(colors)
            #print(str(Color(tuple(color))))            
            if color not in usedColor :
                k=k+1
                btn=Button(text="Button #%s" % (k),background_color=color,on_release=self.upScore,on_press=lambda *args: self.btncolor(color,*args))
                #print('btn'+str(btn)) #btn<kivy.uix.button.Button object at 
                usedColor.append(color)
                self.ids.btnBox.add_widget(btn)                
        if (get_color_from_hex(hex_colormap['red'])in usedColor):
            print("ok")
        else:
            print(self.index)
            print(self.btnColor)
            #indexList=int(self.index[1])-1
            #print(usedColor[indexList])
            print(' '.join(str(usedColor)))   
        return Tarefas()
   
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