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

from Model.sax_parser import PetElement

from kivymd.uix.picker import MDDatePicker

from View.myscreen import MainScreen


class Model:
    """
    The MyScreenModel class is a data model implementation. The model stores
    the values of the variables `c`, `d` and their sum. The model provides an
    interface through which to work with stored values. The model contains
    methods for registration, deletion and notification observers.

    The model is (primarily) responsible for the logic of the application.
    MyScreenModel class task is to add two numbers.
    """

    def __init__(self):
        self._pet_name = ''
        self._birth = ''
        self._last_appointment_date = ''
        self._vet_name =''
        self._disease=''
        self.val = ''

        self.view = MainScreen()


        # список классов наблюдателя
        self._observers = []
        # список всех пациентов
        self._pets_list = []


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

    # добавляю все записи в один список
    def add_info(self):
        # создаю отдельную запись для пациента
        self._patients = {}
        self._patients['pet_name'] = self._pet_name
        self._patients['birth_date'] = self._birth
        self._patients['last_appointment_date'] = self._last_appointment_date
        self._patients['vet_name'] = self._vet_name
        self._patients['disease'] = self._disease
        # добавляю эту запись ко всем остальным записям
        self._pets_list.append(self._patients)

        self._pet_name=''
        self._birth=''
        self._vet_name=''
        self._last_appointment_date=''
        self._disease=''


    # запись информации о животном в файлик
    def record_patient_info(self):
        # добавляю все записи в один список
        self.show_patient_info()
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

    # считывание данных о пациенте
    def show_patient_info(self):
        parser = sax.make_parser()  # creating an XMLReader
        parser.setFeature(sax.handler.feature_namespaces, 0)  # turning off namespaces
        handler = PetElement()
        parser.setContentHandler(handler)  # overriding default ContextHandler
        parser.parse('pet.xml')

        self._pets_list = handler.return_pets_list()
        print('SAX:')
        for item in self._pets_list:
            print(item)

    # поиск по имени и дате рождения
    def search_name_birth(self, pet_name, birth_date):
        for item in self._pets_list:
            if item['pet_name'] == pet_name and item['birth_date'] == birth_date:
                print(item)

    # поиск по врачу и дате псоледнего посещения
    def search_last_appointment_vet_name(self, vet_name, last_appointment_date):
        for item in self._pets_list:
            if item['vet_name'] == vet_name and item['last_appointment_date'] == last_appointment_date:
                print(item)

    # поиск по фразе из диагноза
    def find_disease(self, world):
        for item in self._pets_list:
            if item['disease'].find(world) != -1:
                print('found')

    # удаление по имени и дате рождения
    def delete_pet_name_birth_date(self, pet_name, birth_date):
        amount_of_deleted_pets = 0
        for item in self._pets_list:
            if item['pet_name'] == pet_name and item['birth_date'] == birth_date:
                amount_of_deleted_pets += 1
                self._pets_list.remove(item)
                print(self._pets_list)
            if amount_of_deleted_pets == 0:
                print('there no records then suit the condition')

    # удаление по имени и дате рождения
    def delete_vet_name_last_appointment_date(self, vet_name, last_appointment_date):
        amount_of_deleted_pets = 0
        for item in self._pets_list:
            if item['vet_name'] == vet_name and item['last_appointment_date'] == last_appointment_date:
                amount_of_deleted_pets += 1
                self._pets_list.remove(item)
                print(self._pets_list, amount_of_deleted_pets)
            if amount_of_deleted_pets == 0:
                print('there no records then suit the condition')








    def return_birth_date(self):
        return str(self._birth)


    # # добавление наблюдателей
    # def add_observer(self, observer):
    #     self._observers.append(observer)
    #
    # # удаление наблюдателей
    # def remove_observer(self, observer):
    #     self._observers.remove(observer)
    #
    # # оповещение наблюдателей
    # def notify_observers(self):
    #     # будет вызываться наблюдателем, когда модель меняется
    #     self._names.append(self._name)
    #     for observer in self._observers:
    #         observer.model_is_changed()
    #     print(self._observers)
    #     print(self._names)