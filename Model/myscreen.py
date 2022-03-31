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

from kivy.properties import ObjectProperty

from kivymd.uix.picker import MDDatePicker

from View.myscreen import MainScreen, AddPopup, SearchPopup, DeletePopup


class Model:


    def __init__(self, controller):
        self._pet_name = ''
        self._birth = ''
        self._last_appointment_date = ''
        self._vet_name =''
        self._disease=''
        self.val = ''
        self.controller = controller

        # список всех пациентов
        self._pets_list = []

        # reading info from the file with the start of the program
        self.set_previous_patient_info()
        self.main_view = MainScreen(model = self, controller = self.controller)
        self.view = AddPopup(self.main_view.return_controller(), self.main_view.return_model())
        self.search_view = SearchPopup(self.controller, self.main_view.return_model())
        self.delete_view = DeletePopup(self.main_view.return_controller(), self.main_view.return_model())


        # список классов наблюдателя
        self._observers = []




    def return_pets_list(self):
        return self._pets_list


    @property
    def pet_name(self):
        return self._pet_name

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

    # adds pet record to the other ones
    def add_info(self):
        self._patients = {}
        self._patients['pet_name'] = self._pet_name
        self._patients['birth_date'] = self._birth
        self._patients['last_appointment_date'] = self._last_appointment_date
        self._patients['vet_name'] = self._vet_name
        self._patients['disease'] = self._disease

        self._pets_list.append(self._patients)

        self._pet_name=''
        self._birth=''
        self._vet_name=''
        self._last_appointment_date=''
        self._disease=''

    # adds info into the file
    def record_patient_info(self):
        # if the file exists
        if path.exists('pet.xml'):
            self.set_previous_patient_info()
            self.add_info()
        # if not
        else:
            self.add_info()


        # добавляю записи в файлик
        doc = md.Document()
        list = doc.createElement('pets_list')
        doc.appendChild(list)

        for item in self._pets_list:
            pet = doc.createElement('pet')

            pet_name = doc.createElement('pet_name')
            pet_name.appendChild(doc.createTextNode(item['pet_name']))

            birth_date = doc.createElement('birth_date')
            birth_date.appendChild(doc.createTextNode(str(item['birth_date'])))

            last_appointment = doc.createElement('last_appointment_date')
            last_appointment.appendChild(doc.createTextNode(str(item['last_appointment_date'])))

            vet_name = doc.createElement('vet_name')
            vet_name.appendChild(doc.createTextNode(item['vet_name']))

            disease = doc.createElement('disease')
            disease.appendChild(doc.createTextNode(item['disease']))

            pet.appendChild(pet_name)
            pet.appendChild(birth_date)
            pet.appendChild(last_appointment)
            pet.appendChild(vet_name)
            pet.appendChild(disease)

            list.appendChild(pet)

        file = open('pet.xml', 'w')
        doc.writexml(file, encoding='windows-1251')
        file.close()

    # updates info in the file after deleting the record/s
    def upload_patient_info(self):
        doc = md.Document()
        list = doc.createElement('pets_list')
        doc.appendChild(list)

        for item in self._pets_list:
            pet = doc.createElement('pet')

            pet_name = doc.createElement('pet_name')
            pet_name.appendChild(doc.createTextNode(item['pet_name']))

            birth_date = doc.createElement('birth_date')
            birth_date.appendChild(doc.createTextNode(str(item['birth_date'])))

            last_appointment = doc.createElement('last_appointment_date')
            last_appointment.appendChild(doc.createTextNode(str(item['last_appointment_date'])))

            vet_name = doc.createElement('vet_name')
            vet_name.appendChild(doc.createTextNode(item['vet_name']))

            disease = doc.createElement('disease')
            disease.appendChild(doc.createTextNode(item['disease']))

            pet.appendChild(pet_name)
            pet.appendChild(birth_date)
            pet.appendChild(last_appointment)
            pet.appendChild(vet_name)
            pet.appendChild(disease)

            list.appendChild(pet)

        file = open('pet.xml', 'w')
        doc.writexml(file, encoding='windows-1251')
        file.close()

    # takes info from the file
    def set_previous_patient_info(self):
        parser = sax.make_parser()  # creating an XMLReader
        parser.setFeature(sax.handler.feature_namespaces, 0)  # turning off namespaces
        handler = PetElement()
        parser.setContentHandler(handler)  # overriding default ContextHandler
        parser.parse('pet.xml')

        self._pets_list = handler.return_pets_list()


    # search for particular records by the given pet name and birth date
    def search_name_birth(self, pet_name, birth_date):
        amount_of_found_items = 0
        for item in self._pets_list:
            if item['pet_name'].lower() == pet_name.lower() and item['birth_date'] == birth_date:
                amount_of_found_items += 1
        self.return_searched_amount(amount_of_found_items)

    # search for particular records by the given vet name and last appointment date
    def search_last_appointment_vet_name(self, last_appointment_date, vet_name):
        amount_of_found_items = 0
        for item in self._pets_list:
            if item['vet_name'].lower() == vet_name.lower() and item['last_appointment_date'] == last_appointment_date:
                amount_of_found_items += 1
        self.search_view.return_searched_amount(amount_of_found_items)

    # search for particular records by the given disease phrase
    def search_disease_phrase(self, world):
        amount_of_found_items = 0
        for item in self._pets_list:
            if (item['disease'].lower()).find(world.lower()) != -1:
                amount_of_found_items += 1
        self.return_searched_amount(amount_of_found_items)

    # returns the amount of found pet records
    def return_searched_amount(self, count):
        self.search_view.return_searched_amount(count)



    # delete particular records by the given parameters of pet name and birth date
    def delete_pet_name_birth_date(self, pet_name, birth_date):
        amount_of_deleted_items = 0
        for item in self._pets_list:
            if item['pet_name'].lower() == pet_name.lower() and item['birth_date'] == birth_date:
                amount_of_deleted_items += 1
                self._pets_list.remove(item)

        self.upload_patient_info()
        self.return_deleted_amount(amount_of_deleted_items)

    # delete particular records by given parameters of vet name and last appointment date
    def delete_last_appointment_date_vet_name(self, last_appointment_date, vet_name):
        amount_of_deleted_items = 0
        for item in self._pets_list:
            if item['vet_name'].lower() == vet_name.lower() and item['last_appointment_date'] == last_appointment_date:
                amount_of_deleted_items += 1
                self._pets_list.remove(item)

        self.upload_patient_info()
        self.return_deleted_amount(amount_of_deleted_items)

    # delete the particular records by the given disease phrase
    def delete_disease_phrase(self, phrase):
        amount_of_deleted_items = 0
        for item in self._pets_list:
            if (item['disease'].lower()).find(phrase.lower()) != -1:
                amount_of_deleted_items += 1
                self._pets_list.remove(item)

        self.upload_patient_info()
        self.return_deleted_amount(amount_of_deleted_items)

    # returns the amount of deleted records
    def return_deleted_amount(self, amount):
        self.delete_view.return_deleted_amount(amount)
