import sys

# Thư viện chính
from back_end import *
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

#print("Python version:", sys.version)
#print("Kivy version:", kivy.__version__)

# On/off/other fucntion
def on():
    pass
def off():
    quit()
def shift():
    pass
def alpha():
    pass

# Kiểm tra thử có chạy layout + button không
class TestApp(App):
    def build(self):
        layout = GridLayout(cols=3)
        layout.add_widget(Button(text="1"))
        layout.add_widget(Button(text="2"))
        layout.add_widget(Button(text="3"))
        layout.add_widget(Button(text="+"))
        layout.add_widget(Button(text="-"))
        layout.add_widget(Button(text="="))
        return layout

if __name__ == "__main__":
    TestApp().run()