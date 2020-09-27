import re
import csv


class ModifyingPhoneBook:

    def __init__(self):
        self.phonenumbers_modified = []
        self.person_info_modified = []
        self.person_info = []
        self.contacts_list_modified = []

    def open_file(self):
        with open("phonebook_raw.csv", encoding='utf-8') as f:
            rows = csv.reader(f, delimiter=",")
            contacts_list = list(rows)
        return contacts_list

    def modifying_phonenumbers(self):
        contacts_list = self.open_file()
        for data in contacts_list:
            data_modified = []
            for item in data:
                regex = r"(\+7|8)(\s*)\(*(\d{3})\)*(\s|-)*(\d{3})((\s|-)*)(\d{2})(\s|-)*(\d*)(\s*)(\(?)([а-яёА-ЯЁ]*\.?)\s*(\d*)\)?"
                subst = "+7(\\3)\\5-\\8-\\10\\11\\13\\14"
                result = re.sub(regex, subst, item, 0, re.MULTILINE)
                data_modified.append(result)
            if data_modified not in self.phonenumbers_modified:
                self.phonenumbers_modified.append(data_modified)

    def modifying_phonebook_names(self):
        for line in self.phonenumbers_modified:
            organization = line[3]
            position = line[4]
            phone = line[5]
            email = line[6]
            if line[1] == '' and line[2] == '' and line[0].count(' ') == 2:
                name = line[0].split(' ')
                lastname = name[0]
                firstname = name[1]
                surname = name[2]
            elif line[1] == '' and line[2] == '' and line[0].count(' ') == 1:
                name = line[0].split(' ')
                lastname = name[0]
                firstname = name[1]
                surname = ''
            elif line[1] != '' and line[2] == '':
                name = line[1].split(' ')
                lastname = line[0]
                firstname = name[0]
                surname = name[1]
            elif line[:2] != '':
                lastname = line[0]
                firstname = line[1]
                surname = line[2]
            self.info_list = [lastname, firstname, surname, organization, position, phone, email]
            self.person_info.append(self.info_list)
            self.modifying_person_info()

    def modifying_person_info(self):
        for info in self.person_info:
            if self.info_list[:2] == info[:2]:
                index = 0
                for item in self.info_list:
                    if item != info[index] and item != '':
                        info.insert(index, item)
                    index += 1
                if info not in self.person_info_modified:
                    self.person_info_modified.append(info)

    def making_result_list(self):
        self.contacts_list_modified.append(self.person_info_modified[0])
        for person_info in sorted(self.person_info_modified):
            if '+' in person_info[6]:
                person_info[5], person_info[6] = person_info[6], person_info[5]
            if '+' in person_info[5]:
                self.contacts_list_modified.append(person_info[:7])
        for item in self.contacts_list_modified:
            print(item)

    def save_new_phonebook(self):
        with open("phonebook.csv", "w") as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerows(self.contacts_list_modified)


modifying = ModifyingPhoneBook()
modifying.open_file()
modifying.modifying_phonenumbers()
modifying.modifying_phonebook_names()
modifying.making_result_list()
modifying.save_new_phonebook()
