# отслеживает все события, которые происходят на экране
# вызывает методы модели и представления

from View.myscreen import MainScreen, AddPopup, SearchPopup
from kivy.properties import StringProperty


class Controller:
    """координирует работу модели и представления"""

    def __init__(self, model):
        # model
        self.model = model

        # сview screens
        self.main_view = MainScreen(controller=self, model=self.model)
        self.view = AddPopup(controller=self, model=self.model)
        self.search_view = SearchPopup(controller=self, model=self.model)

        self.pet_name = ''
        self.birth_date = ''
        self.last_appointment_date = ''
        self.vet_name = ''
        self.disease = ''

        self.all_is_ready_to_be_a_patient_info = 5

    def set_pet_name(self, name):
        self.pet_name = str(name)

    def set_birth(self, birth):
        self.birth_date = birth

    def set_last_appointment_date(self, app):
        self.last_appointment_date = app

    def set_vet_name(self, name: str):
        self.vet_name = name

    def set_disease(self, disease):
        self.disease = disease


    # is called to correct the input data
    def set_all_pet_info(self):
        self.ready_=0
        if self.is_string(self.pet_name) and not self.is_empty(self.pet_name):

            self.ready_+=1
        if self.is_correct_date(self.birth_date) and not self.is_empty(self.birth_date):

            self.ready_+=1
        if self.is_correct_date(self.last_appointment_date) and not self.is_empty(self.last_appointment_date):

            self.ready_+=1
        if self.is_string(self.vet_name)and not self.is_empty(self.vet_name):

            self.ready_+=1
        if self.is_string(self.disease) and not self.is_empty(self.disease):

            self.ready_+=1

        # if all input fields are ready
        if self.all_is_ready_to_be_a_patient_info == self.ready_:
            self.model.pet_name = self.pet_name
            self.model.birth = self.birth_date
            self.model.last_appointment_date = self.last_appointment_date
            self.model.vet_name = self.vet_name
            self.model.disease = self.disease

            self.pet_name = ''
            self.birth_date = ''
            self.last_appointment_date = ''
            self.vet_name = ''
            self.disease = ''
            return True

        # if even one field is empty
        elif self.all_is_ready_to_be_a_patient_info != self.ready_:
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

    # returns True if correct False if it is not
    def is_correct_date(self, date):
        #
        count = 0
        full_date = []
        item = ''
        for i in date:
            if i == '-':
                count += 1
                full_date.append(item)
                item = ''
            else:
                item += i
        full_date.append(item)

        # check the right year, month and date values
        if len(date) != 10:
            return False
        elif count != 2:
            return False
        elif date[4] == '-' and date[7] == '-':

            if int(full_date[0]) > 2022 or int(full_date[0]) < 0:
                full_date.clear()
                return False
            elif int(full_date[1]) > 12 or int(full_date[1]) < 0:
                full_date.clear()
                return False
            elif int(full_date[1]) == 2:
                if int(full_date[0]) % 4 == 0 and int(full_date[0]) % 100 != 0 or int(full_date[0]) % 400 == 0:
                    if int(full_date[2]) > 29:
                        full_date.clear()
                        return False
                    else:
                        full_date.clear()
                        return True
                else:
                    if int(full_date[2]) > 28:
                        full_date.clear()
                        return False
                    else:
                        full_date.clear()
                        return True



            elif int(full_date[1]) % 2 == 0:
                if int(full_date[2]) > 30:
                    full_date.clear()
                    return False
                else:
                    full_date.clear()
                    return True
            elif int(full_date[1]) % 2 == 1:
                if int(full_date[2]) > 31:
                    full_date.clear()
                    return False
                else:
                    full_date.clear()
                    return True




    # if info is correct -> to the model
    # else -> dialog
    def record_patient_info(self):
        correct_check = self.set_all_pet_info()
        if correct_check == True:
            self.view.dialogs(True)
            self.model.record_patient_info()
        elif correct_check == False:
            self.view.dialogs(False)


        # IS USED ONLY IN PURPOSE OF MAKING INCORRECT RECORDS
        # self.model.pet_name = self.pet_name
        # self.model.birth = self.birth_date
        # self.model.last_appointment_date = self.last_appointment_date
        # self.model.vet_name = self.vet_name
        # self.model.disease = self.disease
        # self.model.record_patient_info()
        # self.pet_name = ''
        # self.birth_date = ''
        # self.last_appointment_date = ''
        # self.vet_name = ''
        # self.disease = ''



    def show_patient_info(self):
        return self.model.show_patient_info()


    def search_name_birth(self, pet_name, birth_date):
        if self.is_correct_date(birth_date) and self.is_string(pet_name):
            self.model.search_name_birth(pet_name, birth_date)
        else:
            self.search_view.wrong_input_dialog()

    def search_last_appointment_vet_name(self, last_appointment_date, vet_name):
        if self.is_correct_date(last_appointment_date) and self.is_string(vet_name):
            self.model.search_last_appointment_vet_name(last_appointment_date, vet_name)
        else:
            self.search_view.wrong_input_dialog()

    def search_disease_phrase(self, phrase):
        if self.is_string(phrase):
            self.model.search_disease_phrase(phrase)
        else:
            self.search_view.wrong_input_dialog()


    def delete_pet_name_birth_date(self, pet_name, birth_date):
        if self.is_correct_date(birth_date) and self.is_string(pet_name):
            self.model.delete_pet_name_birth_date(pet_name, birth_date)
        else:
            self.search_view.wrong_input_dialog()

    def delete_vet_name_last_appointment_date(self, vet_name, last_appointment_date):
        if self.is_correct_date(last_appointment_date) and self.is_string(vet_name):
            self.model.delete_vet_name_last_appointment_date(vet_name, last_appointment_date)
        else:
            self.search_view.wrong_input_dialog()

    def delete_disease_phrase(self, phrase):
        if self.is_string(phrase):
            self.model.delete_disease_phrase(phrase)
        else:
            self.search_view.wrong_input_dialog()




    # DO NOT TOUCH
    # returns the main  screen
    def get_screen(self):
        return self.main_view