# отслеживает все события, которые происходят на экране
# вызывает методы модели и представления

from View.myscreen import MainScreen, MyPopup
from kivy.properties import StringProperty


class Controller:
    """координирует работу модели и представления"""

    def __init__(self, model):
        # объект модели
        self.model = model
        # создаем объект представления
        self.view = MainScreen(controller=self, model=self.model)

        self.pet_name = ''
        self.birth_date = ''
        self.last_appointment_date = ''
        self.vet_name = ''
        self.disease = ''

        self.all_is_ready_to_be_a_patient_info = 5

    def set_pet_name(self, name):
        print('con', name)
        self.pet_name = str(name)

    def set_birth(self, birth):
        self.birth_date = birth

    def set_last_appointment_date(self, app):
        self.last_appointment_date = app

    def set_vet_name(self, name: str):
        self.vet_name = name

    def set_disease(self, disease):
        self.disease = disease

    # передача модели всей инфы о pet
    # только если вся инфа соответствует требованиям
    def set_all_pet_info(self):
        self.ready=0
        if self.is_string(self.pet_name) and not self.is_empty(self.pet_name):

            self.ready+=1
        if self.is_correct_date(self.birth_date) and not self.is_empty(self.birth_date):

            self.ready+=1
        if self.is_correct_date(self.last_appointment_date) and not self.is_empty(self.last_appointment_date):

            self.ready+=1
        if self.is_string(self.vet_name)and not self.is_empty(self.vet_name):

            self.ready+=1
        if self.is_string(self.disease) and not self.is_empty(self.disease):

            self.ready+=1

        # if all input fields are ready
        if self.all_is_ready_to_be_a_patient_info == self.ready:
            self.view.everything_is_ready(True)
            self.model.pet_name = self.pet_name
            self.model.birth = self.birth_date
            self.model.last_appointment_date = self.last_appointment_date
            self.model.vet_name = self.vet_name
            self.model.disease = self.disease
            return True

        # if even one field is empty
        else:
            self.view.everything_is_ready(False)
            return False



    # returns True if str, False if it is not
    def is_string(self, string):
        numbers='1234567890'
        for i in string:
            for j in numbers:
                if i == j:
                    return False
        return True

    # returns True if empty, False if it is not
    def is_empty(self, string):
        if len(string) == 0:
            return True
        else:
            return False

    #returns True if correct False if there is ane
    def is_correct_date(self, date):
        count=0
        for i in date:
            if i == '-':
                count+= 1
        if len(date) != 10:
            return False
        elif count != 2:
            return False
        elif date[4] == '-' and date[7] == '-':
            return True


    # запись данных о пациенте
    def record_patient_info(self):
        if self.set_all_pet_info():
            self.model.record_patient_info()

    def search_name_birth(self, pet_name, birth_date):
        self.model.search_name_birth(pet_name, birth_date)

    def search_last_appointment_vet_name(self, vet_name, last_appointment_date):
        self.model.search_last_appointment_vet_name(vet_name, last_appointment_date)

    def delete_pet_name_birth_date(self, pet_name, birth_date):
        self.model.delete_pet_name_birth_date(pet_name, birth_date)

    # удаление по имени врача и дате последнего посещения
    def delete_vet_name_last_appointment_date(self, vet_name, last_appointment_date):
        self.model.delete_vet_name_last_appointment_date(vet_name, last_appointment_date)

    # считывание данных о пациенте
    def show_patient_info(self):
        return self.model.show_patient_info()

    def choose_birth_date(self):
        self.model.choose_birth_date()



    def return_birth_date(self):
        return self.model.return_birth_date()

    def set(self):
        return self.model.set()
    # поиск по фразе из диагноза
    def find_disease(self, world):
        self.model.find_disease(world)

    def get_screen(self):
        return self.view