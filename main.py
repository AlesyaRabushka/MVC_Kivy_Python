from kivymd.app import MDApp

from Controller.myscreen import Controller


class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = Controller(12)

    def build(self):
        return self.controller.get_screen()


MyApp().run()
