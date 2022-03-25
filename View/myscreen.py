import os


from kivymd.uix.dialog import MDDialog


from kivy.lang import Builder
from kivy.properties import ObjectProperty

from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import Screen

#from Kivy_MVC_Template.Utility.observer import Observer

from kivymd.uix.button import MDFlatButton


class MainScreen(MDScreen):
    """"
    A class that implements the visual presentation `MyScreenModel`.

    """

    # объект контроллера
    controller = ObjectProperty() # специальный подкласс
    # объект модели
    model = ObjectProperty()
    dialog = None

    def __init__(self, **kw):
        super().__init__(**kw)
        #self.dialog = None
        #self.model.add_observer(self)  # register the view as an observer


    def set_pet_name(self, name):
        return self.controller.set_pet_name(name)

    def set_birth(self, birth):
        self.controller.set_birth(birth)

    def set_last_appointment_date(self, app):
        self.controller.set_last_appointment_date(app)

    def set_vet_name(self, name):
        self.controller.set_vet_name(name)

    def set_disease(self, disease):
        self.controller.set_disease(disease)

    # запись данных пациента
    def record_patient_info(self):
        self.controller.record_patient_info()

    # поиск по имени и дню рождения
    def search_name_birth(self, pet_name, birth_date):
        self.controller.search_name_birth(pet_name, birth_date)

    #поиск по врачу и последнему посещению
    def search_last_appointment_vet_name(self, vet_name, last_appointment_date):
        self.controller.search_last_appointment_vet_name(vet_name, last_appointment_date)

    # удалить по имени и дате рождения
    def delete_pet_name_birth_date(self, pet_name, birth_date):
        self.controller.delete_pet_name_birth_date(pet_name, birth_date)

    # удаление по имени врача и дате последнего приёма
    def delete_vet_name_last_appointment_date(self, vet_name, last_appointment_date):
        self.controller.delete_vet_name_last_appointment_date(vet_name, last_appointment_date)

    # показ данных о пациентах
    def info(self):
        return self.controller.show_patient_info()

    def choose_birth_date(self):
        self.controller.choose_birth_date()


    def choose_last_appointment_date(self):
        self.controller.choose_last_appointment_date()

    def return_birth_date(self):
        return self.controller.return_birth_date()

    def set1(self):
        #self.ids.birth_date.text = str(k)
        #потому что нет объекта, поэтому не ставит(
        self.ids.birth_date = 'hel'
        #print('k',k)
        return 'he'

    # поиск по фразе из диагноза
    def search_disease(self, world):
        self.controller.find_disease(world)

    def show_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title = 'hello gues',
                text = 'hi hi',
                buttons =[
                    MDFlatButton(text='click')
                ]
            )
        self.dialog.open()

    def model_is_changed(self):
        """
        The method is called when the model changes.
        Requests and displays the value of the sum.
        """

        self.ids.result.text = str(self.model.full_name)


Builder.load_file(os.path.join(os.path.dirname(__file__), "myscreen.kv"))