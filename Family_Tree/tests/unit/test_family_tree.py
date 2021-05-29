from unittest import TestCase
from Family_Tree.person import Person
from Family_Tree.family_tree import FamilyTree
from Family_Tree import constants


class TestFamilyTree(TestCase):

    def setUp(self):
        self.family_tree = FamilyTree()
        self.family_tree.family_tree = {
            'Father': Person("Father", constants.MALE),
        }

    def test_initialization(self):
        # check instance
        self.assertIsInstance(self.family_tree, FamilyTree)

    def test_add_member(self):
        # check exception
        self.assertRaises(ValueError, self.family_tree.add_member, "Father", constants.MALE)

        # add new person
        added_member = self.family_tree.add_member("Added_Member", constants.FEMALE)

        # check if added member is returned
        self.assertEqual(added_member.name, "Added_Member")

        # check if member is added to family tree
        self.assertIs(self.family_tree.family_tree.get("Added_Member"), added_member)

    def test_add_spouse(self):
        # check exception
        self.assertRaises(ValueError, self.family_tree.add_spouse, "Wrong_Person", "Spouse", constants.FEMALE)

        # check if spouse addition is successful
        self.assertEqual(self.family_tree.add_spouse("Father", "Mother", constants.FEMALE), constants.SPOUSE_ADDITION_SUCCEEDED)

        # check duplicate spouse condition
        self.assertEqual(self.family_tree.add_spouse("Father", "Mother", constants.FEMALE), constants.SPOUSE_ADDITION_FAILED)

    def test_add_child_errors(self):
        # check invalid mother input
        self.assertEqual(self.family_tree.add_child("Mother", "Child", constants.FEMALE), constants.PERSON_NOT_FOUND)

        # add mother to tree
        self.family_tree.add_spouse("Father", "Mother", constants.FEMALE)

        # check for calling on Male 
        self.assertEqual(self.family_tree.add_child("Father", "Child", constants.FEMALE), constants.CHILD_ADDITION_FAILED)

        # check for adding child to mother without spouse
        self.family_tree.add_member("Mother_Without_Spouse", constants.FEMALE)
        self.assertEqual(self.family_tree.add_child("Mother_Without_Spouse", "Child", constants.FEMALE), constants.CHILD_ADDITION_FAILED)

        # check for child name already in family tree
        self.assertEqual(self.family_tree.add_child("Mother", "Mother_Without_Spouse", constants.FEMALE), constants.CHILD_ADDITION_FAILED)

    def test_add_child(self):
        # add mother to tree
        self.family_tree.add_spouse("Father", "Mother", constants.FEMALE)

        # check add child to mother
        self.assertEqual(self.family_tree.add_child("Mother", "Child", constants.FEMALE), constants.CHILD_ADDITION_SUCCEEDED)

    def test_get_relatives_error(self):
        # check for person not in tree
        self.assertEqual(self.family_tree.get_relatives("Person", "Paternal-Uncle"), constants.PERSON_NOT_FOUND)

    def test_get_relatives_paternal_aunt(self):
        # create mock family
        self.family_tree.add_spouse("Father", "Mother", constants.FEMALE)
        self.family_tree.add_child("Mother", "Paternal_Aunt", constants.FEMALE)
        self.family_tree.add_child("Mother", "Person", constants.MALE)
        self.family_tree.add_spouse("Person", "Spouse", constants.FEMALE)
        self.family_tree.add_child("Spouse", "Child", constants.FEMALE)

        # test get paternal aunt
        paternal_aunt = self.family_tree.get_relatives("Child", "Paternal-Aunt")
        self.assertEqual(paternal_aunt, [self.family_tree.family_tree.get("Paternal_Aunt")])

    def test_get_relatives_maternal_aunt(self):
        # create mock family
        self.family_tree.add_spouse("Father", "Mother", constants.FEMALE)
        self.family_tree.add_child("Mother", "Maternal_Aunt", constants.FEMALE)
        self.family_tree.add_child("Mother", "Person", constants.FEMALE)
        self.family_tree.add_spouse("Person", "Spouse", constants.MALE)
        self.family_tree.add_child("Person", "Child", constants.FEMALE)

        # test get paternal aunt
        maternal_aunt = self.family_tree.get_relatives("Child", "Maternal-Aunt")
        self.assertEqual(maternal_aunt, [self.family_tree.family_tree.get("Maternal_Aunt")])

    def test_get_relatives_paternal_uncle(self):
        # create mock family
        self.family_tree.add_spouse("Father", "Mother", constants.FEMALE)
        self.family_tree.add_child("Mother", "Paternal_Uncle", constants.MALE)
        self.family_tree.add_child("Mother", "Person", constants.MALE)
        self.family_tree.add_spouse("Person", "Spouse", constants.FEMALE)
        self.family_tree.add_child("Spouse", "Child", constants.FEMALE)

        # test get paternal aunt
        paternal_uncle = self.family_tree.get_relatives("Child", "Paternal-Uncle")
        self.assertEqual(paternal_uncle, [self.family_tree.family_tree.get("Paternal_Uncle")])

    def test_get_relatives_maternal_uncle(self):
        # create mock family
        self.family_tree.add_spouse("Father", "Mother", constants.FEMALE)
        self.family_tree.add_child("Mother", "Maternal_Uncle", constants.MALE)
        self.family_tree.add_child("Mother", "Person", constants.FEMALE)
        self.family_tree.add_spouse("Person", "Spouse", constants.MALE)
        self.family_tree.add_child("Person", "Child", constants.FEMALE)

        # test get paternal aunt
        maternal_uncle = self.family_tree.get_relatives("Child", "Maternal-Uncle")
        self.assertEqual(maternal_uncle, [self.family_tree.family_tree.get("Maternal_Uncle")])
