import os
import webbrowser

from kivy.lang import Builder
from kivy.properties import ObjectProperty

from kivymd.uix.screen import MDScreen
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.tooltip import MDTooltip
from kivymd.uix.button import MDFlatButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.dropdownitem import MDDropDownItem

from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.uix.checkbox import CheckBox




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

    def return_model(self):
        return self.model
    def return_controller(self):
        return self.controller
    def get_values(self):
        values = ['Кот', 'Собака', 'Питон','Хорёк', 'Енот','Морская\n свинка']
        print(self.ids.click_label.text)
        return values

    @property
    def ready(self):
        return self._ready
    @ready.setter
    def ready(self, ready):
        self._ready = ready


    def set_pet_name(self, name):
        self.controller.set_pet_name(name)


    def set_pet_type(self, value):
        #self.ids.click_label.text = f'You Selected:{value}'
        self.ids.spinner_id.text = f'{value}'
        self.controller.set_pet_type(value)

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


    # is called when the pet info registration has been successfully done
    def start_handler_info(self):
        Factory.HandlerPopup(controller = self.return_controller(), model = self.return_model(), add_popup = self).open()

    # is called when the pet information is successfully added
    def show_dialog(self):
        self.dialog = MDDialog(
            title='Registration',
            text='The record has been added!',
            buttons=[
                MDFlatButton(text='Ok', on_release=self.closed)
            ]
        )
        self.dialog.open()


    # is called when there is wrong pet information
    def show_no_dialog(self):
        self.dialog = MDDialog(
            title='Warning',
            text='Please correct the input data',
            # size_hint=(0.5,0.5),
            buttons=[
                MDFlatButton(text='Ok', on_release=self.no_closed)
            ]
        )
        self.dialog.open()

   # is called when the pet indo is correct
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
        o = FoundPopup(controller = self, model = self.model)
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
        self.dialog = None

        self.pet_name = ''
        self.birth_date = ''
        self.last_appointment_date = ''
        self.vet_name = ''
        self.disease = ''
        self.letter = None

        self.first = ''
        self.second=''

        self._check_option = 0

        self.options = []
        self.deleted_items_mail = []

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
        if count == 0:
            self.show_none_dialog()
        else:
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

    @property
    def check_option(self):
        return self._check_option
    @check_option.setter
    def check_option(self, option):
        self._check_option = option

    # calls out of .kv to define the search options
    def delete(self):
        if len(self.options) == 0:
            self.empty_dialog()
        elif self.options[0] == 'disease' and self.disease != '':
            self._check_option = 3
            self.first = self.disease
            self.delete_disease_phrase()
            #self.letter = EmailLetterPopup(model=self.model, option=3, arg1=self.disease, arg2='', deleted_items=self.deleted_items).open()

        elif self.options[0] == 'pet_name' and self.options[
            1] == 'birth_date' and self.pet_name != '' and self.birth_date != '':
            self._check_option = 1
            self.first = self.pet_name
            self.second = self.birth_date
            self.delete_pet_name_birth_date()
            #self.letter = EmailLetterPopup(model=self.model, option=2, arg1=self.pet_name, arg2=self.birth_date, deleted_items=self.deleted_items).open()

        elif self.options[0] == 'vet_name' and self.options[
            1] == 'last_appointment_date' and self.vet_name != '' and self.last_appointment_date != '':
            self._check_option = 2
            self.first = self.vet_name
            self.second = self.last_appointment_date
            self.delete_last_appointment_date_vet_name()
            #self.letter = EmailLetterPopup(model=self.model, option=1, arg1=self.vet_name,arg2=self.last_appointment_date, deleted_items=self.deleted_items).open()

        else:
            self.empty_input_dialog()

    # is called to show how many records have been found
    def show_dialog(self, count):
        self.dialog = MDDialog(
            title='Delete',
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
                MDFlatButton(text='Ok', on_release=self.closed_empty)
            ]
        )
        self.dialog.open()

    # is called if no info have been found
    def show_none_dialog(self):
        self.dialog = MDDialog(
            title='Delete',
            text='No records have been found',
            buttons=[
                MDFlatButton(text='Ok', on_release=self.closed_empty)
            ]
        )
        self.dialog.open()

        # is called when the input data has not been configured

    def empty_input_dialog(self):
        self.dialog = MDDialog(
            title='Warning',
            text='Please enter the delete data',
            buttons=[
                MDFlatButton(text='Ok', on_release=self.closed_empty)
            ]
        )
        self.dialog.open()

    def wrong_input_dialog(self):
        self.dialog = MDDialog(
            title='Warning',
            text='Please enter the correct data',
            buttons=[
                MDFlatButton(text='Ok', on_release=self.closed_empty)
            ]
        )
        self.dialog.open()

    def set_deleted_items_mail(self, deleted_items_mail):
        self.deleted_items_mail = deleted_items_mail

    # is called to close the dialog
    def closed(self, text):
        self.dialog.dismiss()
        self.letter = EmailLetterPopup(model = self.model, option=1, arg1=self.first, arg2=self.second, deleted_items_mail=self.deleted_items_mail).open()


        #self.letter = Factory.EmailLetterPopup().open()

    # for dialogs with empty input error
    def closed_empty(self, text):
        self.options = []
        self.dialog.dismiss()



class EmailLetterPopup(Popup):
    def __init__(self, model, option, arg1, arg2, deleted_items_mail, **kwargs):
        super().__init__(**kwargs)
        self.all_pet_info = []
        self.option = option
        self.model = model
        self.all_pet_info = self.model.return_all_info_list()
        self.first_point = arg1
        self.second_point = arg2
        self.deleted_items_mail = deleted_items_mail
        if len(self.deleted_items_mail) == 1:
            self.ids.deleted_item_mail.text = deleted_items_mail[0]

        self.handler_name = ''
        self.mail = ''
        #self.find_pet_handler_info(deleted_items)

    def open_mail(self):
        print('mail letter ',self.deleted_items_mail)
        # open default browser
        webbrowser.open_new('https://e.mail.ru/drafts/')
        # open certain browser
        #webbrowser.get("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe %s").open_new('https://e.mail.ru/inbox/')


    # set contact pet handler info
    def find_pet_handler_info(self, deleted_items):
        print(deleted_items)
        for item in deleted_items:
            print(item)
            if self.option == 1:
                if item['pet_name'].lower() == self.first_point.lower() and item['birth_date'] == self.second_point:
                    self.handler_name = item['handler_name']
                    self.mail = item['mail']
            elif self.option == 2:
                if item['vet_name'].lower() == self.first_point.lower() and item['last_appointment_date'] == self.second_point:
                    self.handler_name = item['handler_name']
                    self.mail = item['mail']
            elif self.option == 3:
                print('point ', self.first_point)
                print(item['disease'])
                if (item['disease'].lower()).find(self.first_point.lower()) != -1:
                    self.handler_name = item['handler_name']
                    self.mail = item['mail']
                    print('item ', self.mail)
        print(self.mail)
        self.ids.mail_to_death.text = self.mail


class DropDownItem(MDDropDownItem):
    pass

# popup window with found by search info
class FoundPopup(Popup, Widget):
    def __init__(self,controller,model, **kwargs):
        self.model=model
        #self._found_list
        super().__init__(**kwargs)
        self.table = MDDataTable(pos_hint={'center_y': 0.58, 'center_x': 0.5},
                                 use_pagination=True,
                                 column_data=[
                                     ("Имя питомца", dp(40)),
                                     ("Вид животного", dp(30)),
                                     ("Дата рождения", dp(30)),
                                     ("Дата последнего приема", dp(30)),
                                     ("ФИО ветеринара", dp(30)),
                                     ("Диагноз", dp(30))], size_hint=(1, 0.7),row_data=self.add_info())
        self.add_widget(self.table)
    def add_info(self):
        return self.model._found_list

# popup window about pet handler information that is appeared after AddPopup window
class HandlerPopup(Popup):
    """
    Is used to set up pet handler information
    """

    model = ObjectProperty()
    controller = ObjectProperty()

    def __init__(self,controller, model, add_popup, **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.controller = controller
        self.add_popup = add_popup

    # set pet handler info
    def set_handler_name(self, handler):
        self.controller.set_handler_name(handler)
    def set_phone_number(self, phone):
        self.controller.set_phone_number(phone)
    def set_mail(self, mail):
        self.controller.set_mail(mail)
    def set_address(self, address):
        self.controller.set_address(address)

    def record_handler_info(self):
        self.controller.record_handler_info()



# popup window for single pet information that is appeared when you click on CHECK in main screen table
class InformationPopup(Popup):
    """
    Is used to show more detailed pet info
    """
    def __init__(self, pet_info, main, **kwargs):
        super().__init__(**kwargs)
        self.pet_info = pet_info
        self.main = main
        self._all_info_list = main.return_all_info_list()


        self.pet_name = pet_info[0]
        self.pet_type = pet_info[1]
        self.birth_date = pet_info[2]
        self.last_appointment_date = pet_info[3]
        self.vet_name = pet_info[4]
        self.disease = pet_info[5]

        for item in self._all_info_list:
            if item['pet_name'] == self.pet_name:
                self.ids.handler_name.text = item['handler_name']
                self.ids.phone_number.text = item['phone_number']
                self.ids.mail.text = item['mail']
                self.ids.handler_address.text = item['handler_address']


        self.ids.pet_name.text = self.pet_name
        self.ids.pet_type.text = self.pet_type
        # self.ids.birth_date.text = self.birth_date
        # self.ids.last_appointment_date.text = self.last_appointment_date
        # self.ids.vet_name.text = self.vet_name
        self.ids.disease.text = self.disease


    # is called to close the InformationPopup
    # and make CHECK in the main screen table down again
    def close_pet_info_window(self):
        self.dismiss()
        self.main.close_pet_info_window()


# popup window that shows the amount of broken records if they exist
class WarningPopup(Popup, Widget):
    """
    Is used for showing the amount of broken records if they exist
    """
    def __init__(self, main, bad_files_count, bad_line_name, bad_line_count, **kwargs):
        super().__init__(**kwargs)
        self.main = main

        self.ids.files_count.text = bad_files_count
        self.ids.line_name.text = bad_line_name
        self.ids.line_count.text = bad_line_count

    def dismiss(self):
        self.main.dismiss_warning()

class HelperPopup(Popup):
    pass


# tooltips
class TooltipCheckBox(CheckBox, MDTooltip):
    pass
class TooltipButton(Button, MDTooltip):
    pass



# main view
class MainScreen(MDScreen):
    """"
    The first (main) window of the program
    """


    controller = ObjectProperty()
    model = ObjectProperty()

    def __init__(self,model,controller, **kw):
        super().__init__(**kw)
        self.dialog=None

        self.controller = controller
        self.model = model

        self._pets_list=self.model.return_pets_list()
        self._all_info_list = self.model.return_all_info_list()

        self.current_pet_info = []

        # the table on the main screen
        self.table = MDDataTable(pos_hint={'center_y': 0.58, 'center_x': 0.5},
                                 use_pagination=True,
                                 check = True,
                                 column_data=[
                                     ("Имя питомца", dp(40)),
                                     ("Вид животного", dp(30)),
                                     ("Дата рождения", dp(30)),
                                     ("Дата последнего приема", dp(30)),
                                     ("ФИО ветеринара", dp(30)),
                                     ("Диагноз", dp(30))], size_hint=(1, 0.7),
                                 row_data=self.add_table_data())
        #self.table.bind(on_row_press=self.pet_info_window)
        self.table.bind(on_check_press=self.check_info)
        self.add_widget(self.table)

        # the warning window about broken records in xml file
        # is shown ONLY if they exist
        self.bad_files_count =str(self.model.return_bad_files_count())

        self.bad_line_name = '<' +  self.model.return_bad_line_name() + '>'
        self.bad_line_count = str(self.model.return_bad_line_count())
        if int(self.bad_files_count) != 0:
            self.w = WarningPopup(main = self, bad_files_count=self.bad_files_count, bad_line_name = self.bad_line_name,bad_line_count = self.bad_line_count)
            self.add_widget(self.w)



    def dismiss_warning(self):
        self.remove_widget(self.w)

    # is called in ToolBar
    #  and shows the menu buttons
    def show_menu(self):
        pass


    def return_all_info_list(self):
        return self._all_info_list

    # popup window with more detailed pet info
    # is appeared when you click on CHECK in the main screen table
    def check_info(self, instance, pet_info):
        InformationPopup(pet_info, main=self).open()


    # is called from InformationPopup when it is dismissed
    def close_pet_info_window(self):
        self.remove_widget(self.table)
        self.add_into_main_table(self._pets_list)


    # is called to add patients info into the table
    def add_table_data(self):
        table_pets_list=[]
        for item in self._pets_list:
            pet_list = []
            pet_list.append(item['pet_name'])
            pet_list.append(item['pet_type'])
            pet_list.append(item['birth_date'])
            pet_list.append(item['last_appointment_date'])
            pet_list.append(item['vet_name'])
            pet_list.append(item['disease'])
            table_pets_list.append(pet_list)

        return table_pets_list

    # new table is appeared after deleting the pet element
    def delete_from_main_table(self, pet):
        self.remove_widget(self.table)
        self.table = MDDataTable(pos_hint={'center_y': 0.58, 'center_x': 0.5},
                                 use_pagination=True,
                                 check = True,
                                 column_data=[
                                     ("Имя питомца", dp(30)),
                                     ("Вид животного", dp(30)),
                                     ("Дата рождения", dp(30)),
                                     ("Дата последнего приема", dp(30)),
                                     ("ФИО ветеринара", dp(30)),
                                     ("Диагноз", dp(30))], size_hint=(1, 0.7),
                                 row_data=self.add_table_data_deleted(pet))
        self.table.bind(on_check_press=self.check_info)
        self.add_widget(self.table)

    # is called in delete_from_main_table(pet) to delete pet element info from main screen data table
    def add_table_data_deleted(self, pets):
        table_pets_list = []
        for item in pets:
            pet_list = []
            pet_list.append(item['pet_name'])
            pet_list.append(item['pet_type'])
            pet_list.append(item['birth_date'])
            pet_list.append(item['last_appointment_date'])
            pet_list.append(item['vet_name'])
            pet_list.append(item['disease'])
            table_pets_list.append(pet_list)

        return table_pets_list

    # new table is appeared after adding a new pet element
    def add_into_main_table(self, pets_list):
        self.remove_widget(self.table)
        self.table = MDDataTable(pos_hint={'center_y': 0.58, 'center_x': 0.5},
                                 use_pagination=True,
                                 check = True,
                                 column_data=[
                                     ("Имя питомца", dp(30)),
                                     ("Вид животного", dp(30)),
                                     ("Дата рождения", dp(30)),
                                     ("Дата последнего приема", dp(30)),
                                     ("ФИО ветеринара", dp(30)),
                                     ("Диагноз", dp(30))], size_hint=(1, 0.7),
                                 row_data=self.add_table_data_added(pets_list))

        self.table.bind(on_check_press=self.check_info)
        self.add_widget(self.table)

    # is called in add_into_main_table() to upload a new pet list into main screen table
    def add_table_data_added(self, pets_list):
        table_pets_list = []
        self._pets_list = pets_list
        for item in pets_list:
            pet_list = []
            pet_list.append(item['pet_name'])
            pet_list.append(item['pet_type'])
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