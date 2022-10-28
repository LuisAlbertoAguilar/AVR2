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
    def add_Diagnostico_TrenMotrizSetPoint(self):
        currentStr = self.ids.trenSP.text
        currentLst = currentStr.split(' '+'km/h')
        currentNum = int(currentLst[0])
        currentNum += 1
        if currentNum >= 90:
            currentNum = 90
        self.ids.trenSP.text = str(currentNum)+' '+'km/h'
        global arduino
        global trenSP
        global trenEnable
        global trenReversa
        global trenLimVel1
        global trenLimVel2
        trenSP = str(currentNum)
        arduinoString = "84 5 " + str(trenSP) + " " + str(trenEnable) + " " + str(trenReversa) + " " + str(trenLimVel1) + " " + str(trenLimVel2) 
        print(arduinoString)
        arduino.write(arduinoString.encode())


    def subs_Diagnostico_TrenMotriz_SetPoint(self):
        currentStr = self.ids.trenSP.text
        currentLst = currentStr.split(' '+'km/h')
        currentNum = int(currentLst[0])
        currentNum -= 1
        if currentNum <= 0:
            currentNum = 0
        self.ids.trenSP.text = str(currentNum)+' '+'km/h'
        global arduino
        global trenSP
        global trenEnable
        global trenReversa
        global trenLimVel1
        global trenLimVel2
        trenSP = str(currentNum)
        arduinoString = "84 5 " + str(trenSP) + " " + str(trenEnable) + " " + str(trenReversa) + " " + str(trenLimVel1) + " " + str(trenLimVel2)
        print(arduinoString)
        arduino.write(arduinoString.encode())


    def add_Diagnostico_Direccion(self):
        currentStr = self.ids.direccionSP.text
        currentLst = currentStr.split('°')
        currentNum = int(currentLst[0])
        currentNum += 1
        if currentNum >= 90:
            currentNum = 90
        self.ids.direccionSP.text = str(currentNum)+'°'
        global direccionSP
        global arduino
        direccionSP = str(currentNum)
        arduinoString = "83 1 " + (direccionSP)
        print(arduinoString)
        arduino.write(arduinoString.encode())


    def subs_Diagnostico_Direccion(self):
        currentStr = self.ids.direccionSP.text
        currentLst = currentStr.split('°')
        currentNum = int(currentLst[0])
        currentNum -= 1
        if currentNum <= -90:
            currentNum = -90
        self.ids.direccionSP.text = str(currentNum)+'°'
        global direccionSP
        global arduino
        direccionSP = str(currentNum)
        arduinoString = "83 1 " + (direccionSP)
        print(arduinoString)
        arduino.write(arduinoString.encode())


    # TODO: checar límites frenos
    def add_Diagnostico_FrenoTrasero(self):
        currentStr = self.ids.frenoTraseroSP.text
        currentLst = currentStr.split('%')
        currentNum = int(currentLst[0])
        currentNum += 1
        if currentNum >= 100:
            currentNum = 100
        self.ids.frenoTraseroSP.text = str(currentNum) + '%'
        global frenoTraseroSP
        global arduino
        frenoTraseroSP = str(currentNum)
        arduinoString = "66 1 " + (frenoTraseroSP)
        print(arduinoString)
        arduino.write(arduinoString.encode())


    def subs_Diagnostico_FrenoTrasero(self):
        currentStr = self.ids.frenoTraseroSP.text
        currentLst = currentStr.split('%')
        currentNum = int(currentLst[0])
        currentNum -= 1
        if currentNum <= 0:
            currentNum = 0
        self.ids.frenoTraseroSP.text = str(currentNum) + '%'
        global frenoTraseroSP
        global arduino
        frenoTraseroSP = str(currentNum)
        arduinoString = "66 1 " + (frenoTraseroSP)
        print(arduinoString)
        arduino.write(arduinoString.encode())


    def add_Diagnostico_FrenoDelantero(self):
        currentStr = self.ids.frenoDelanteroSP.text
        currentLst = currentStr.split('%')
        currentNum = int(currentLst[0])
        currentNum += 1
        if currentNum >= 100:
            currentNum = 100
        self.ids.frenoDelanteroSP.text = str(currentNum) + '%'
        global frenoDelanteroSP
        global arduino
        frenoDelanteroSP = str(currentNum)
        arduinoString = "68 1 " + (frenoDelanteroSP)
        print(arduinoString)
        arduino.write(arduinoString.encode())


    def subs_Diagnostico_FrenoDelantero(self):
        currentStr = self.ids.frenoDelanteroSP.text
        currentLst = currentStr.split('%')
        currentNum = int(currentLst[0])
        currentNum -= 1
        if currentNum <= 0:
            currentNum = 0
        self.ids.frenoDelanteroSP.text = str(currentNum) + '%'
        global arduino
        global frenoDelanteroSP
        frenoDelanteroSP = str(currentNum)
        arduinoString = "68 1 " + (frenoDelanteroSP)
        print(arduinoString)
        arduino.write(arduinoString.encode())

    def button_trenEnable(self):
        global trenEnable
        trenEnable = not trenEnable
        if trenEnable:
            self.ids['enableButton'].background_color = (0, 1, 0, 1)
        else:
            self.ids['enableButton'].background_color = (1, 0, 0, 1)
        global arduino
        global trenSP
        global trenReversa
        global trenLimVel1
        global trenLimVel2
        arduinoString = "84 5" + str(trenSP) + " " + ("1" if trenEnable else "0") + " " + ("1" if trenReversa else "0") + " " + ("1" if trenLimVel1 else "0") + " " + ("1" if trenLimVel2 else "0")
        print(arduinoString)
        arduino.write(arduinoString.encode())

    def button_trenReversa(self):
        global trenReversa
        trenReversa = not trenReversa
        if trenReversa:
            self.ids['reversaButton'].background_color = (0, 1, 0, 1)
        else:
            self.ids['reversaButton'].background_color = (1, 0, 0, 1)
        global arduino
        global trenSP
        global trenEnable
        global trenLimVel1
        global trenLimVel2
        arduinoString = "84 5" + str(trenSP) + " " + ("1" if trenEnable else "0") + " " + ("1" if trenReversa else "0") + " " + ("1" if trenLimVel1 else "0") + " " + ("1" if trenLimVel2 else "0")        
        print(arduinoString)
        arduino.write(arduinoString.encode())

    def button_trenLim1(self):
        global trenLimVel1
        trenLimVel1 = not trenLimVel1
        if trenLimVel1:
            self.ids['lim1Button'].background_color = (0, 1, 0, 1)
        else:
            self.ids['lim1Button'].background_color = (1, 0, 0, 1)
        global arduino
        global trenSP
        global trenEnable
        global trenReversa
        global trenLimVel2
        arduinoString = "84 5" + str(trenSP) + " " + ("1" if trenEnable else "0") + " " + ("1" if trenReversa else "0") + " " + ("1" if trenLimVel1 else "0") + " " + ("1" if trenLimVel2 else "0")        
        print(arduinoString)
        arduino.write(arduinoString.encode())

    def button_trenLim2(self):
        global trenLimVel2
        trenLimVel2 = not trenLimVel2
        if trenLimVel2:
            self.ids['lim2Button'].background_color = (0, 1, 0, 1)
        else:
            self.ids['lim2Button'].background_color = (1, 0, 0, 1)
        global arduino
        global trenSP
        global trenEnable
        global trenReversa
        global trenLimVel1
        arduinoString = "84 5" + str(trenSP) + " " + ("1" if trenEnable else "0") + " " + ("1" if trenReversa else "0") + " " + ("1" if trenLimVel1 else "0") + " " + ("1" if trenLimVel2 else "0")        
        print(arduinoString)
        arduino.write(arduinoString.encode())

    

        # global arduino
        # global frenoDelanteroSP
        # frenoDelanteroSP = str(currentNum)
        # arduinoString = "68 1 " + (frenoDelanteroSP)
        # print(arduinoString)
        # arduino.write(arduinoString.encode())
        
################################################################################
#     def add_Diagnostico_Velocidad(self):
#         currentStr = self.ids.diagnostico_referencia_velocidad.text
#         currentLst = currentStr.split(' '+'km/h')
#         currentNum = int(currentLst[0])
#         currentNum += 1
#         if currentNum >= 90:
#             currentNum = 90
#         self.ids.diagnostico_referencia_velocidad.text = str(currentNum)+' '+'km/h'
#         global nuevo_diagnostico_referencia_velocidad_ValueStr
#         nuevo_diagnostico_referencia_velocidad_ValueStr = str(currentNum)

#     def subs_Diagnostico_Velocidad(self):
#         currentStr = self.ids.diagnostico_referencia_velocidad.text
#         currentLst = currentStr.split(' '+'km/h')
#         currentNum = int(currentLst[0])
#         currentNum -= 1
#         if currentNum <= 0:
#             currentNum = 0
#         self.ids.diagnostico_referencia_velocidad.text = str(currentNum)+' '+'km/h'
#         global nuevo_diagnostico_referencia_velocidad_ValueStr
#         nuevo_diagnostico_referencia_velocidad_ValueStr = str(currentNum)
# ################################################################################
#     def add_Diagnostico_Frenos_Delanteros(self):
#         currentStr = self.ids.diagnostico_referencia_frenos_delanteros.text
#         currentLst = currentStr.split(' '+'%')
#         currentNum = int(currentLst[0])
#         currentNum += 1
#         if currentNum >= 90:
#             currentNum = 90
#         self.ids.diagnostico_referencia_frenos_delanteros.text = str(currentNum)+' '+'%'
#         global nuevo_diagnostico_referencia_frenos_delanteros_ValueStr
#         nuevo_diagnostico_referencia_frenos_delanteros_ValueStr = str(currentNum)

#     def subs_Diagnostico_Frenos_Delanteros(self):
#         currentStr = self.ids.diagnostico_referencia_frenos_delanteros.text
#         currentLst = currentStr.split(' '+'%')
#         currentNum = int(currentLst[0])
#         currentNum -= 1
#         if currentNum <= 0:
#             currentNum = 0
#         self.ids.diagnostico_referencia_frenos_delanteros.text = str(currentNum)+' '+'%'
#         global nuevo_diagnostico_referencia_frenos_delanteros_ValueStr
#         nuevo_diagnostico_referencia_frenos_delanteros_ValueStr = str(currentNum)
# ################################################################################
#     def add_Diagnostico_Frenos_Traseros(self):
#         currentStr = self.ids.diagnostico_referencia_frenos_traseros.text
#         currentLst = currentStr.split(' '+'%')
#         currentNum = int(currentLst[0])
#         currentNum += 1
#         if currentNum >= 90:
#             currentNum = 90
#         self.ids.diagnostico_referencia_frenos_traseros.text = str(currentNum)+' '+'%'
#         global nuevo_diagnostico_referencia_frenos_traseros_ValueStr
#         nuevo_diagnostico_referencia_frenos_traseros_ValueStr = str(currentNum)
        
#     def modoconduccion(self):
#         self.driving=True
        
#     def subs_Diagnostico_Frenos_Traseros(self):
#         currentStr = self.ids.diagnostico_referencia_frenos_traseros.text
#         currentLst = currentStr.split(' '+'%')
#         currentNum = int(currentLst[0])
#         currentNum -= 1
#         if currentNum <= 0:
#             currentNum = 0
#         self.ids.diagnostico_referencia_frenos_traseros.text = str(currentNum)+' '+'%'
#         global nuevo_diagnostico_referencia_frenos_traseros_ValueStr
#         nuevo_diagnostico_referencia_frenos_traseros_ValueStr = str(currentNum)
###############################################################################

    def update_Diagnostico_Referencia_Direccion(self):
        return nuevo_diagnostico_referencia_direccion_ValueStr

    def update_Diagnostico_Referencia_Velocidad(self):
        return trenValActual

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
    trenSP = ObjectProperty(0)
    trenValActual = ObjectProperty(0)
    direccionSP = ObjectProperty(0)
    direccionValActual = ObjectProperty(0)
    frenoTraseroSP = ObjectProperty(0)
    frenoTraseroValActual = ObjectProperty(0)
    frenoDelanteroSP = ObjectProperty(0)
    frenoDelanteroValActual = ObjectProperty(0)

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
        # TODO: regresar valores
        global trenSP
        trenSP = 3
        global trenEnable
        trenEnable = True
        global trenReversa
        trenReversa = False
        global trenLimVel1
        trenLimVel1 = False
        global trenLimVel2
        trenLimVel2 = False
        global trenValActual
        trenValActual = 0
        global direccionSP
        direccionSP = 0
        global direccionValActual
        direccionValActual = 10
        global frenoTraseroSP
        frenoTraseroSP = 0
        global frenoTraseroValActual
        frenoTraseroValActual = 0
        global frenoDelanteroSP
        frenoDelanteroSP = 0
        global frenoDelanteroValActual
        frenoDelanteroValActual = 0



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
        # TODO: regresar arduino
        try:
            global arduino
            arduino = serial.Serial('/dev/ttyUSB0',115200, timeout = 0.5)
        except:
            print('Sin comunicación.')

		#Inicia la comunicación para que Arduino pueda contestar con eco
		#Si no se envía una cadena al inicio, Arduino jamás responderá debido al SerialEvent()

		#Todos los arrays de caracteres deben terminar en # para que arduino sepa que una línea completa ha sido recibida
        initValStr = '0 0 0 0 #'

        # TODO: regresar arduino
        # self.arduino.write(initValStr.encode())
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
        Button:
            text: 'Enable'
            bold: True
            id: enableButton
            background_color: (0, 1, 0, 1)
            on_release: root.button_trenEnable()
        Button:
            text: 'Reversa'
            bold: True
            background_color: (1,0,0,1)
            id: reversaButton
            on_release: root.button_trenReversa()
        Button:
            text: 'Límite 1'
            bold: True
            id: lim1Button
            background_color: (1,0,0,1)
            on_release: root.button_trenLim1()
        Button:
            text: 'Límite 2'
            bold: True
            id: lim2Button
            background_color: (1,0,0,1)
            on_release: root.button_trenLim2()
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
            text:'Tren SP'
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
            on_release: root.add_Diagnostico_TrenMotrizSetPoint()
        MDLabel:
            id: trenSP
            text: str(app.trenSP)
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
            on_release: root.subs_Diagnostico_TrenMotriz_SetPoint()
        MDLabel:
            id: trenValActual
            text: str(app.trenValActual) + ' km/h'
            font_size: "20sp"
            halign:'center'
            pos_hint:{'center_y': 0.2}
################################################################################
        MDLabel:
            text:'Dirección SP'
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
            id: direccionSP
            text: str(app.direccionSP)
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
            text: str(app.direccionValActual)  + '°'
            font_size: "20sp"
            halign:'center'
            pos_hint:{'center_y': 0.2}
################################################################################

        MDLabel:
            text:'Frenos Traseros SP'
            font_size: "20sp"
            halign:'center'
        Button:
            text:"+"
            font_size:"50sp"
            halign:"right"
            valign:"middle"
            size: 30,30
            background_color: (0,1,0,1)
            on_release: root.add_Diagnostico_FrenoTrasero()
        MDLabel:
            id: frenoTraseroSP
            text: str(app.frenoTraseroSP)
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
            on_release: root.subs_Diagnostico_FrenoTrasero()
        MDLabel:
            id: frenoTraseroValActual
            text: str(app.frenoTraseroValActual) + '%'
            font_size: "20sp"
            halign:'center'
            pos_hint:{'center_y': 0.2}
################################################################################
        MDLabel:
            text:'Frenos Delanteros SP'
            font_size: "20sp"
            halign:'center'
        Button:
            text: "+"
            font_size:"50sp"
            halign:"right"
            valign:"middle"
            size: 30,30
            background_color: (0,1,0,1)
            on_release: root.add_Diagnostico_FrenoDelantero()
        MDLabel:
            id: frenoDelanteroSP
            text: str(app.frenoDelanteroSP)
            font_size: "20sp"
            halign:'center'
        Button:
            text:"-"
            font_size:"50sp"
            halign:"right"
            valign:"middle"
            size: 30,30
            background_color: (0,0,1,1)
            on_release: root.subs_Diagnostico_FrenoDelantero()
        MDLabel:
            id: frenoDelanteroValActual
            text: str(app.frenoDelanteroValActual)  + '%'
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
        # TODO: regresar arduino

        # arduino = self.arduino


        # TODO: checar si es necesario lo siguiente
        #Pasa los estados modificados a la pantalla de Diagnóstico
        # classObj = Diagnostico()
        #Actualización de variables de Referencia
        # diagnostico_referencia_direccion_ValueStr = classObj.update_Diagnostico_Referencia_Direccion()
        # diagnostico_referencia_velocidad_ValueStr = classObj.update_Diagnostico_Referencia_Velocidad()
        # diagnostico_referencia_frenos_delanteros_ValueStr = classObj.update_Diagnostico_Referencia_Frenos_Delanteros()
        # diagnostico_referencia_frenos_traseros_ValueStr = classObj.update_Diagnostico_Referencia_Frenos_Traseros()

        #Buffer a enviar
        Valores_Actuales_Str = str(trenSP) + ' ' + str(trenEnable) + ' ' + str(trenReversa) + ' ' + str(trenLimVel1) + ' ' + str(trenLimVel2) + ' ' + str(trenValActual) + ' ' + str(direccionSP)+ ' ' + str(direccionValActual)+ ' ' + str(frenoTraseroSP) + ' ' + str(frenoTraseroValActual) + ' ' + str(frenoDelanteroSP) + ' ' + str(frenoDelanteroValActual) 
         # diagnostico_referencia_direccion_ValueStr + ' ' +  diagnostico_referencia_velocidad_ValueStr + ' ' +  diagnostico_referencia_frenos_delanteros_ValueStr + ' ' +  diagnostico_referencia_frenos_traseros_ValueStr + ' ' + '#'

        #Convierte a Lista el String
        Valores_Actuales_Lst = Valores_Actuales_Str.split()

        #Imprime la Lista
        print('                                                     ')
        #print('Envío de valores:',Valores_Actuales_Lst)

        # try:
        #     # print(Valores_Actuales_Str)                                         #Este se envía a Arduino
        # except:
        #     print('AYUDA!')

        #Actualización de valores en REFERENCIA de la pantalla DIAGNÓSTICO en la INTERFAZ
        # self.diagnostico_referencia_velocidad_ValueInt = (Valores_Actuales_Lst[1]) +' '+'km/h'
        self.trenSP = (Valores_Actuales_Lst[0])+' '+'km/h'
        # self.trenValActual = (Valores_Actuales_Lst[5])+' '+'km/h'
        self.direccionSP = (Valores_Actuales_Lst[6]) + '°'
        # self.direccionValActual = (Valores_Actuales_Lst[7]) + '°'
        self.frenoTraseroSP = (Valores_Actuales_Lst[8]) + '%'
        # self.frenoTraseroValActual = (Valores_Actuales_Lst[9]) + '%'
        self.frenoDelanteroSP = (Valores_Actuales_Lst[10]) + '%'
        # self.frenoDelanteroValActual = (Valores_Actuales_Lst[11]) + '%'

        #Buffer y eco a arduino
        # TODO: regresar arduino
        # self.arduino.write(Valores_Actuales_Str.encode())

    def recibo(self,*args):

            #Recepción y Almacenamiento de Datos
            TODO: regresar arduino
            global arduino
            # Lectura_Str = arduino.read(size=200).decode()

            #print('Recibimiento de valores:',Lectura_Str)
            # Lectura_Str = "84 5 8 False False False False 56"
            lectura_l = Lectura_Str.split()
            # print(lectura_l)
            # lectura_l=Lectura_Str.split("%")
            classObj = Diagnostico()

            #Actualización de variables de Referencia
            diagnostico_referencia_direccion_ValueStr = classObj.update_Diagnostico_Referencia_Direccion()
            diagnostico_referencia_velocidad_ValueStr = classObj.update_Diagnostico_Referencia_Velocidad()
            diagnostico_referencia_frenos_delanteros_ValueStr = classObj.update_Diagnostico_Referencia_Frenos_Delanteros()
            diagnostico_referencia_frenos_traseros_ValueStr = classObj.update_Diagnostico_Referencia_Frenos_Traseros()

            # TODO: regresar arduino
            # TODO: actualizar a que se editen valores actuales 
            # self.trenSP = 
            try:
                if lectura_l[0] == "84":
                    self.trenEnable = lectura_l[3]
                    self.trenReversa = lectura_l[4]
                    self.trenLimVel1 = lectura_l[5]
                    self.trenLimVel2 = lectura_l[6]
                    self.trenValActual = lectura_l[7]
                #     print(trenSP)
                #     # self.diagnostico_sensor_direccion_ValueInt = lectura_l[3] 
                #     # self.diagnostico_referencia_velocidad = lectura_l[4]
                #     # self.diagnostico_referencia_frenos_delanteros_ValueInt = lectura_l[5]
                #     #Valores_Actuales_Str = self.diagnostico_sensor_direccion_ValueInt + ' ' lectura_l[4] + ' ' lectura_l[5] + '#'
                if lectura_l[0] == "116":
                    self.trenValActual = lectura_l[2]

                # if lectura_l[0] == "83":
                #     self.direccionSP = lectura_l[2]

                if lectura_l[0] == "115":
                    self.direccionValActual = lectura_l[2]

                # if lectura_l[0] == "66":
                #     self.frenoTraseroSP = lectura_l[2]

                if lectura_l[0] == "98":
                    self.frenoTraseroValActual = lectura_l[2]

                # if lectura_l[0] == "68":
                #     self.frenoDelanteroSP = lectura_l[2]

                if lectura_l[0] == "100":
                    self.frenoDelanteroValActual = lectura_l[2]





                print(self.driving)
            
                 # + self.frenoDelanteroValActual +self.frenoTraseroValActual)
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
