from kivy import Config
Config.set('graphics', 'multisamples', '0')
Config.set('kivy','window_icon','icon.ico')
from kivy.app import App

from kivy.graphics import Color,Rectangle

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from urllib.error import HTTPError

from theotown import search,download

class TestApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        layout.size_hint = (1,1)
        btn_search =  Button(text='Search')
        btn_search.bind(on_press=self.search)
        btn_search.background_color = (32/255,126/255,204/255,1)
        inputAndSearch = BoxLayout(orientation='horizontal')
        inputAndSearch.size_hint = (1.0, 0.1)
        self.text_input = TextInput()
        self.text_input.multiline = False
        self.text_input.bind(on_text_validate=self.search)
        inputAndSearch.add_widget(self.text_input)
        inputAndSearch.add_widget(btn_search)
        results_holder = ScrollView(size_hint=(1, 0.9))
        self.results = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.results.bind(minimum_height=self.results.setter('height'))
        
        layout.add_widget(inputAndSearch)
        results_holder.add_widget(self.results)
        layout.add_widget(results_holder)
        return layout
    def search(self,_):
        self.results.clear_widgets()
        a = search(str(self.text_input.text))
        if len(a.ls) == 0:
            self.results.add_widget(Label(text='No resuls found :('))
        for i in a.ls:
            lay = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            btn = Button(text='Download')
            btn.url = i['link']
            btn.bind(on_press=self.download)
            btn.background_color = (0.82,0.82,0.82,1)
            d = Label(text=i['name'])
            lay.add_widget(d)
            lay.add_widget(btn)
            self.results.add_widget(lay)#len(self.results.children)*16))
    def download(self,btn):
        btn.text = 'Downloading...'
        try:
            download(btn.url)
            btn.text = 'Downloaded!'
        except HTTPError:
            btn.text = 'Not valid format :('
        except SystemExit:
            btn.text = 'Not valid format :('

TestApp().run()
