import os
from kivy.lang import Builder

import xml.sax
from kivy.uix.popup import Popup




class PetElement(xml.sax.ContentHandler):
    def __init__(self, model):
        self.current_data = False
        self.pet_name = False
        self.birth_date = False
        self.last_appointment_date = False
        self.vet_name = False
        self.disease = False
        self.handler_name = False
        self.phone_number = False
        self.mail = False
        self.address = False

        self.model = model

        # self.dialog = main_view

        self.count_pet = 0
        self.count_handler = 0
        self.bad_files_count = 0
        self.bad_lines = {}




    def startElement(self, name, attrs):
        self.current_data = name
        if self.current_data == 'pets_list':
            self.pets_list = []
            self.handlers_list = []
            self.all_list = []
            self.lines = []
            self.line = 1


        elif self.current_data == 'pet':
            self.pet = {}
            self.handler = {}
            self.all = {}
            self.line += 1

        elif self.current_data == 'pet_name':
            self.pet_name=True
            self.line += 1
            print(self.line)
            #print('petname:', self.pet_name)
        elif self.current_data == 'birth_date':
            self.birth_date = True
            self.line += 1
            #print('birth date: ', self.birth_data)
        elif self.current_data == 'last_appointment_date':
            self.last_appointment_date = True
            self.line += 1
            #print('last appointment date: ', self.last_appointment_date)
        elif self.current_data == 'vet_name':
            self.vet_name = True
            self.line += 1
            #print('vet name: ', self.vet_name)
        elif self.current_data == 'disease':
            self.disease = True
            self.line += 1


        elif self.current_data == 'handler_name':
            self.handler_name = True
            self.line += 1
        elif self.current_data == 'phone_number':
            self.phone_number = True
            self.line += 1
        elif self.current_data == 'mail':
            self.mail = True
            self.line += 1
        elif self.current_data == 'handler_address':
            self.address = True
            self.line += 1
        elif self.current_data == 'pet_name/':
            print('baddesss$')
            #print('disease: ', self.disease)
        self.current_data=''


    def endElement(self, tag):
        if tag == 'pet':
            if self.count_pet == 5 and self.count_handler == 4:
                self.pets_list.append(self.pet)
                self.handlers_list.append(self.handler)
                self.all_list.append(self.all)

                self.pet = {}
                self.handler = {}
                self.all = {}

                self.count_pet=0
                self.count_handler=0
            else:
                #print('bad file')
                self.count_pet = 0
                self.count_handler = 0
                self.bad_files_count += 1


    def characters(self, content):
        # pet info
        if self.pet_name:
            #self.pet_name = content
            self.pet['pet_name'] = content
            self.all['pet_name'] = content
            self.count_pet += 1
            self.pet_name = False


            #print(content)

            # if self.line % 11 != 4:
            #     print('error in line' , self.line)
            #     # self.line -= 1
            #     #self.count_pet -= 1
            #
            # else:
            #     self.pet['pet_name'] = content
            #     self.all['pet_name'] = content
            #     self.count_pet += 1
            #     print('pet_name ', self.line)

        # elif self.pet_name == False:
        #         print('not name ',self.line)
        #         if self.line > 12:
        #             self.bad_line.append(self.line - 8)
        #         else:
        #             self.bad_line.append(self.line)
                #print(self.bad_line)
        elif self.birth_date:
            self.pet['birth_date'] = content
            self.all['birth_date'] = content
            self.birth_date = False
            print('birth ',self.line)
            self.count_pet += 1
            #self.birth_data = content
        elif self.last_appointment_date:
            self.pet['last_appointment_date'] = content
            self.all['last_appointment_date'] = content
            self.last_appointment_date = False
            self.count_pet += 1
            print('last ', self.line)
            #self.last_appointment_date = content
        elif self.vet_name:
            self.pet['vet_name'] = content
            self.all['vet_name'] = content
            self.vet_name = False
            self.count_pet += 1
            print('vet ', self.line)
            #self.vet_name = content
        elif self.disease:
            self.pet['disease'] = content
            self.all['disease'] = content
            self.disease = False
            self.count_pet += 1
            print('disease ',self.line)

        # handler info
        elif self.handler_name:
            self.handler['handler_name'] = content
            self.all['handler_name'] = content
            self.handler_name = False
            self.count_handler += 1
        elif self.phone_number:
            self.handler['phone_number'] = content
            self.all['phone_number'] = content
            self.phone_number = False
            self.count_handler += 1
        elif self.mail:
            self.handler['mail'] = content
            self.all['mail'] = content
            self.mail = False
            self.count_handler += 1
        elif self.address:
            self.handler['handler_address'] = content
            self.all['handler_address'] = content
            self.address = False
            self.count_handler += 1
           #self.disease = content

    def return_pets_list(self):
        return self.pets_list
    def return_handlers_list(self):
        return self.handlers_list
    def return_all_list(self):
        return self.all_list
    def return_bad_files_count(self):
        return self.bad_files_count


#Builder.load_file(os.path.join(os.path.dirname(__file__), "sax_parser.kv"))