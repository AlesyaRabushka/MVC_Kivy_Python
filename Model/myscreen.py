# The model implements the observer pattern. This means that the class must
# support adding, removing, and alerting observers. In this case, the model is
# completely independent of controllers and views. It is important that all
# registered observers implement a specific method that will be called by the
# model when they are notified (in this case, it is the `model_is_changed`
# method). For this, observers must be descendants of an abstract class,
# inheriting which, the `model_is_changed` method must be overridden.

import datetime
import xml.dom.minidom as md
import xml.sax as sax

from os import path

from Model.sax_parser import PetElement
from View.myscreen import MainScreen, AddPopup, SearchPopup, DeletePopup

from View.myscreen import WarningPopup


class Model:


    def __init__(self, controller):
        self._pet_name = ''
        self._pet_type = ''
        self._birth = ''
        self._last_appointment_date = ''
        self._vet_name =''
        self._disease=''
        self.val = ''
        self.controller = controller

        # список всех пациентов
        self._pets_list = []
        self._handlers_list = []
        self._all_info_list = []
        self._found_list = []
        # reading info from the file with the start of the program
        self.bad_files_count = 0
        self.bad_line_name = ''
        self.bad_line_count = 0
        self.set_previous_patient_info()

        # self.main_view = MainScreen(model = self, controller = self.controller)
        #
        # self.view = AddPopup(controller = self.controller, model = self)
        # self.search_view = SearchPopup(self.controller, self.main_view.return_model())
        # self.delete_view = DeletePopup(self.main_view.return_controller(), self.main_view.return_model())

        # pet handler info
        self._handler_name = ''
        self._phone_number = ''
        self._mail = ''
        self._address = ''






    def return_found_list(self):
        return self._found_list
    def return_pets_list(self):
        return self._pets_list
    def return_all_info_list(self):
        return self._all_info_list

    # set pet info
    @property
    def pet_name(self):
        return self._pet_name
    @property
    def pet_type(self):
        return self._pet_type
    @property
    def birth(self):
        return self._birth
    @property
    def last_appointment_date(self):
        return self._last_appointment_date
    @property
    def vet_name(self):
        return self._vet_name
    @property
    def disease(self):
        return self._disease

    @pet_name.setter
    def pet_name(self, name):
        self._pet_name = name
    @pet_type.setter
    def pet_type(self, type):
        self._pet_type = type
    @birth.setter
    def birth(self, birth):
        self._birth = birth
    @last_appointment_date.setter
    def last_appointment_date(self, app):
        self._last_appointment_date = app
    @vet_name.setter
    def vet_name(self, name):
        self._vet_name = name
    @disease.setter
    def disease(self, disease):
        self._disease = disease


    # pet pet handler info
    @property
    def handler_name(self):
        return self._handler_name
    @handler_name.setter
    def handler_name(self, handler):
        self._handler_name = handler
    @property
    def phone_number(self):
        return self._phone_number
    @phone_number.setter
    def phone_number(self, number):
        self._phone_number = number
    @property
    def mail(self):
        return self._mail
    @mail.setter
    def mail(self, mail):
        self._mail = mail
    @property
    def address(self):
        return self._address
    @address.setter
    def address(self, address):
        self._address = address


    # adds all pet info to the other ones
    def add_info(self):
        self._patients = {}
        self.pet={}
        self.handler={}
        # set all info
        self._patients['pet_name'] = self._pet_name
        self._patients['pet_type'] = self._pet_type
        self._patients['birth_date'] = self._birth
        self._patients['last_appointment_date'] = self._last_appointment_date
        self._patients['vet_name'] = self._vet_name
        self._patients['disease'] = self._disease
        self._patients['handler_name'] = self._handler_name
        self._patients['phone_number'] = self._phone_number
        self._patients['mail'] = self._mail
        self._patients['handler_address'] = self._address

        # set only pet info
        self.pet['pet_name'] = self._pet_name
        self.pet['pet_type'] = self._pet_type
        self.pet['birth_date'] = self._birth
        self.pet['last_appointment_date'] = self._last_appointment_date
        self.pet['vet_name'] = self._vet_name
        self.pet['disease'] = self._disease

        # set only handler info
        self.handler['handler_name'] = self._handler_name
        self.handler['phone_number'] = self._phone_number
        self.handler['mail'] = self._mail
        self.handler['handler_address'] = self._address


        self._all_info_list.append(self._patients)
        self._pets_list.append(self.pet)
        self._handlers_list.append(self.handler)




        self._pet_name=''
        self._pet_type = ''
        self._birth=''
        self._vet_name=''
        self._last_appointment_date=''
        self._disease=''
        self._handler_name = ''
        self._phone_number = ''
        self._mail = ''
        self._address = ''

    def record_handler_info(self):
        self.record_all_info()



    def record_patient_info(self):
        # self._patients = {}
        # self._patients['pet_name'] = self._pet_name
        # self._patients['birth_date'] = self._birth
        # self._patients['last_appointment_date'] = self._last_appointment_date
        # self._patients['vet_name'] = self._vet_name
        # self._patients['disease'] = self._disease
        # self._patients['handler_name'] = self._handler_name
        # self._patients['phone_number'] = self._phone_number
        # self._patients['mail'] = self._mail
        # self._patients['address'] = self._address
        #
        # self._pets_list.append(self._patients)
        pass

    # adds ALL info into the file
    def record_all_info(self):
        # if the file exists
        if path.exists('pet.xml'):
            self.set_previous_patient_info()
            self.add_info()
        # if not
        else:
            self.add_info()


        self.add_into_main_table(self._pets_list)




        # is called to record pets info into the file
        doc = md.Document()
        list = doc.createElement('pets_list')
        doc.appendChild(list)

        for item in self._all_info_list:
            pet = doc.createElement('pet')

            pet_name = doc.createElement('pet_name')
            pet_name.appendChild(doc.createTextNode(item['pet_name']))

            pet_type = doc.createElement('pet_type')
            pet_type.appendChild(doc.createTextNode(item['pet_type']))

            birth_date = doc.createElement('birth_date')
            birth_date.appendChild(doc.createTextNode(str(item['birth_date'])))

            last_appointment = doc.createElement('last_appointment_date')
            last_appointment.appendChild(doc.createTextNode(str(item['last_appointment_date'])))

            vet_name = doc.createElement('vet_name')
            vet_name.appendChild(doc.createTextNode(item['vet_name']))

            disease = doc.createElement('disease')
            disease.appendChild(doc.createTextNode(item['disease']))

            handler = doc.createElement('handler_name')
            handler.appendChild(doc.createTextNode(item['handler_name']))

            phone = doc.createElement('phone_number')
            phone.appendChild(doc.createTextNode(item['phone_number']))

            mail = doc.createElement('mail')
            mail.appendChild(doc.createTextNode(item['mail']))

            address = doc.createElement('handler_address')
            address.appendChild(doc.createTextNode(item['handler_address']))

            pet.appendChild(pet_name)
            pet.appendChild(pet_type)
            pet.appendChild(birth_date)
            pet.appendChild(last_appointment)
            pet.appendChild(vet_name)
            pet.appendChild(disease)
            pet.appendChild(handler)
            pet.appendChild(phone)
            pet.appendChild(mail)
            pet.appendChild(address)

            list.appendChild(pet)

        file = open('pet.xml', 'w')
        doc.writexml(file, encoding='windows-1251')
        file.close()

    # updates info in the file after deleting the record/s
    def upload_patient_info(self):
        doc = md.Document()
        list = doc.createElement('pets_list')
        doc.appendChild(list)

        for item in self._all_info_list:
            pet = doc.createElement('pet')

            pet_name = doc.createElement('pet_name')
            pet_name.appendChild(doc.createTextNode(item['pet_name']))

            pet_type = doc.createElement('pet_type')
            pet_type.appendChild(doc.createTextNode(item['pet_type']))

            birth_date = doc.createElement('birth_date')
            birth_date.appendChild(doc.createTextNode(str(item['birth_date'])))

            last_appointment = doc.createElement('last_appointment_date')
            last_appointment.appendChild(doc.createTextNode(str(item['last_appointment_date'])))

            vet_name = doc.createElement('vet_name')
            vet_name.appendChild(doc.createTextNode(item['vet_name']))

            disease = doc.createElement('disease')
            disease.appendChild(doc.createTextNode(item['disease']))

            handler = doc.createElement('handler_name')
            handler.appendChild(doc.createTextNode(item['handler_name']))

            phone = doc.createElement('phone_number')
            phone.appendChild(doc.createTextNode(item['phone_number']))

            mail = doc.createElement('mail')
            mail.appendChild(doc.createTextNode(item['mail']))

            address = doc.createElement('handler_address')
            address.appendChild(doc.createTextNode(item['handler_address']))

            pet.appendChild(pet_name)
            pet.appendChild(pet_type)
            pet.appendChild(birth_date)
            pet.appendChild(last_appointment)
            pet.appendChild(vet_name)
            pet.appendChild(disease)
            pet.appendChild(handler)
            pet.appendChild(phone)
            pet.appendChild(mail)
            pet.appendChild(address)

            list.appendChild(pet)

        file = open('pet.xml', 'w')
        doc.writexml(file, encoding='windows-1251')
        file.close()

    # updates info in tne main screen table after
    def add_into_main_table(self, pets_list):
        self.controller.main_view.add_into_main_table(pets_list)

    # takes info from the file by PARSER
    def set_previous_patient_info(self):
        parser = sax.make_parser()  # creating an XMLReader
        parser.setFeature(sax.handler.feature_namespaces, 0)  # turning off namespaces

        handler = PetElement()
        parser.setContentHandler(handler)  # overriding default ContextHandler
        parser.parse('pet.xml')

        self._pets_list = handler.return_pets_list()
        self._all_info_list = handler.return_all_list()
        self.bad_files_count = handler.return_bad_files_count()
        self.bad_line_name = handler.return_bad_line_name()
        self.bad_line_count = handler.return_bad_line_count()

    #def return_previous_patient_info


    def return_bad_files_count(self):
        return self.bad_files_count
    def return_bad_line_name(self):
        return self.bad_line_name
    def return_bad_line_count(self):
        return self.bad_line_count




    # search for particular records by the given pet name and birth date
    def search_name_birth(self, pet_name, birth_date):
        amount_of_found_items = 0
        self._found_list = []
        for item in self._pets_list:
            info_list = []
            if item['pet_name'].lower() == pet_name.lower() and item['birth_date'] == birth_date:
                amount_of_found_items += 1
                info_list.append(item['pet_name'])
                info_list.append(item['pet_type'])
                info_list.append(item['birth_date'])
                info_list.append(item['last_appointment_date'])
                info_list.append(item['vet_name'])
                info_list.append(item['disease'])
                self._found_list.append(info_list)
        #self.return_searched_info(self._found_list)
        self.return_searched_amount(amount_of_found_items)

    # search for particular records by the given vet name and last appointment date
    def search_last_appointment_vet_name(self, last_appointment_date, vet_name):
        amount_of_found_items = 0
        self._found_list = []
        for item in self._pets_list:
            info_list = []
            if item['vet_name'].lower() == vet_name.lower() and item['last_appointment_date'] == last_appointment_date:
                amount_of_found_items += 1
                info_list.append(item['pet_name'])
                info_list.append(item['pet_type'])
                info_list.append(item['birth_date'])
                info_list.append(item['last_appointment_date'])
                info_list.append(item['vet_name'])
                info_list.append(item['disease'])
                self._found_list.append(info_list)
        #self.return_searched_info(self._found_list)
        self.controller.search_view.return_searched_amount(amount_of_found_items)

    # search for particular records by the given disease phrase
    def search_disease_phrase(self, world):
        amount_of_found_items = 0
        self._found_list = []
        for item in self._pets_list:
            info_list = []
            if (item['disease'].lower()).find(world.lower()) != -1:
                amount_of_found_items += 1
                info_list.append(item['pet_name'])
                info_list.append(item['pet_type'])
                info_list.append(item['birth_date'])
                info_list.append(item['last_appointment_date'])
                info_list.append(item['vet_name'])
                info_list.append(item['disease'])
                self._found_list.append(info_list)
        #self.return_searched_info(self._found_list)
        self.return_searched_amount(amount_of_found_items)

    # returns the amount of found pet records
    def return_searched_info(self,found):
        return self._found_list
    def return_searched_amount(self, count):
        self.controller.search_view.return_searched_amount(count)


    # delete particular records by the given parameters of pet name and birth date
    def delete_pet_name_birth_date(self, pet_name, birth_date):
        amount_of_deleted_items = 0
        for item in self._pets_list:
            if item['pet_name'].lower() == pet_name.lower() and item['birth_date'] == birth_date:
                amount_of_deleted_items += 1
                self._pets_list.remove(item)
                # looking for this item in the main list
                for bigger_item in self._all_info_list:
                    if bigger_item['pet_name'].lower() == pet_name.lower() and bigger_item['birth_date'] == birth_date:
                        self._all_info_list.remove(bigger_item)


        self.upload_patient_info()
        self.return_deleted_amount(amount_of_deleted_items)
        self.delete_from_main_table(self._pets_list)

    # delete particular records by given parameters of vet name and last appointment date
    def delete_last_appointment_date_vet_name(self, last_appointment_date, vet_name):
        amount_of_deleted_items = 0
        for item in self._pets_list:
            if item['vet_name'].lower() == vet_name.lower() and item['last_appointment_date'] == last_appointment_date:
                amount_of_deleted_items += 1
                self._pets_list.remove(item)
                # looking for this item in the main list
                for bigger_item in self._all_info_list:
                    if bigger_item['vet_name'].lower() == vet_name.lower() and bigger_item['last_appointment_date'] == last_appointment_date:
                        self._all_info_list.remove(bigger_item)

        self.upload_patient_info()
        self.return_deleted_amount(amount_of_deleted_items)
        self.delete_from_main_table(self._pets_list)

    # delete the particular records by the given disease phrase
    def delete_disease_phrase(self, phrase):
        amount_of_deleted_items = 0
        self.deleted_items_mail=[]
        for item in self._pets_list:
            if (item['disease'].lower()).find(phrase.lower()) != -1:
                amount_of_deleted_items += 1
                self._pets_list.remove(item)
                # looking for this item in the main list
                for bigger_item in self._all_info_list:
                    if (bigger_item['disease'].lower()).find(phrase.lower()) != -1:
                        self.deleted_items_mail.append(bigger_item['mail'])
                        self._all_info_list.remove(bigger_item)
            else:
                pass

        self.upload_patient_info()
        self.return_deleted_amount(amount_of_deleted_items)
        self.controller.delete_view.set_deleted_items_mail(self.deleted_items_mail)
        self.delete_from_main_table(self._pets_list)

    # delete the particular pet element from main screen data table
    def delete_from_main_table(self, deleted_list):
        self.controller.main_view.delete_from_main_table(deleted_list)

    # returns the amount of deleted records
    def return_deleted_amount(self, amount):
        self.controller.delete_view.return_deleted_amount(amount)
