import xml.sax

class PetElement(xml.sax.ContentHandler):
    def __init__(self):
        self.current_data = False
        self.pet_name = False
        self.birth_date = False
        self.last_appointment_date = False
        self.vet_name = False
        self.disease = False


    def startElement(self, name, attrs):
        self.current_data = name
        if self.current_data == 'pets_list':
            self.pets_list = []
        elif self.current_data == 'pet':
            self.pet = {}
        elif self.current_data == 'pet_name':
            self.pet_name=True
            #print('petname:', self.pet_name)
        elif self.current_data == 'birth_date':
            self.birth_date = True
            #print('birth date: ', self.birth_data)
        elif self.current_data == 'last_appointment_date':
            self.last_appointment_date = True
            #print('last appointment date: ', self.last_appointment_date)
        elif self.current_data == 'vet_name':
            self.vet_name = True
            #print('vet name: ', self.vet_name)
        elif self.current_data == 'disease':
            self.disease = True
            #print('disease: ', self.disease)
        self.current_data=''


    def endElement(self, tag):
        if tag == 'pet':
            self.pets_list.append(self.pet)
            self.pet = {}

    def characters(self, content):
        if self.pet_name:
            #self.pet_name = content
            self.pet['pet_name'] = content
            self.pet_name = False
        elif self.birth_date:
            self.pet['birth_date'] = content
            self.birth_date = False
            #self.birth_data = content
        elif self.last_appointment_date:
            self.pet['last_appointment_date'] = content
            self.last_appointment_date = False
            #self.last_appointment_date = content
        elif self.vet_name:
            self.pet['vet_name'] = content
            self.vet_name = False
            #self.vet_name = content
        elif self.disease:
            self.pet['disease'] = content
            self.disease = False
           #self.disease = content

    def return_pets_list(self):
        return self.pets_list
