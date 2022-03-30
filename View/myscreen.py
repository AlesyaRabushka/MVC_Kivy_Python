import os
import datetime

import setuptools.extern
from kivymd.uix.dialog import MDDialog


from kivy.lang import Builder
from kivy.properties import ObjectProperty, BooleanProperty

from kivymd.uix.screen import MDScreen
from kivymd.uix.picker import MDDatePicker
from kivy.uix.screenmanager import Screen

from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.core.window import Window

from kivy.uix.widget import Widget

#from Kivy_MVC_Template.Utility.observer import Observer

from kivymd.uix.button import MDFlatButton


# popup window for pet data input
class AddPopup(Popup, Widget):
    """
    Is used for apply new pet
    """
    model = ObjectProperty()
    controller = ObjectProperty()

    def __init__(self, controller, model, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.controller = controller
        self.dialog = None

        self._ready = ''


    @property
    def ready(self):
        return self._ready
    @ready.setter
    def ready(self, ready):
        self._ready = ready


    def set_pet_name(self, name):
        self.controller.set_pet_name(name)

    def set_birth_date(self, birth):
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

    # показ данных о пациентах
    def info(self):
        return self.controller.show_patient_info()


    # установка даты рождения
    def choose_birth_date(self):
        date_dialog = MDDatePicker(min_year=2010, max_year=2022)
        date_dialog.bind(on_save=self.set_birth_date_calendar)
        date_dialog.open()

    def set_birth_date_calendar(self, instance, value, date_range):
        self.set_birth_date(str(value))
        self.ids.birth_date_input.text = str(value)


    # установка даты последнего посещения
    def choose_last_appointment_date(self):
        date_dialog = MDDatePicker(min_year=2000, max_year=2022)
        date_dialog.bind(on_save=self.set_last_appointment_date_calendar)
        date_dialog.open()

    def set_last_appointment_date_calendar(self, instance, value, date_range):
        self.ids.last_appointment_date_input.text = str(value)
        self.set_last_appointment_date(str(value))



    # is called after controller checked the input data
    def dialogs(self, right_info):
        # if all the fields are full
        if right_info == True:
            self.ready = True
            self.show_dialog()
        # if even one field is empty
        elif right_info == False:
            self.ready = False
            self.show_no_dialog()

    # is called when the pet information is successfully added
    def show_dialog(self):
        self.dialog = MDDialog(
            title='Регистрация данных',
            text='Запись добавлена!',
            buttons=[
                MDFlatButton(text='Ok', on_release=self.closed)
            ]
        )
        self.dialog.open()


    # is called when there is wrong pet information
    def show_no_dialog(self):
        self.dialog = MDDialog(
            title='Ошибка регистрации',
            text='Проверьте введенные вами данные!',
            # size_hint=(0.5,0.5),
            buttons=[
                MDFlatButton(text='Ok', on_release=self.no_closed)
            ]
        )
        self.dialog.open()


    def closed(self, text):
        self.dialog.dismiss()


    def no_closed(self, text):
        self.dialog.dismiss()


# popup window to search info
class SearchPopup(Popup, Widget):
    """
    Is used for search for particular pets records
    """
    model = ObjectProperty()
    controller = ObjectProperty()
    dialog = None
    def __init__(self, controller, model, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.controller = controller

        self.pet_name=''
        self.birth_date=''
        self.last_appointment_date=''
        self.vet_name = ''
        self.disease = ''

        self.options = []


    def set_search_pet_name(self, pet_name):
        self.pet_name = str(pet_name)

    def set_search_birth_date(self, birth_date):
        self.birth_date = str(birth_date)

    def set_search_last_appointment_date(self, last_app_date):
        self.last_appointment_date = last_app_date

    def set_search_vet_name(self, vet_name):
        self.vet_name = vet_name

    def set_search_disease_phrase(self, phrase):
        self.disease = phrase


    # set last appointment date by calendar widget
    def choose_search_last_appointment_date(self):
        date_dialog = MDDatePicker(min_year=2000, max_year=2022)
        date_dialog.bind(on_save=self.set_last_appointment_date_calendar)
        date_dialog.open()

    def set_last_appointment_date_calendar(self, instance, value, date_range):
        self.ids.last_appointment_date_search.text = str(value)
        self.set_search_last_appointment_date(str(value))

    # set birth date by calendar widget
    def choose_search_birth_date(self):
        date_dialog = MDDatePicker(min_year=2000, max_year=2022)
        date_dialog.bind(on_save=self.set_birth_date_calendar)
        date_dialog.open()

    def set_birth_date_calendar(self, instance, value, date_range):
        self.ids.birth_date_search.text = str(value)
        self.set_search_birth_date(str(value))


    # serch for pet with the given PET NAME and DATE BIRTH
    def search_name_birth(self):
        self.controller.search_name_birth(self.pet_name, self.birth_date)
    def search_last_appointment_date_vet_name(self):
        self.controller.search_last_appointment_vet_name(self.last_appointment_date, self.vet_name)
    def search_disease_phrase(self):
        self.controller.search_disease_phrase(self.disease)


    # returns the amount of notes that have been found
    # and call the dialog
    def return_searched_amount(self, count):
        self.show_dialog(count)


    # info from checkboxes
    def set_properties(self, instance, value, option1, option2):
        if value == True:
            if option1 == 'disease':
                self.options.append(option1)
            else:
                self.options.append(option1)
                self.options.append(option2)
        else:
            self.options.clear()

    # calls out of .kv to define the search options
    def search(self):
        if len(self.options) == 0:
            self.empty_dialog()
        elif self.options[0] == 'disease' and self.disease != '':
            self.search_disease_phrase()
        elif self.options[0] == 'pet_name' and self.options[1] == 'birth_date' and self.pet_name != '' and self.birth_date != '':
            self.search_name_birth()
        elif self.options[0] == 'vet_name' and self.options[1] == 'last_appointment_date' and self.vet_name != '' and self.last_appointment_date != '':
            self.search_last_appointment_date_vet_name()
        else:
            self.empty_input_dialog()


    # is called to show how many records have been found
    def show_dialog(self, count):
        self.dialog = MDDialog(
            title='Search',
            text=f'Found records: {count}',
            buttons=[
                MDFlatButton(text='Ok', on_release=self.closed)
            ]
        )
        self.dialog.open()


    # is called when the search option has not been configured
    def empty_dialog(self):
        self.dialog = MDDialog(
            title='Warning',
            text='Please choose the search options',
            buttons=[
                MDFlatButton(text='Ok', on_release=self.closed)
            ]
        )
        self.dialog.open()

    # is called when the input data has not been configured
    def empty_input_dialog(self):
        self.dialog = MDDialog(
            title='Warning',
            text= 'Please enter the search data',
            buttons=[
                MDFlatButton(text='Ok', on_release=self.closed)
            ]
        )
        self.dialog.open()

    def wrong_input_dialog(self):
        self.dialog = MDDialog(
            title='Warning',
            text='Please enter the correct data',
            buttons=[
                MDFlatButton(text='Ok', on_release=self.closed)
            ]
        )
        self.dialog.open()

    # is called to close the dialog
    def closed(self, text):
        self.dialog.dismiss()


# popup window to delete info
class DeletePopup(Popup, Widget):
    """
        Is used for delete particular pets records
    """
    def __init__(self, controller, model, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.controller = controller

        self.pet_name = ''
        self.birth_date = ''
        self.last_appointment_date = ''
        self.vet_name = ''
        self.disease = ''

        self.options = []

    # setters for deleted items
    def set_delete_pet_name(self, pet_name):
        self.pet_name = str(pet_name)

    def set_delete_birth_date(self, birth_date):
        self.birth_date = str(birth_date)

    def set_delete_last_appointment_date(self, last_app_date):
        self.last_appointment_date = last_app_date

    def set_delete_vet_name(self, vet_name):
        self.vet_name = vet_name

    def set_delete_disease_phrase(self, phrase):
        self.disease = phrase

    # set last appointment date by calendar widget
    def choose_delete_last_appointment_date(self):
        date_dialog = MDDatePicker(min_year=2000, max_year=2022)
        date_dialog.bind(on_save=self.set_last_appointment_date_calendar)
        date_dialog.open()

    def set_last_appointment_date_calendar(self, instance, value, date_range):
        self.ids.last_appointment_date_delete.text = str(value)
        self.set_delete_last_appointment_date(str(value))

    # set birth date by calendar widget
    def choose_delete_birth_date(self):
        date_dialog = MDDatePicker(min_year=2000, max_year=2022)
        date_dialog.bind(on_save=self.set_birth_date_calendar)
        date_dialog.open()

    def set_birth_date_calendar(self, instance, value, date_range):
        self.ids.birth_date_delete.text = str(value)
        self.set_delete_birth_date(str(value))



    # calls for delete
    def delete_pet_name_birth_date(self):
        self.controller.delete_pet_name_birth_date(self.pet_name, self.birth_date)

    def delete_last_appointment_date_vet_name(self):
        self.controller.delete_last_appointment_date_vet_name(self.last_appointment_date, self.vet_name)

    def delete_disease_phrase(self):
        self.controller.delete_disease_phrase(self.disease)

        # returns the amount of notes that have been found
        # and call the dialog

    def return_deleted_amount(self, count):
        self.show_dialog(count)

        # info from checkboxes

    def set_properties(self, instance, value, option1, option2):
        if value == True:
            if option1 == 'disease':
                self.options.append(option1)
            else:
                self.options.append(option1)
                self.options.append(option2)
        else:
            self.options.clear()

        # calls out of .kv to define the search options

    def delete(self):
        if len(self.options) == 0:
            self.empty_dialog()
        elif self.options[0] == 'disease' and self.disease != '':
            self.delete_disease_phrase()
        elif self.options[0] == 'pet_name' and self.options[
            1] == 'birth_date' and self.pet_name != '' and self.birth_date != '':
            self.delete_pet_name_birth_date()
        elif self.options[0] == 'vet_name' and self.options[
            1] == 'last_appointment_date' and self.vet_name != '' and self.last_appointment_date != '':
            self.delete_last_appointment_date_vet_name()
        else:
            self.empty_input_dialog()

        # is called to show how many records have been found

    def show_dialog(self, count):
        self.dialog = MDDialog(
            title='Search',
            text=f'Deleted records: {count}',
            buttons=[
                MDFlatButton(text='Ok', on_release=self.closed)
            ]
        )
        self.dialog.open()

        # is called when the search option has not been configured

    def empty_dialog(self):
        self.dialog = MDDialog(
            title='Warning',
            text='Please choose the delete options',
            buttons=[
                MDFlatButton(text='Ok', on_release=self.closed)
            ]
        )
        self.dialog.open()

        # is called when the input data has not been configured

    def empty_input_dialog(self):
        self.dialog = MDDialog(
            title='Warning',
            text='Please enter the delete data',
            buttons=[
                MDFlatButton(text='Ok', on_release=self.closed)
            ]
        )
        self.dialog.open()

    def wrong_input_dialog(self):
        self.dialog = MDDialog(
            title='Warning',
            text='Please enter the correct data',
            buttons=[
                MDFlatButton(text='Ok', on_release=self.closed)
            ]
        )
        self.dialog.open()

        # is called to close the dialog

    def closed(self, text):
        self.dialog.dismiss()


class MainScreen(MDScreen):
    """"
    The first (main) window of the program

    """

    # объект контроллера
    controller = ObjectProperty() # специальный подкласс
    # объект модели
    model = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.dialog=None
        #self.ready = False
        #self.dialog = None
        #self.model.add_observer(self)  # register the view as an observer


    def r_m(self):
        return self.model
    def r_c(self):
        return self.controller

    # def set_pet_name(self, name):
    #     self.controller.set_pet_name(name)
    #
    # def set_birth_date(self, birth):
    #     self.controller.set_birth(birth)
    #
    # def set_last_appointment_date(self, app):
    #     self.controller.set_last_appointment_date(app)
    #
    # def set_vet_name(self, name):
    #     self.controller.set_vet_name(name)
    #
    # def set_disease(self, disease):
    #     self.controller.set_disease(disease)
    #
    # # запись данных пациента
    # def record_patient_info(self):
    #     self.controller.record_patient_info()
    #
    # # поиск по имени и дню рождения
    # def search_name_birth(self, pet_name, birth_date):
    #     self.controller.search_name_birth(pet_name, birth_date)
    #
    # #поиск по врачу и последнему посещению
    # def search_last_appointment_vet_name(self, vet_name, last_appointment_date):
    #     self.controller.search_last_appointment_vet_name(vet_name, last_appointment_date)
    #
    # # удалить по имени и дате рождения
    # def delete_pet_name_birth_date(self, pet_name, birth_date):
    #     self.controller.delete_pet_name_birth_date(pet_name, birth_date)
    #
    # # удаление по имени врача и дате последнего приёма
    # def delete_vet_name_last_appointment_date(self, vet_name, last_appointment_date):
    #     self.controller.delete_vet_name_last_appointment_date(vet_name, last_appointment_date)
    #
    # # показ данных о пациентах
    # def info(self):
    #     return self.controller.show_patient_info()
    #
    #
    #
    # # установка даты рождения
    # def choose_birth_date(self):
    #     min_date = datetime.datetime.strptime("2022:02:15", '%Y:%m:%d').date()
    #     max_date = datetime.datetime.strptime("2022:05:30", '%Y:%m:%d').date()
    #     print(min_date)
    #     date_dialog = MDDatePicker(min_year=2010, max_year=2022)
    #     date_dialog.bind(on_save=self.set_birth_date_calendar)
    #     date_dialog.open()
    # def set_birth_date_calendar(self, instance, value, date_range):
    #     date_part=''
    #
    #     for i in value:
    #         if i != '-':
    #             date_part += i
    #         else:
    #             pass
    #
    #
    #     today = datetime.date.today()
    #     print('today = ', today)
    #     if today == str(value):
    #         self.set_birth_date(str(value))
    #         self.ids.birth_date_input.text = str(value)
    #
    #
    # # установка даты последнего посещения
    # def choose_last_appointment_date(self):
    #     date_dialog = MDDatePicker(min_year=2000, max_year=2022)
    #     date_dialog.bind(on_save=self.set_last_appointment_date_calendar)
    #     date_dialog.open()
    #
    # def set_last_appointment_date_calendar(self, instance, value, date_range):
    #     self.ids.last_appointment_date_input.text = str(value)
    #     self.set_last_appointment_date(str(value))
    #
    # def return_birth_date(self):
    #     return self.controller.return_birth_date()
    #
    # def clear_pet_info_input(self):
    #     self.ids.pet_name_input.text = ''
    #     self.ids.birth_date_input.text = ''
    #     self.ids.last_appointment_date_input.text=''
    #     self.ids.vet_name_input.text=''
    #     self.ids.disease_input.text=''
    #
    #
    # # поиск по фразе из диагноза
    # def search_disease(self, world):
    #     self.controller.find_disease(world)
    #
    # def show_dialog(self):
    #
    #     self.dialog = MDDialog(
    #         title = 'Добавление',
    #         text = 'Запись зарегистрирована',
    #         #size_hint=(0.5,0.5),
    #         buttons =[
    #             MDFlatButton(text='Ok', on_release=self.closed)
    #         ]
    #     )
    #     self.dialog.open()
    #     #self.clear_pet_info_input()
    #
    # def show_no_dialog(self):
    #
    #     self.dialog = MDDialog(
    #         title = 'xy',
    #         text = 'Все поля должны быть заполнены',
    #         #size_hint=(0.5,0.5),
    #         buttons =[
    #             MDFlatButton(text='Ok', on_release=self.closed)
    #         ]
    #     )
    #     self.dialog.open()
    #
    # def closed(self, text):
    #     self.dialog.dismiss()
    #
    # def everything_is_ready(self, rez):
    #     self.ready = rez
    #
    # def ever(self):
    #     return self.ready
    #
    #
    # def model_is_changed(self):
    #     """
    #     The method is called when the model changes.
    #     Requests and displays the value of the sum.
    #     """
    #
    #     self.ids.result.text = str(self.model.full_name)


Builder.load_file(os.path.join(os.path.dirname(__file__), "myscreen.kv"))
