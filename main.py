from kivymd.app import MDApp

from Controller.myscreen import Controller
from Model.myscreen import Model


class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.model = Model()
        self.controller = Controller(self.model)

    def build(self):
        return self.controller.get_screen()


MyApp().run()
