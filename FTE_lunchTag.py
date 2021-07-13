import csv
from datetime import date
from sys import argv

class Documents():
    def __init__(self, original, final):
        self.original_doc = original
        self.final_doc = final
        self.formatted_rows = []
        self.pairs = Pairs()

    def process(self):
        self.create_people_from_doc()
        self.pairs.generate_pairs()
        self.write_pairs_to_doc()

    def create_people_from_doc(self):
        with open(self.original_doc) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for line in csv_reader:
                self.create_person(line[1], line[2], line[3], line[4], line[5], line[6], line[7])

    def create_person(self, name, email, employee_type, category, match_preference, intern_one_thing, FTE_one_thing):
        if employee_type == "Intern/Co-op":
            self.pairs.create_intern(name, email, category, match_preference, intern_one_thing)
        else:
            self.pairs.create_fte(name, email, category, match_preference, FTE_one_thing)
    
    def write_pairs_to_doc(self):
        with open(final_doc, mode = 'w') as lunch_pairs:
            pair_writer = csv.writer(lunch_pairs, delimiter=',', quotechar='"')
            self.format_rows()
            pair_writer.writerow(["Intern/Co-op (Sender)", "Full Time Employee (Recipient)"])
            for row in self.formatted_rows:
                pair_writer.writerow(row)

    def format_rows(self):
        for pair in self.pairs.pair_list:
            row = []
            for person in pair:
                row.append(person.category + ' ' + person.preference + '\n' + person.name + ': ' + person.email + '\nOne thing I would like to talk about is: ' + person.one_thing)
            self.formatted_rows.append(row)

class Pairs():
    def __init__(self):
        self.pair_list = []
        self.internscoops = People()
        self.ftes = People()
        self.category_ls = ["Design", "Product Management (PM)", "Software Engineering/Frontend (SWE)", "Software Engineering/Backend (SWE)"]
        self.preference_dict = {
            "Anyone! Put me in the general pool, please": "general",
            "Someone in my category, please": "priority",
            "I'd prefer to get matched with my category but am happy to talk to anyone!": "regular"
        }
    def create_intern(self, name, email, category, match_preference, intern_one_thing):
        self.internscoops.add_person(Person(name, email, category, self.preference_dict[match_preference], intern_one_thing))
    
    def create_fte(self, name, email, category, match_preference, FTE_one_thing):
        self.ftes.add_person(Person(name, email, category, self.preference_dict[match_preference], FTE_one_thing))
    
    def generate_pairs(self):
        self.match_by_category("priority")
        self.match_by_category("regular")
        self.create_general_pairs()

    def match_by_category(self, preference):
        for category in self.category_ls:
            self.match_people(category, preference)
    
    def match_people(self, category, preference):
        curr_sets = {
            "priority": [self.internscoops.priority_set_dict[category], self.ftes.priority_set_dict[category]],
            "regular": [self.internscoops.regular_set_dict[category], self.ftes.regular_set_dict[category]]
        }
        interncoop_set = curr_sets[preference][0]
        fte_set = curr_sets[preference][1]
        self.equalize_sets(fte_set, interncoop_set, category, preference)
        for interncoop, fte in zip(interncoop_set, fte_set):
            self.pair_list.append([interncoop, fte])
    
    def equalize_sets(self, fte_set, interncoop_set, category, preference):
        next_sets = {
            "priority": [self.internscoops.regular_set_dict[category], self.ftes.regular_set_dict[category]],
            "regular": [self.internscoops.general_set, self.ftes.general_set]
        }
        diff = len(fte_set) - len(interncoop_set)
        if diff > 0:
            self.equalize(diff, fte_set, next_sets[preference][1])
        else:
            self.equalize(0 - diff, interncoop_set, next_sets[preference][0])

    def equalize(self, diff, curr_set, new_set):
        while diff > 0:
            iterator = iter(curr_set)
            item = next(iterator, None)
            curr_set.remove(item)
            new_set.add(item)
            diff -= 1
    
    def create_general_pairs(self):
        fte_set = self.ftes.general_set
        interncoop_set = self.internscoops.general_set
        for fte, interncoop in zip(fte_set, interncoop_set):
            self.pair_list.append([fte, interncoop])

class People():
    def __init__(self):
        self.num_people = 0
        self.general_set = set()
        self.priority_set_dict = self.regular_set_dict = {
            "Design": set(), 
            "Product Management (PM)": set(), 
            "Software Engineering/Frontend (SWE)": set(), 
            "Software Engineering/Backend (SWE)": set(), 
        }
        self.set_dicts = {
            "regular": self.regular_set_dict,
            "priority": self.priority_set_dict
        }

    def add_person(self, person):
        if person.category == "Not Listed/Other" or person.preference == "general":
            self.general_set.add(person)
        else:
            dictionary = self.set_dicts[person.preference]
            dictionary[person.category].add(person)
        self.num_people += 1

class Person():
    def __init__(self, name, email, category, preference, one_thing):
        self.name = name
        self.email = email
        self.category = category
        self.preference = preference 
        self.one_thing = one_thing
        
if __name__ == "__main__":
    original_doc = argv[1]

    today = date.today()
    date = today.strftime("%m-%d-%Y")
    final_doc = "FTE-lunch_pairs-" + date + ".csv"

    documents = Documents(original_doc, final_doc)
    documents.process()