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
from kivy.metrics import dp
#from Kivy_MVC_Template.Utility.observer import Observer

from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivy.uix.gridlayout import GridLayout
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

    def clear_all(self):
        self.ids.pet_name_input.text ='мм '
        self.ids.birth_date_input.text = ' '


# popup window to search info
class SearchPopup(Popup, Widget):
    """
    Is used for search for particular pets records
    """
    # model = ObjectProperty()
    # controller = ObjectProperty()
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
                MDFlatButton(text='Ok', on_release=self.closed_yes)
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
    def closed_yes(self, text):
        self.dialog.dismiss()
        o = FoundPopup()
        o.open()

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


class FoundPopup(Popup, Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table = MDDataTable(pos_hint={'center_y': 0.58, 'center_x': 0.5},
                                 use_pagination=True,
                                 column_data=[
                                     ("Имя питомца", dp(30)),
                                     ("Дата рождения", dp(30)),
                                     ("Дата последнего приема", dp(30)),
                                     ("ФИО ветеринара", dp(30)),
                                     ("Диагноз", dp(30))], size_hint=(1, 0.7))
        self.add_widget(self.table)


class MainScreen(MDScreen):
    """"
    The first (main) window of the program

    """

    controller = ObjectProperty()
    model = ObjectProperty()

    def __init__(self,model,controller,**kw):
        super().__init__(**kw)
        self.dialog=None

        self.controller = controller
        self.model = model
        self._pets_list=self.model.return_pets_list()

        # the table on the main screen
        self.table = MDDataTable(pos_hint={'center_y': 0.58, 'center_x': 0.5},
                                 use_pagination=True,
                                 column_data=[
                                     ("Имя питомца", dp(30)),
                                     ("Дата рождения", dp(30)),
                                     ("Дата последнего приема", dp(30)),
                                     ("ФИО ветеринара", dp(30)),
                                     ("Диагноз", dp(30))], size_hint=(1, 0.7),
                                 row_data=self.add_table_data())
        self.add_widget(self.table)


    # is called to add patients info into the table
    def add_table_data(self):
        table_pets_list=[]
        for item in self._pets_list:
            pet_list = []
            pet_list.append(item['pet_name'])
            pet_list.append(item['birth_date'])
            pet_list.append(item['last_appointment_date'])
            pet_list.append(item['vet_name'])
            pet_list.append(item['disease'])
            table_pets_list.append(pet_list)

        return table_pets_list

    # are called when the popup windows are initialized
    def return_model(self):
        return self.model
    def return_controller(self):
        return self.controller



Builder.load_file(os.path.join(os.path.dirname(__file__), "myscreen.kv"))
