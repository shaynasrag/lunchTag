import csv
import random
from datetime import date
from sys import argv

class Documents():
    def __init__(self, original, final):
        self.original_doc = original
        self.final_doc = final
        self.formatted_rows = []
        self.people = People()

    def process(self):
        self.parse_doc_and_make_pairs()
        self.write_pairs_to_doc()

    def parse_doc_and_make_pairs(self):
        with open(self.original_doc) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for line in csv_reader:
                self.people.individual_list.append(Person(line[1], line[2]))
                self.people.num_people += 1
        self.people.create_pairs()

    def write_pairs_to_doc(self):
        with open(final_doc, mode = 'w') as lunch_pairs:
            pair_writer = csv.writer(lunch_pairs, delimiter=',', quotechar='"')
            self.format_rows()
            pair_writer.writerow(["Person 1 (Sender)", "Person 2 (Recipient)", "Person 3 (Recipient)"])
            for row in self.formatted_rows:
                pair_writer.writerow(row)

    def format_rows(self):
        for pair in self.people.pair_list:
            row = []
            for person in pair:
                row.append(person.name + ': ' + person.email)
            self.formatted_rows.append(row)

class Person():
    def __init__(self, name, email):
        self.name = name
        self.email = email

class People():
    def __init__(self):
        self.num_people = 0
        self.individual_list = []
        self.pair_list = []

    def create_pairs(self):
        first_person = self.find_first_person()
        self.add_pairs(first_person)

    def find_first_person(self):
        random.shuffle(self.individual_list)
        first_person = 0
        if self.num_people % 2 == 1:
            self.process_extra_pair()
            first_person = 3
        return first_person

    def process_extra_pair(self):
        self.pair_list.append([self.individual_list[0], self.individual_list[1], self.individual_list[2]])

    def add_pairs(self, curr_person):
        while curr_person < self.num_people:
            self.pair_list.append([self.individual_list[curr_person], self.individual_list[curr_person + 1]])
            curr_person += 2

if __name__ == "__main__":
    original_doc = argv[1]
    category = argv[2]

    today = date.today()
    date = today.strftime("%m-%d-%Y")
    final_doc = category + "-lunch_pairs-" + date + ".csv"

    documents = Documents(original_doc, final_doc)
    documents.process()
