import csv
from datetime import date
from sys import argv, exit

class Documents():
    def __init__(self, original, final, group_type):
        self.original_doc, self.final_doc = original, final
        self.formatted_rows = []
        self.static = Static()
        self.pairs = Pairs(self.static) if group_type == "-pairs" else Groups(self.static)
        self.new_doc_header = self.pairs.new_doc_header
        self.create_pairs_dict =  self.static.get_create_pairs_dict(self.pairs.internscoops.add_person, self.pairs.ftes.add_person)
        self.preference_dict = self.static.preference_dict

    def process(self):
        self.create_pairs_from_doc()
        self.format_rows()
        self.write_rows_to_doc()

    def create_pairs_from_doc(self):
        counter = 0
        with open(self.original_doc) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for line in csv_reader:
                counter += 1
                self.create_person(line[1], line[2], line[3], line[4], line[5], [line[6], line[7]])
        self.pairs.create_pairs()

    def create_person(self, name, email, employee_type, category, match_preference, one_thing_ls):
        create_func, i = self.create_pairs_dict[employee_type]
        create_func(Person(name, email, category, self.preference_dict[match_preference], one_thing_ls[i]))
    
    def format_rows(self):
        for pair in self.pairs.pair_list:
            row = ['{0}: {1}\n{2}\nOne thing I would like to talk about is: {3}'.format(person.name, person.email, person.category, person.one_thing) if isinstance(person, Person) else "" for person in pair]
            self.formatted_rows.append(row)
    
    def write_rows_to_doc(self):
        with open(final_doc, mode = 'w') as lunch_pairs:
            pair_writer = csv.writer(lunch_pairs, delimiter=',', quotechar='"')
            pair_writer.writerow(self.new_doc_header)
            for row in self.formatted_rows:
                pair_writer.writerow(row)

class Pairs():
    def __init__(self, static):
        self.static = static
        self.pair_list = []
        self.internscoops, self.ftes = People(), People()
        self.new_doc_header = self.static.get_new_doc_header("pairs")
        self.category_ls = self.static.category_ls
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
            self.update_instance_variables(category, preference)
            self.equalize_sets()
            self.match_people()
    
    def update_instance_variables(self, category, preference):
        self.preference = preference
        self.category = category
        self.update_set_dicts()
        self.update_sets()
        
    
    def update_sets(self):
        self.fte_set = self.curr_sets[self.preference][1]
        self.interncoop_set = self.curr_sets[self.preference][0]

    def update_set_dicts(self):
        self.curr_sets["priority"] = [self.internscoops.priority_set_dict[self.category], self.ftes.priority_set_dict[self.category]]
        self.curr_sets["regular"] = [self.internscoops.regular_set_dict[self.category], self.ftes.regular_set_dict[self.category]]
        self.next_sets["priority"] = [self.internscoops.regular_set_dict[self.category], self.ftes.regular_set_dict[self.category]]
    
    def equalize_sets(self):
        diff = len(self.fte_set) - len(self.interncoop_set)
        if diff > 0:
            self.balance_sets(diff, self.fte_set, self.next_sets[self.preference][1])
        else:
            self.balance_sets(0 - diff, self.interncoop_set, self.next_sets[self.preference][0])

    def balance_sets(self, diff, curr_set, next_set):
        while diff > 0:
            iterator = iter(curr_set)
            item = next(iterator, None)
            curr_set.remove(item)
            next_set.add(item)
            diff -= 1
    
    def match_people(self):
        for interncoop, fte in zip(self.interncoop_set, self.fte_set):
            self.pair_list.append([interncoop, fte])

class Groups(Pairs):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new_doc_header = self.static.get_new_doc_header("groups")
    
    def create_pairs(self):
        self.match_by_category("priority")
        self.match_by_category("regular")
        self.match_general(list(self.curr_sets["general"][0]), list(self.curr_sets["general"][1]))

    def match_general(self, intern_ls, fte_ls):
        i = j = 0
        while i < len(intern_ls):
            if len(intern_ls) - i == len(fte_ls) - j:
                self.pair_list.append([intern_ls[i], "", fte_ls[j]])
                i += 1
                j += 1
            else:
                self.pair_list.append([intern_ls[i], intern_ls[i + 1], fte_ls[j]])
                i += 2
                j += 1

    def match_people(self):
        intern_ls, fte_ls = list(self.interncoop_set), list(self.fte_set)
        i = j = 0
        while j < len(fte_ls):
            if i + 1 < len(intern_ls):
                self.pair_list.append([intern_ls[i], intern_ls[i + 1], fte_ls[j]])
                i += 2
                j += 1 

    def equalize_sets(self):
        if not self.sets_empty():
            self.make_interns_even()
            diff = (len(self.interncoop_set) // 2) - len(self.fte_set)
            key = 1 if diff > 0 else 0
            self.remove_difference(diff, key)

    def remove_difference(self, diff, key):
        diff_dict = {
            0: [0 - diff, self.fte_set, self.next_sets[self.preference][1]],
            1: [diff * 2, self.interncoop_set, self.next_sets[self.preference][0]]
        }
        self.balance_sets(diff_dict[key][0], diff_dict[key][1], diff_dict[key][2])

    def make_interns_even(self):
        if len(self.interncoop_set) % 2 == 1:
            self.move_to_next_set(iter(self.interncoop_set), self.interncoop_set, self.next_sets[self.preference][0])

    def sets_empty(self):
        if len(self.interncoop_set) == 0 or len(self.fte_set) == 0:
            self.move_all_to_next_set()

    def balance_sets(self, diff, curr_set, next_set):
        while diff > 0:
            self.move_to_next_set(iter(curr_set), curr_set, next_set)
            diff -= 1
    
    def move_all_to_next_set(self):
        curr_sets = [self.interncoop_set, self.fte_set]
        next_sets = [self.next_sets[self.preference][0], self.next_sets[self.preference][1]]
        for i in range(2):
            while len(curr_sets[i]) > 0:
                self.move_to_next_set(iter(curr_sets[i]), curr_sets[i], next_sets[i])

    def move_to_next_set(self, iterator, curr_set, next_set):
        item = next(iterator, None)
        curr_set.remove(item)
        next_set.add(item)

class People():
    def __init__(self):
        self.num_people = 0
        self.general_set = set()
        self.priority_set_dict = Static().get_set_dict()
        self.regular_set_dict = Static().get_set_dict()
        self.set_dicts = {
            "regular": self.regular_set_dict,
            "priority": self.priority_set_dict
        }

    def add_person(self, person):
        if person.category == "Not Listed/Other" or person.preference == "general":
            self.general_set.add(person)
        else:
            self.set_dicts[person.preference][person.category].add(person)
        self.num_people += 1

class Person():
    def __init__(self, name, email, category, preference, one_thing):
        self.name = name
        self.email = email
        self.category = category
        self.preference = preference 
        self.one_thing = one_thing

class Static():
    def __init__(self):
        self.preference_dict = {
            "Anyone! Put me in the general pool, please": "general",
            "Someone in my category, please": "priority",
            "I'd prefer to get matched with my category but am happy to talk to anyone!": "regular"
        }
        self.category_ls = ["Design", "Product Management (PM)", "Software Engineering/Frontend (SWE)", "Software Engineering/Backend (SWE)"]

    def get_set_dict(self):
        return {
            "Design": set(), 
            "Product Management (PM)": set(), 
            "Software Engineering/Frontend (SWE)": set(), 
            "Software Engineering/Backend (SWE)": set(), 
        }
    def get_create_pairs_dict(self, intern_func, fte_func):
        return {
            "Intern/Co-op": (intern_func, 0),
            "Full Time Employee (FTE)": (fte_func, 1)
        }
    def get_new_doc_header(self, key):
        header_dict = {
            "pairs": ["Intern/Co-op (Sender)", "Full Time Employee (Recipient)"],
            "groups": ["Intern/Co-op 1 (Sender)", "Intern/Co-op 2 (Recipient)", "Full Time Employee (Recipient)"]
        }
        return header_dict[key]
    
        
if __name__ == "__main__":
    original_doc = argv[1]
    group_type = argv[2]
    if not (group_type == "-groups" or group_type == "-pairs"):
        print("Usage: python3 {original document} {group type} [options: -groups, -pairs]")
        exit()
    today = date.today()
    formatted_date = today.strftime("%m-%d-%Y")
    final_doc = "FTE-lunch_pairs-" + formatted_date + ".csv"
    Documents(original_doc, final_doc, group_type).process()