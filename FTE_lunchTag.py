import csv
from datetime import date
from sys import argv

class Documents():
    def __init__(self, original, final):
        self.original_doc, self.final_doc = original, final
        self.formatted_rows = []
        self.pairs = Pairs()
        self.create_pairs_dict = {
            "Intern/Co-op": (self.pairs.internscoops.add_person, 0),
            "Full Time Employee (FTE)": (self.pairs.ftes.add_person, 1)
        }
        self.preference_dict = {
            "Anyone! Put me in the general pool, please": "general",
            "Someone in my category, please": "priority",
            "I'd prefer to get matched with my category but am happy to talk to anyone!": "regular"
        }

    def process(self):
        self.create_pairs_from_doc()
        self.format_rows()
        self.write_rows_to_doc()

    def create_pairs_from_doc(self):
        with open(self.original_doc) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for line in csv_reader:
                self.create_person(line[1], line[2], line[3], line[4], line[5], [line[6], line[7]])
        self.pairs.create_pairs()

    def create_person(self, name, email, employee_type, category, match_preference, one_thing_ls):
        create_func, i = self.create_pairs_dict[employee_type]
        create_func(Person(name, email, category, self.preference_dict[match_preference], one_thing_ls[i]))
    
    def format_rows(self):
        for pair in self.pairs.pair_list:
            row = ['{0}: {1}\n{2}\nOne thing I would like to talk about is: {3}'.format(person.name, person.email, person.category, person.one_thing) for person in pair]
            self.formatted_rows.append(row)
    
    def write_rows_to_doc(self):
        with open(final_doc, mode = 'w') as lunch_pairs:
            pair_writer = csv.writer(lunch_pairs, delimiter=',', quotechar='"')
            pair_writer.writerow(["Intern/Co-op (Sender)", "Full Time Employee (Recipient)"])
            for row in self.formatted_rows:
                pair_writer.writerow(row)

class Pairs():
    def __init__(self):
        self.pair_list = []
        self.internscoops = self.ftes = People()
        self.category_ls = ["Design", "Product Management (PM)", "Software Engineering/Frontend (SWE)", "Software Engineering/Backend (SWE)"]
        self.curr_sets = {
            "priority": None, "regular": None, "general": [self.internscoops.general_set, self.ftes.general_set]
        }
        self.next_sets = {
            "priority": None, "regular": [self.internscoops.general_set, self.ftes.general_set]
        }

    def create_pairs(self):
        self.match_by_category("priority")
        self.match_by_category("regular")
        self.match_people(self.curr_sets["general"][0], self.curr_sets["general"][1])

    def match_by_category(self, preference):
        for category in self.category_ls:
            self.update_set_dicts(category)
            self.equalize_sets(self.curr_sets[preference][1], self.curr_sets[preference][0], preference)
            self.match_people(fte_set=self.curr_sets[preference][1], interncoop_set=self.curr_sets[preference][0])
    
    def update_set_dicts(self, category):
        self.curr_sets["priority"] = [self.internscoops.priority_set_dict[category], self.ftes.priority_set_dict[category]]
        self.curr_sets["regular"] = [self.internscoops.regular_set_dict[category], self.ftes.regular_set_dict[category]]
        self.next_sets["priority"] = [self.internscoops.regular_set_dict[category], self.ftes.regular_set_dict[category]]
    
    def equalize_sets(self, fte_set, interncoop_set, preference):
        diff = len(fte_set) - len(interncoop_set)
        if diff > 0:
            self.balance_sets(diff, iter(fte_set), fte_set, self.next_sets[preference][1])
        else:
            self.balance_sets(0 - diff, iter(interncoop_set), interncoop_set, self.next_sets[preference][0])

    def balance_sets(self, diff, iterator, curr_set, next_set):
        while diff > 0:
            item = next(iterator, None)
            curr_set.remove(item)
            next_set.add(item)
            diff -= 1
    
    def match_people(self, interncoop_set, fte_set):
        for interncoop, fte in zip(interncoop_set, fte_set):
            self.pair_list.append([interncoop, fte])

class People():
    def __init__(self):
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
            self.set_dicts[person.preference][person.category].add(person)

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
    formatted_date = today.strftime("%m-%d-%Y")
    final_doc = "FTE-lunch_pairs-" + formatted_date + ".csv"

    Documents(original_doc, final_doc).process()