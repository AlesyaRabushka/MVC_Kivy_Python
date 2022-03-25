# отслеживает все события, которые происходят на экране
# вызывает методы модели и представления

from View.myscreen import MainScreen


class Controller:
    """координирует работу модели и представления"""

    def __init__(self, model):
        # объект модели
        self.model = model
        # создаем объект представления
        self.view = MainScreen(controller=self, model=self.model)

    def set_pet_name(self, name: str):
        self.model.pet_name = name

    def set_birth(self, birth):
        self.model.birth = birth

    def set_last_appointment_date(self, app):
        self.model.last_appointment_date = app

    def set_vet_name(self, name: str):
        self.model.vet_name = name

    def set_disease(self, disease):
        self.model._disease = disease


    # запись данных о пациенте
    def record_patient_info(self):
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