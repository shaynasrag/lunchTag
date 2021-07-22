import pytest
import csv
from lunchTag import Documents, People, Person
    
@pytest.fixture
def valid_Documents():
    return Documents('original_lunchTag.csv', 'final_lunchTag.csv')

@pytest.fixture
def valid_Documents_odd():
    return Documents('original_lunchTag1.csv', 'final_lunchTag.csv')

@pytest.fixture
def valid_People():
    return People()

@pytest.fixture
def valid_Person():
    return Person("test", "test@mail.com")

@pytest.fixture
def valid_Person1():
    return Person("test1", "test1@intuit.com")

@pytest.fixture
def valid_Person2():
    return Person("test2", "test2@intuit.com")

def test_Documents_init(valid_Documents):
    assert hasattr(valid_Documents, "original_doc")
    assert valid_Documents.original_doc == "original_lunchTag.csv"
    assert hasattr(valid_Documents, "final_doc")
    assert valid_Documents.final_doc == "final_lunchTag.csv"
    assert hasattr(valid_Documents, "formatted_rows")
    assert valid_Documents.formatted_rows == []
    assert hasattr(valid_Documents, "people")
    assert isinstance(valid_Documents.people, People)

# def test_Documents_createPairsFromDoc(valid_Documents):
#     valid_Documents.create_pairs_from_doc()
#     assert valid_Documents.people.num_people == 2
#     assert len(valid_Documents.people.individual_list) == 2
#     for person in valid_Documents.people.individual_list:
#         assert isinstance(person, Person)
#         assert (person.name == "test1" or person.name == "test2")
#         assert (person.email == "test1@intuit.com" or person.email == "test2@intuit.com")

# def test_Documents_formatRows(valid_Documents):
#     assert len(valid_Documents.formatted_rows) == 0
#     valid_Documents.create_pairs_from_doc()
#     valid_Documents.format_rows()
#     assert len(valid_Documents.formatted_rows) == 1
#     for row in valid_Documents.formatted_rows:
#         assert (row == ["test1: test1@intuit.com", "test2: test2@intuit.com"] or row == ["test2: test2@intuit.com", "test1: test1@intuit.com"])

# def test_Documents_writeRowsToDocs(valid_Documents):
#     valid_Documents.create_pairs_from_doc()
#     valid_Documents.format_rows()
#     valid_Documents.write_rows_to_doc()
#     doc = valid_Documents.final_doc
#     final_doc_ls = list(csv.reader(open(doc)))
#     assert final_doc_ls[0] == ["Person 1 (Sender)", "Person 2 (Recipient)", "Person 3 (Recipient)"]
#     assert (final_doc_ls[1] == ["test1: test1@intuit.com", "test2: test2@intuit.com"] or final_doc_ls[1] == ["test2: test2@intuit.com", "test1: test1@intuit.com"])

def test_People_init(valid_People):
    assert hasattr(valid_People, "num_people")
    assert valid_People.num_people == 0
    assert hasattr(valid_People, "individual_list")
    assert valid_People.individual_list == []
    assert hasattr(valid_People, "pair_list")
    assert valid_People.pair_list == []

# def test_People_resolveExtraPair(valid_Documents):
#     valid_Documents.people.individual_list.append(valid_Person1)
#     valid_Documents.people.individual_list.append(valid_Person2)
#     valid_Documents.people.num_people = 2
#     extra_pair = valid_Documents.people.resolve_extra_pair()
#     assert extra_pair == None
#     assert len(valid_Documents.people.pair_list) == 0

# def test_People_resolveExtraPairOdd(valid_Documents):
#     valid_Documents.people.individual_list.append(valid_Person)
#     valid_Documents.people.individual_list.append(valid_Person1)
#     valid_Documents.people.individual_list.append(valid_Person2)
#     valid_Documents.people.num_people = 3
#     extra_pair = valid_Documents.people.resolve_extra_pair()
#     assert extra_pair == True
#     assert len(valid_Documents.people.pair_list) == 1

# def test_People_addPairsToList(valid_Documents):
#     assert valid_Documents.people.pair_list == []
#     valid_Documents.create_pairs_from_doc()
    # assert len(valid_Documents.people.pair_list) == 1

def test_Person_init(valid_Person):
    assert hasattr(valid_Person, "name")
    assert valid_Person.name == "test"
    assert hasattr(valid_Person, "email")
    assert valid_Person.email == "test@mail.com"