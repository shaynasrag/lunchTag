import csv
import random
from datetime import date
from sys import argv

class Documents():
    def __init__(self, original, final):
        self.original_doc, self.final_doc = original, final
        self.formatted_rows = []
        self.people = People()

    def process(self):
        self.create_pairs_from_doc()
        self.format_rows()
        self.write_rows_to_doc()

    def create_pairs_from_doc(self):
        with open(self.original_doc) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for line in csv_reader:
                self.people.individual_list.append(Person(line[1], line[2]))
                self.people.num_people += 1
        self.people.create_pairs()
    
    def format_rows(self):
        for pair in self.people.pair_list:
            row = ['{0}: {1}'.format(person.name, person.email) for person in pair]
            self.formatted_rows.append(row)

    def write_rows_to_doc(self):
        with open(final_doc, mode = 'w') as lunch_pairs:
            pair_writer = csv.writer(lunch_pairs, delimiter=',', quotechar='"')
            pair_writer.writerow(["Person 1 (Sender)", "Person 2 (Recipient)", "Person 3 (Recipient)"])
            for row in self.formatted_rows:
                pair_writer.writerow(row)

class People():
    def __init__(self):
        self.num_people = 0
        self.individual_list = self.pair_list = []

    def create_pairs(self):
        random.shuffle(self.individual_list)
        first_person = 3 if self.resolve_extra_pair() else 0
        self.add_pairs_to_list(first_person)

    def resolve_extra_pair(self):
        if self.num_people % 2 == 1:
            self.pair_list.append([self.individual_list[0], self.individual_list[1], self.individual_list[2]])
            return True

    def add_pairs_to_list(self, curr_person):
        while curr_person < self.num_people:
            self.pair_list.append([self.individual_list[curr_person], self.individual_list[curr_person + 1]])
            curr_person += 2

class Person():
    def __init__(self, name, email):
        self.name = name
        self.email = email

if __name__ == "__main__":
    original_doc = argv[1]
    category = argv[2]

    today = date.today()
    formatted_date = today.strftime("%m-%d-%Y")
    final_doc = category + "-lunch_pairs-" + formatted_date + ".csv"

    Documents(original_doc, final_doc).process()