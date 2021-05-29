from unittest import TestCase
from Family_Tree.person import Person
from Family_Tree.family_tree import FamilyTree
from geektrust import Geektrust
from Family_Tree import constants


class TestGeektrust(TestCase):

    def setUp(self):
        self.geektrust_app = Geektrust()
    
    def test_add_member_call(self):
        # check error case
        self.geektrust_app.add_member_call(("wrong", "input", "count"))

        # check whether add_member_call returns a call for add_member method
        self.assertEqual(self.geektrust_app.add_member_call('name', 'gender'), "self.family_tree.add_member('name', 'gender')")

    def test_add_spouse_call(self):
        # check error case
        self.geektrust_app.add_spouse_call(("input", "count", "not", "right"))

        # check whether add_spouse_call returns a call for add_spouse method
        self.assertEqual(self.geektrust_app.add_spouse_call('name', 'spouse_name', 'spouse_gender'), "self.family_tree.add_spouse('name', 'spouse_name', 'spouse_gender')")

    def test_add_child_call(self):
        # check error case
        self.geektrust_app.add_member_call(("input", "count", "not", "right"))

        # check whether add_child_call returns a call for add_child method
        self.assertEqual(self.geektrust_app.add_child_call('mother_name', 'child_name', 'child_gender'), "self.family_tree.add_child('mother_name', 'child_name', 'child_gender')")

    def test_get_relatives_call(self):
        # check error case
        self.geektrust_app.add_member_call(("wrong", "input", "count"))

        # check whether get_relatives_call returns a call for get_relatives method
        self.assertEqual(self.geektrust_app.get_relatives_call('person_name', 'relation'), "self.family_tree.get_relatives('person_name', 'relation')")

    def test_readfile(self):
        # check readfile function
        self.assertEqual(self.geektrust_app.readfile('./tests/test_files/test_readfile.txt'), ['ADD_MEMBER SHAN MALE'])

    def test_get_tokens(self):
        # check if get_tokens split instructions by space
        self.assertEqual(self.geektrust_app.get_tokens("SPLIT THIS INSTRUCTION"), ('SPLIT', 'THIS', 'INSTRUCTION'))

    def test_get_method(self):
        # check error case
        self.assertRaises(ValueError, self.geektrust_app.get_method, 'add_member', 'name', 'gender')

        # check if get_method returns the right method call
        self.assertEqual(self.geektrust_app.get_method(*tuple(['ADD_MEMBER', 'name', 'gender'])), self.geektrust_app.add_member_call('name', 'gender'))

    def test_translate(self):
        # check for invalid instruction
        self.assertRaises(ValueError, self.geektrust_app.translate, './tests/test_files/test_translate_exception.txt')

        # check if translate successfully translates user instructions into corresponding method calls
        self.assertEqual(self.geektrust_app.translate('./tests/test_files/test_readfile.txt'), ["self.family_tree.add_member('SHAN', 'MALE')"])

    def test_execute(self):
        # check if execute can run a list of method calls
        self.assertEqual(self.geektrust_app.execute(["str.upper('uppercase')", "str.lower('LOWERCASE')"]), ['UPPERCASE', 'lowercase'])

    def test_get_names(self):
        person_a = Person("A", constants.FEMALE)
        person_b = Person("B", constants.MALE)

        # check if get_names returns names of all Person objects in a list
        self.assertEqual(self.geektrust_app.get_names([None, person_b]), ["B"])

    def test_format_names(self):
        # check if format_names returns list of str objects separated by space and sorted by alphabet
        self.assertEqual(self.geektrust_app.format_names(["space", "between", "each", "word"]), "between each space word")

    def test_str_input_for_format_result(self):
        # check if str inputs are kept as is in a list
        self.assertEqual(self.geektrust_app.format_result(["These", "are", "the", "same"]), ["These", "are", "the", "same"])
