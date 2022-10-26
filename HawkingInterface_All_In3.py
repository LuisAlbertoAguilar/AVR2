#Librerías para crear la interfaz
from kivy.app import App
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList
from kivy.properties import StringProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineIconListItem, MDList
from kivymd.icon_definitions import md_icons
from kivy.config import Config
from kivymd.uix.button import MDRectangleFlatButton
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.properties import ObjectProperty
import threading

#Librería para Arduino
import serial

#Librería de fecha y hora
import time
from datetime import date

#Tamaño de la ventana
from kivy.core.window import Window
Window.size=(800, 530)

class MenuPrincipal(Screen):
    pass

class Diagnostico(Screen):

    def Reset(self):
        self.diagnostico_sensor_direccion_ValueInt = '0'+'°'
        self.diagnostico_sensor_velocidad_ValueInt = '0'+' '+'km/h'
        self.diagnostico_sensor_frenos_delanteros_ValueInt = '0'+' '+'%'
        self.diagnostico_sensor_frenos_traseros_ValueInt = '0'+' '+'%'
################################################################################
    def add_Diagnostico_Direccion(self):
        currentStr = self.ids.diagnostico_referencia_direccion.text
        currentLst = currentStr.split('°')
        currentNum = int(currentLst[0])
        currentNum += 1
        if currentNum >= 90:
            currentNum = 90
        self.ids.diagnostico_referencia_direccion.text = str(currentNum)+'°'
        global nuevo_diagnostico_referencia_direccion_ValueStr
        nuevo_diagnostico_referencia_direccion_ValueStr = str(currentNum)

    def subs_Diagnostico_Direccion(self):
        currentStr = self.ids.diagnostico_referencia_direccion.text
        currentLst = currentStr.split('°')
        currentNum = int(currentLst[0])
        currentNum -= 1
        if currentNum <= -90:
            currentNum = -90
        self.ids.diagnostico_referencia_direccion.text = str(currentNum)+'°'
        global nuevo_diagnostico_referencia_direccion_ValueStr
        nuevo_diagnostico_referencia_direccion_ValueStr = str(currentNum)
################################################################################
    def add_Diagnostico_Velocidad(self):
        currentStr = self.ids.diagnostico_referencia_velocidad.text
        currentLst = currentStr.split(' '+'km/h')
        currentNum = int(currentLst[0])
        currentNum += 1
        if currentNum >= 90:
            currentNum = 90
        self.ids.diagnostico_referencia_velocidad.text = str(currentNum)+' '+'km/h'
        global nuevo_diagnostico_referencia_velocidad_ValueStr
        nuevo_diagnostico_referencia_velocidad_ValueStr = str(currentNum)

    def subs_Diagnostico_Velocidad(self):
        currentStr = self.ids.diagnostico_referencia_velocidad.text
        currentLst = currentStr.split(' '+'km/h')
        currentNum = int(currentLst[0])
        currentNum -= 1
        if currentNum <= 0:
            currentNum = 0
        self.ids.diagnostico_referencia_velocidad.text = str(currentNum)+' '+'km/h'
        global nuevo_diagnostico_referencia_velocidad_ValueStr
        nuevo_diagnostico_referencia_velocidad_ValueStr = str(currentNum)
################################################################################
    def add_Diagnostico_Frenos_Delanteros(self):
        currentStr = self.ids.diagnostico_referencia_frenos_delanteros.text
        currentLst = currentStr.split(' '+'%')
        currentNum = int(currentLst[0])
        currentNum += 1
        if currentNum >= 90:
            currentNum = 90
        self.ids.diagnostico_referencia_frenos_delanteros.text = str(currentNum)+' '+'%'
        global nuevo_diagnostico_referencia_frenos_delanteros_ValueStr
        nuevo_diagnostico_referencia_frenos_delanteros_ValueStr = str(currentNum)

    def subs_Diagnostico_Frenos_Delanteros(self):
        currentStr = self.ids.diagnostico_referencia_frenos_delanteros.text
        currentLst = currentStr.split(' '+'%')
        currentNum = int(currentLst[0])
        currentNum -= 1
        if currentNum <= 0:
            currentNum = 0
        self.ids.diagnostico_referencia_frenos_delanteros.text = str(currentNum)+' '+'%'
        global nuevo_diagnostico_referencia_frenos_delanteros_ValueStr
        nuevo_diagnostico_referencia_frenos_delanteros_ValueStr = str(currentNum)
################################################################################
    def add_Diagnostico_Frenos_Traseros(self):
        currentStr = self.ids.diagnostico_referencia_frenos_traseros.text
        currentLst = currentStr.split(' '+'%')
        currentNum = int(currentLst[0])
        currentNum += 1
        if currentNum >= 90:
            currentNum = 90
        self.ids.diagnostico_referencia_frenos_traseros.text = str(currentNum)+' '+'%'
        global nuevo_diagnostico_referencia_frenos_traseros_ValueStr
        nuevo_diagnostico_referencia_frenos_traseros_ValueStr = str(currentNum)
        
    def modoconduccion(self):
        self.driving=True
        
    def subs_Diagnostico_Frenos_Traseros(self):
        currentStr = self.ids.diagnostico_referencia_frenos_traseros.text
        currentLst = currentStr.split(' '+'%')
        currentNum = int(currentLst[0])
        currentNum -= 1
        if currentNum <= 0:
            currentNum = 0
        self.ids.diagnostico_referencia_frenos_traseros.text = str(currentNum)+' '+'%'
        global nuevo_diagnostico_referencia_frenos_traseros_ValueStr
        nuevo_diagnostico_referencia_frenos_traseros_ValueStr = str(currentNum)
###############################################################################

    def update_Diagnostico_Referencia_Direccion(self):
        return nuevo_diagnostico_referencia_direccion_ValueStr

    def update_Diagnostico_Referencia_Velocidad(self):
        return nuevo_diagnostico_referencia_velocidad_ValueStr

    def update_Diagnostico_Referencia_Frenos_Delanteros(self):
        return nuevo_diagnostico_referencia_frenos_delanteros_ValueStr

    def update_Diagnostico_Referencia_Frenos_Traseros(self):
        return nuevo_diagnostico_referencia_frenos_traseros_ValueStr

###############################################################################

class ModoManual(Screen):
    pass

class Reset(Screen):
    pass

sm=ScreenManager()
sm.add_widget(MenuPrincipal(name = 'menu'))
sm.add_widget(Diagnostico(name = 'diagnostico'))
sm.add_widget(ModoManual(name = 'modo_manual'))
sm.add_widget(Reset(name = 'reset'))

class HawkingInterface(MDApp):
    #Variable que despliega el tiempo de compilación
    tiempo = time.asctime()
    tiempo = '          ' + tiempo

    #Variables enteras para el apartado REFERENCIA en DIAGNÓSTICO
    diagnostico_referencia_direccion_ValueInt = ObjectProperty(0)
    diagnostico_referencia_velocidad_ValueInt = ObjectProperty(0)
    diagnostico_referencia_frenos_delanteros_ValueInt = ObjectProperty(0)
    diagnostico_referencia_frenos_traseros_ValueInt = ObjectProperty(0)

    #Variables enteras para el apartado de SENSOR en DIAGNÓSTICO
    diagnostico_sensor_direccion_ValueInt = ObjectProperty(0)
    diagnostico_sensor_velocidad_ValueInt = ObjectProperty(0)
    diagnostico_sensor_frenos_delanteros_ValueInt = ObjectProperty(0)
    diagnostico_sensor_frenos_traseros_ValueInt = ObjectProperty(0)

    #Variables enteras en MODO MANUAL
    modo_manual_velocidad_ValueInt = ObjectProperty(0)
    modo_manual_bateria_ValueInt = ObjectProperty(0)
    
    #Variable del modo de conducción
    driving=False

    def build(self):
        #REFERENCIA
        #DIRECCIÓN de la pantalla DIAGNÓSTICO
        global diagnostico_referencia_direccion_ValueStr
        global nuevo_diagnostico_referencia_direccion_ValueStr
        diagnostico_referencia_direccion_ValueStr = '0'
        nuevo_diagnostico_referencia_direccion_ValueStr = '0'

        #VELOCIDAD de la pantalla DIAGNÓSTICO
        global diagnostico_referencia_velocidad_ValueStr
        global nuevo_diagnostico_referencia_velocidad_ValueStr
        diagnostico_referencia_velocidad_ValueStr  = '0'
        nuevo_diagnostico_referencia_velocidad_ValueStr = '0'

        #Variables para los FRENOS_DELANTEROS de la pantalla DIAGNÓSTICO
        global diagnostico_referencia_frenos_delanteros_ValueStr
        global nuevo_diagnostico_referencia_frenos_delanteros_ValueStr
        diagnostico_referencia_frenos_delanteros_ValueStr  = '0'
        nuevo_diagnostico_referencia_frenos_delanteros_ValueStr = '0'

        #Variables para los FRENOS_TRASEROS de la pantalla DIAGNÓSTICO
        global diagnostico_referencia_frenos_traseros_ValueStr
        global nuevo_diagnostico_referencia_frenos_traseros_ValueStr
        diagnostico_referencia_frenos_traseros_ValueStr  = '0'
        nuevo_diagnostico_referencia_frenos_traseros_ValueStr = '0'
        
        
################################################################################

        self.theme_cls.primary_palette = "Indigo"

        try:
            self.arduino = serial.Serial('/dev/ttyUSB0',115200, timeout = 0.5)
        except:
            print('Sin comunicación.')

		#Inicia la comunicación para que Arduino pueda contestar con eco
		#Si no se envía una cadena al inicio, Arduino jamás responderá debido al SerialEvent()

		#Todos los arrays de caracteres deben terminar en # para que arduino sepa que una línea completa ha sido recibida
        initValStr = '0 0 0 0 #'

        self.arduino.write(initValStr.encode())
        print('Bus initialized')

        Clock.schedule_interval(self.update, 1)
        Clock.schedule_interval(self.recibo, 1)

        HawkingDesign = Builder.load_string("""
ScreenManager:
    MenuPrincipal:
    Diagnostico:
    ModoManual:
    Reset:

<MenuPrincipal>
    name:'menu'
    MDToolbar:
        id: toolbar
        title: ''
        font_style: 'H5'
        elevation: 10
        pos_hint:{'center_y':0.93}
    MDGridLayout:
        cols: 2
        size: root.width, root.height
        Image:
            source: 'images/tec_borrego.png'
            halign: "center"
            MDLabel:
                text: app.tiempo
                font_style: 'H5'
                width: dp(500)
                halign: 'left'
                pos_hint: {'center_x': 0.6, 'center_y':0.9}
        MDBoxLayout:
            orientation: 'vertical'
            MDLabel:
            MDLabel:
            MDLabel:
            MDLabel:
            MDLabel:
                text: "INICIO"
                font_name: 'Roboto'
                bold: True
                font_size: "50"
                halign: "center"
                pos_hint: {'center_y':0.9}
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1
            MDLabel:
                text: "                                                                                                 Bienvenido a la Interfaz Hawking." #Todos esos espacios permiten que la línea se imprima en el segundo renglón
                italic: True
                font_size: "17"
                halign: "center"
                pos_hint: {'center_y':0.9}
            MDLabel:
            MDLabel:
                text: "OPCIONES"
                font_name: 'Roboto'
                bold: True
                font_size: "34"
                halign: "center"
                pos_hint: {'center_y':0.9}
                theme_text_color: "Custom"
                text_color: 0, 0, 0, 1
            MDLabel:
                text: "                                                                                                 Información de menús."
                italic: True
                halign: "center"
                pos_hint: {'center_y':0.9}
            MDLabel:
            MDFillRoundFlatIconButton:
                text: '  DIAGNÓSTICO  '
                icon:'car-cog'
                width: dp(500)
                pos_hint: {'center_x': 0.5, 'center_y':0.9}
                on_press:
                    root.manager.current= 'diagnostico'
                    root.manager.transition.direction= "left"
                    print("Diagnostico")
                    
            MDLabel:
                text: 'Envío de data sobre frenos o dirección.'
                font_name: 'Roboto'
                font_size: "17"
                halign: "center"
                pos_hint: {'center_x': 0.5, 'center_y':0.9}
            MDLabel:
            MDFillRoundFlatIconButton:
                text: 'MODO MANUAL'
                icon: 'steering'
                width: dp(500)
                pos_hint: {'center_x': 0.5, 'center_y':0.9}
                on_press:
                    root.manager.current= 'modo_manual'
                    root.manager.transition.direction= "left"
                    print("Manual")
                    on_release=root.modoconduccion()
                    app.driving=True
                    print(app.driving)
                    
            MDLabel:
                text: 'Conducción por parte del operador.'
                font_name: 'Roboto'
                font_size: "17"
                halign: "center"
                pos_hint: {'center_x': 0.5, 'center_y':0.9}
            MDLabel:
            MDLabel:

<Diagnostico>:
    name:'diagnostico'
    MDFillRoundFlatIconButton:
        icon:'home-circle'
        text: 'INICIO'
        pos_hint: {'center_x': 0.1, 'center_y':0.9}
        on_press:
            root.manager.current = 'menu'
            root.manager.transition.direction = "right"
    MDGridLayout:
        row_force_default:False
        row_default_height:50
        cols:5
        MDLabel:
        MDLabel:
        MDLabel:
        MDLabel:
        Button:
            text: 'RESET'
            bold: True
            background_color: (1,0,0,1)
            on_release: root.Reset()
################################################################################
        MDLabel:
            bold: True
            font_size: "20sp"
            halign:'center'
        MDLabel:
            text:''
            bold: True
            font_size: "20sp"
            halign:'center'
        MDLabel:
            text:'REFERENCIA'
            bold: True
            font_size: 25
            halign:'center'
        MDLabel:
            text:''
            bold: True
            font_size: "20sp"
            halign:'center'
        MDLabel:
            text:'SENSOR'
            bold: True
            font_size: 25
            halign:'center'
################################################################################
        MDLabel:
            text:'Dirección'
            font_size: "20sp"
            halign:'center'
        Button:
            text:"+"
            font_size:"50sp"
            halign:"right"
            valign:"middle"
            size: 30,30
            background_color: (0,1,0,1)
            on_release: root.add_Diagnostico_Direccion()
        MDLabel:
            id: diagnostico_referencia_direccion
            text: str(app.diagnostico_referencia_direccion_ValueInt)
            font_size: "20sp"
            halign:'center'
            pos_hint:{'center_y': 0.2}
        Button:
            text:"-"
            font_size:"50sp"
            halign:"right"
            valign:"middle"
            size: 30,30
            background_color: (0,0,1,1)
            on_release: root.subs_Diagnostico_Direccion()
        MDLabel:
            id: diagnostico_sensor_direccion
            text: str(app.diagnostico_sensor_direccion_ValueInt)
            font_size: "20sp"
            halign:'center'
            pos_hint:{'center_y': 0.2}
################################################################################
        MDLabel:
            text:'Velocidad'
            font_size: "20sp"
            halign:'center'
            pos_hint:{'center_y': 0.2}
        Button:
            text:"+"
            font_size:"50sp"
            halign:"right"
            valign:"middle"
            size: 30,30
            background_color: (0,1,0,1)
            on_release: root.add_Diagnostico_Velocidad()
        MDLabel:
            id: diagnostico_referencia_velocidad
            text: str(app.diagnostico_referencia_velocidad_ValueInt)
            font_size: "20sp"
            halign:'center'
            pos_hint:{'center_y': 0.2}
        Button:
            text:"-"
            font_size:"50sp"
            halign:"right"
            valign:"middle"
            size: 30,30
            background_color: (0,0,1,1)
            on_release: root.subs_Diagnostico_Velocidad()
        MDLabel:
            id: diagnostico_sensor_velocidad
            text: str(app.diagnostico_sensor_velocidad_ValueInt)
            font_size: "20sp"
            halign:'center'
            pos_hint:{'center_y': 0.2}
################################################################################
        MDLabel:
            text:'Frenos Delanteros'
            font_size: "20sp"
            halign:'center'
        Button:
            text:"+"
            font_size:"50sp"
            halign:"right"
            valign:"middle"
            size: 30,30
            background_color: (0,1,0,1)
            on_release: root.add_Diagnostico_Frenos_Delanteros()
        MDLabel:
            id: diagnostico_referencia_frenos_delanteros
            text: str(app.diagnostico_referencia_frenos_delanteros_ValueInt)
            font_size: "20sp"
            halign:'center'
            pos_hint:{'center_y': 0.2}
        Button:
            text:"-"
            font_size:"50sp"
            halign:"right"
            valign:"middle"
            size: 30,30
            background_color: (0,0,1,1)
            on_release: root.subs_Diagnostico_Frenos_Delanteros()
        MDLabel:
            id: diagnostico_sensor_frenos_delanteros
            text: str(app.diagnostico_sensor_frenos_delanteros_ValueInt)
            font_size: "20sp"
            halign:'center'
            pos_hint:{'center_y': 0.2}
################################################################################
        MDLabel:
            text:'Frenos      Traseros'
            font_size: "20sp"
            halign:'center'
        Button:
            text: "+"
            font_size:"50sp"
            halign:"right"
            valign:"middle"
            size: 30,30
            background_color: (0,1,0,1)
            on_release: root.add_Diagnostico_Frenos_Traseros()
        MDLabel:
            id: diagnostico_referencia_frenos_traseros
            text: str(app.diagnostico_referencia_frenos_traseros_ValueInt)
            font_size: "20sp"
            halign:'center'
        Button:
            text:"-"
            font_size:"50sp"
            halign:"right"
            valign:"middle"
            size: 30,30
            background_color: (0,0,1,1)
            on_release: root.subs_Diagnostico_Frenos_Traseros()
        MDLabel:
            id: diagnostico_sensor_frenos_traseros
            text: str(app.diagnostico_sensor_frenos_traseros_ValueInt)
            font_size: "20sp"
            halign:'center'

<ModoManual>:
    name:'modo_manual'
    MDLabel:
        text: "MODO MANUAL"
        font_name: 'Roboto'
        bold: True
        font_size: "60"
        halign: "center"
        pos_hint: {'center_y':0.9}
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1
        md_bg_color: 0, 0, 0, 1
    MDGridLayout:
        pos_hint:{"top":0.9}
        cols:2
        MDLabel:
        MDLabel:
        MDLabel:
            text:'VELOCIDAD'
            font_name: 'Roboto'
            bold: True
            font_size: "30"
            halign:'center'
            pos_hint:{'center_y': 0.9}
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            md_bg_color: 0, 0, 0, 1
        MDLabel:
            text:'BATERÍA'
            font_name: 'Roboto'
            bold: True
            font_size: "30"
            halign:'center'
            pos_hint:{'center_y': 0.9}
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            md_bg_color: 0, 0, 0, 1
        MDLabel:
            md_bg_color: 0, 0, 0, 1
        MDLabel:
            md_bg_color: 0, 0, 0, 1
        MDLabel:
            id: diagnostico_sensor_frenos_traseros
            text: str(app.modo_manual_velocidad_ValueInt)
            font_name: 'Roboto'
            bold: True
            font_size: "100"
            halign:'center'
            pos_hint:{'center_y': 0.9}
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            md_bg_color: 0, 0, 0, 1
        MDLabel:
            id: modo_manual_bateria
            text: str(app.modo_manual_bateria_ValueInt)
            font_name: 'Roboto'
            bold: True
            font_size: "100"
            halign:'center'
            pos_hint:{'center_y': 0.9}
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            md_bg_color: 0, 0, 0, 1
        MDLabel:
            md_bg_color: 0, 0, 0, 1
        MDLabel:
            md_bg_color: 0, 0, 0, 1
        MDLabel:
            text:'(km/h)'
            font_name: 'Roboto'
            italic: True
            font_size: "30"
            valigh: 'top'
            halign:'center'
            pos_hint:{'center_y': 0.5}
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            md_bg_color: 0, 0, 0, 1
        MDLabel:
            text:'(%)'
            font_name: 'Roboto'
            italic: True
            font_size: "30"
            valigh: 'top'
            halign:'center'
            pos_hint:{'center_y': 0.5}
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            md_bg_color: 0, 0, 0, 1
        MDLabel:
            md_bg_color: 0, 0, 0, 1
        MDLabel:
            md_bg_color: 0, 0, 0, 1
    MDFillRoundFlatIconButton:
        icon:'home-circle'
        text: 'INICIO'
        md_bg_color: 0, 0, 0, 1
        pos_hint: {'center_x': 0.1, 'center_y':0.9}
        on_press:
            root.manager.current = 'menu'
            root.manager.transition.direction = "right"

        """)
        return HawkingDesign

    def update(self,*args):

        #Inicio de conteo de tiempo
        start = time.time()

        arduino = self.arduino

        #Pasa los estados modificados a la pantalla de Diagnóstico
        classObj = Diagnostico()

        #Actualización de variables de Referencia
        diagnostico_referencia_direccion_ValueStr = classObj.update_Diagnostico_Referencia_Direccion()
        diagnostico_referencia_velocidad_ValueStr = classObj.update_Diagnostico_Referencia_Velocidad()
        diagnostico_referencia_frenos_delanteros_ValueStr = classObj.update_Diagnostico_Referencia_Frenos_Delanteros()
        diagnostico_referencia_frenos_traseros_ValueStr = classObj.update_Diagnostico_Referencia_Frenos_Traseros()

        #Buffer a enviar
        Valores_Actuales_Str = diagnostico_referencia_direccion_ValueStr + ' ' +  diagnostico_referencia_velocidad_ValueStr + ' ' +  diagnostico_referencia_frenos_delanteros_ValueStr + ' ' +  diagnostico_referencia_frenos_traseros_ValueStr + ' ' + '#'

        #Convierte a Lista el String
        Valores_Actuales_Lst = Valores_Actuales_Str.split()

        #Imprime la Lista
        print('                                                     ')
        #print('Envío de valores:',Valores_Actuales_Lst)

        try:
            print(Valores_Actuales_Str)                                         #Este se envía a Arduino
        except:
            print('AYUDA!')

        #Actualización de valores en REFERENCIA de la pantalla DIAGNÓSTICO en la INTERFAZ
        self.diagnostico_referencia_direccion_ValueInt = (Valores_Actuales_Lst[0]) + '°'
        self.diagnostico_referencia_velocidad_ValueInt = (Valores_Actuales_Lst[1]) +' '+'km/h'
        self.diagnostico_referencia_frenos_delanteros_ValueInt = (Valores_Actuales_Lst[2]) +' '+ '%'
        self.diagnostico_referencia_frenos_traseros_ValueInt = (Valores_Actuales_Lst[3]) +' '+ '%'

        #Buffer y eco a arduino
        arduino.write(Valores_Actuales_Str.encode())

    def recibo(self,*args):

            #Recepción y Almacenamiento de Datos
            Lectura_Str = self.arduino.read(size=200).decode()

            #print('Recibimiento de valores:',Lectura_Str)
            Lectura_Lst = Lectura_Str.split()
            #print(Lectura_Lst)
            lectura_l=Lectura_Str.split("%")
            print(self.driving)
            try:
                
                print(lectura_l[1])
                Lectura_post=str(lectura_l[1]).split()
                self.diagnostico_sensor_direccion_ValueInt = Lectura_post[0]+'°'
                self.diagnostico_sensor_velocidad_ValueInt = Lectura_post[1]+' '+'km/h'
                self.diagnostico_sensor_frenos_delanteros_ValueInt = Lectura_post[2]+' '+'%'
                self.diagnostico_sensor_frenos_traseros_ValueInt = Lectura_post[3]+' '+'%'

                #Asignación y actualización de variables en Modo Manual
                self.modo_manual_velocidad_ValueInt = Lectura_post[1]
                self.modo_manual_bateria_ValueInt = Lectura_post[4]
            except:
                pass
            

            #Esta función sirve verificar que los valores recibidos de Arduino estén completos
            #if(True):

                #Asignación y actualización de variables del Sensor en Diagnóstico
                

HawkingInterface().run()
