from unittest import TestCase
from Family_Tree.person import Person
from Family_Tree.family_tree import FamilyTree
from geektrust import Geektrust
from Family_Tree import constants


class TestIntegration(TestCase):

    def setUp(self):
        self.geektrust_app = Geektrust()

    def test_invalid_input_throws_exception(self):
        # check if exception is thrown for invalid input
        self.assertRaises(ValueError, self.geektrust_app.run, './tests/test_files/test_translate_exception.txt')

    def test_run_for_add_member(self):
        # check if run adds member from input file
        added_person = self.geektrust_app.get_names(self.geektrust_app.run('./tests/test_files/test_add_member.txt'))
        self.assertEqual(added_person, ['TEST'])

        # check if adding person with same name throws exception
        self.assertRaises(ValueError, self.geektrust_app.run, './tests/test_files/test_add_member.txt')

    def test_run_for_add_spouse(self):
        # check if run adds spouse from input file
        results = self.geektrust_app.run('./tests/test_files/test_add_spouse.txt')

        self.assertEqual(results[1:], ["SPOUSE_ADDITION_FAILED", "SPOUSE_ADDITION_FAILED", "SPOUSE_ADDITION_SUCCEEDED"])

    def test_run_for_add_child(self):
        # check if run adds child from input file
        results = self.geektrust_app.run('./tests/test_files/test_add_child.txt')
        self.assertEqual(results[3:], ['PERSON_NOT_FOUND', 'CHILD_ADDITION_FAILED', 'CHILD_ADDITION_FAILED', 'CHILD_ADDITION_FAILED', 'CHILD_ADDITION_SUCCEEDED'])

    def test_run_for_get_relationships(self):
        # set up family tree
        self.geektrust_app.run('./initiation.txt')

        # check for all relationship types
        results = self.geektrust_app.run('./tests/test_files/test_get_relationships.txt')
        formatted_results = self.geektrust_app.format_result(results)
        self.assertEqual(formatted_results, ['Vyas', 'Ahit', 'Satya', 'Vyas', 'Krpi', 'Chika Vila', 'Ahit', 'Chit Ish Satya Vich', 'PERSON_NOT_FOUND'])
    