from unittest import TestCase
from Family_Tree.person import Person
from Family_Tree import constants


class TestPerson(TestCase):

    def setUp(self):
        self.person = Person("Person", constants.MALE)
        self.mother = Person("Mother", constants.FEMALE)
        self.father = Person("Father", constants.MALE)
        self.brother = Person("Brother", constants.MALE)
        self.sister = Person("Sister", constants.FEMALE)
        self.maternal_aunt = Person("Maternal-Aunt", constants.FEMALE)
        self.spouse = Person("Spouse", constants.FEMALE)
        self.child = Person("Child", constants.FEMALE)
        self.brother_spouse = Person("Brother-Spouse", constants.FEMALE)
        self.sister_spouse = Person("Sister-Spouse", constants.MALE)
        self.sister_child = Person("Sister-Child", constants.FEMALE)

    def test_initialization(self):
        # check instance
        self.assertIsInstance(self.person, Person, "Not a Person")

        # check properties
        self.assertEqual(self.person.name, "Person")
        self.assertEqual(self.person.gender, constants.MALE)
        self.assertEqual(self.person.mother, None)
        self.assertEqual(self.person.father, None)
        self.assertEqual(self.person.spouse, None)
        self.assertEqual(self.person.children, [])

        # edge case for gender
        self.assertRaises(ValueError, Person, "OtherPerson", "Queer")

    def test_set_spouse(self):
        # check error case
        self.assertRaises(ValueError, self.person.set_spouse, self.person)

        # run set_spouse
        self.person.set_spouse(self.spouse)

        # check if succeeded
        self.assertIs(self.person.spouse, self.spouse)
        self.assertIs(self.spouse.spouse, self.person)

    def test_set_parents(self):
        # create mock parents
        self.mother.set_spouse(self.father)

        # run set_parents
        self.person.set_parents(self.mother)

        # check if succeeded
        self.assertIs(self.person.mother, self.mother)
        self.assertIs(self.person.father, self.father)

    def test_add_child(self):
        # set spouse
        self.person.set_spouse(self.spouse)

        # check error case
        self.assertRaises(ValueError, self.person.add_child, self.child)

        # run add_child
        self.spouse.add_child(self.child)

        # check if child assigned to both parents
        self.assertEqual(self.person.children, [self.child])
        self.assertEqual(self.spouse.children, [self.child])

        # check if parents assigned to child
        self.assertIs(self.child.father, self.person)
        self.assertIs(self.child.mother, self.spouse)

    def test_get_children(self):
        # set mother and father
        self.mother.set_spouse(self.father)

        # add a son and daughter
        self.mother.add_child(self.person)
        self.mother.add_child(self.sister)

        # check if get_son_daughter works to get all children with BOTH
        self.assertEqual(self.mother.get_son_daughter("BOTH"), [self.person, self.sister])

    def test_get_son(self):
        # set mother and father
        self.mother.set_spouse(self.father)

        # add a son and daughter
        self.mother.add_child(self.person)

        # check if get_son_daughter works to get sons
        self.assertEqual(self.mother.get_son_daughter(constants.MALE), [self.person])

    def test_get_daughter(self):
        # set mother and father
        self.mother.set_spouse(self.father)

        # add daughter
        self.mother.add_child(self.sister)

        # check if get_son_daughter works to get daughters
        self.assertEqual(self.mother.get_son_daughter(constants.FEMALE), [self.sister])

    def test_get_sibings_error_cases(self):
        # check None case
        self.assertIsNone(self.person.get_siblings(constants.MALE))

        # check error case
        self.assertRaises(ValueError, self.person.get_siblings, "wrong_gender")

    def test_get_all_siblings(self):
        # set mother and father as parents
        self.mother.set_spouse(self.father)
        self.mother.add_child(self.person)

        # add a brother and a sister
        self.mother.add_child(self.brother)
        self.mother.add_child(self.sister)

        # check if get_siblings works with BOTH
        self.assertEqual(self.person.get_siblings("BOTH"), [self.brother, self.sister])

    def test_get_brother(self):
        # set mother and father as parents
        self.mother.set_spouse(self.father)
        self.mother.add_child(self.person)

        # add a brother
        self.mother.add_child(self.brother)

        # check if get_siblings works to get brother(s)
        self.assertEqual(self.person.get_siblings(constants.MALE), [self.brother])

    def test_get_sister(self):
        # set mother and father as parents
        self.mother.set_spouse(self.father)
        self.mother.add_child(self.person)

        # add a brother
        self.mother.add_child(self.sister)

        # check if get_siblings works to get sister(s)
        self.assertEqual(self.person.get_siblings(constants.FEMALE), [self.sister])

    def test_get_pibling_error_cases(self):
        # check for wrong relation input
        self.assertRaises(ValueError, self.person.get_pibling, "Wrong-Relation")

        # check for no parent case
        self.assertIsNone(self.person.get_pibling("Paternal-Uncle"))

    def test_get_paternal_uncle(self):
        # create mock family
        self.mother.set_spouse(self.father)
        self.mother.add_child(self.person)
        self.mother.add_child(self.brother)
        self.person.set_spouse(self.spouse)
        self.spouse.add_child(self.child)

        # check if get_pibling works to get Paternal-Uncle(s)
        self.assertEqual(self.child.get_pibling("Paternal-Uncle"), [self.brother])

    def test_get_paternal_aunt(self):
        # create mock family
        self.mother.set_spouse(self.father)
        self.mother.add_child(self.person)
        self.mother.add_child(self.sister)
        self.person.set_spouse(self.spouse)
        self.spouse.add_child(self.child)

        # check if get_pibling works to get Paternal-Aunt(s)
        self.assertEqual(self.child.get_pibling("Paternal-Aunt"), [self.sister])

    def test_get_maternal_uncle(self):
        # create mock family
        self.mother.set_spouse(self.father)
        self.mother.add_child(self.person)
        self.mother.add_child(self.sister)
        self.sister.set_spouse(self.sister_spouse)
        self.sister.add_child(self.child)

        # check if get_pibling works to get Maternal-Uncle(s)
        self.assertEqual(self.child.get_pibling("Maternal-Uncle"), [self.person])

    def test_get_maternal_aunt(self):
        # create mock family
        self.mother.set_spouse(self.father)
        self.mother.add_child(self.maternal_aunt)
        self.mother.add_child(self.sister)
        self.sister.set_spouse(self.sister_spouse)
        self.sister.add_child(self.child)

        # check if get_pibling works to get Maternal-Aunt(s)
        self.assertEqual(self.child.get_pibling("Maternal-Aunt"), [self.maternal_aunt])

    def test_get_sibling_spouses(self):
        # create mock family
        self.mother.set_spouse(self.father)
        self.mother.add_child(self.person)
        self.mother.add_child(self.sister)
        self.mother.add_child(self.brother)
        self.sister.set_spouse(self.sister_spouse)
        self.brother.set_spouse(self.brother_spouse)

        # check get_sibling_spouses for both gender inputs
        self.assertEqual(self.person.get_sibling_spouses(constants.FEMALE), [self.sister_spouse])
        self.assertEqual(self.person.get_sibling_spouses(constants.MALE), [self.brother_spouse])

    def test_get_spouse_siblings(self):
        # create mock family
        self.mother.set_spouse(self.father)
        self.mother.add_child(self.person)
        self.person.set_spouse(self.spouse)
        self.mother.add_child(self.sister)
        self.sister.set_spouse(self.sister_spouse)

        # check get_spouse_siblings for both gender inputs
        self.assertEqual(self.sister_spouse.get_spouse_siblings(constants.MALE), [self.person])
        self.assertEqual(self.spouse.get_spouse_siblings(constants.FEMALE), [self.sister])

    def test_get_sister_in_law(self):
        # create mock family
        self.mother.set_spouse(self.father)
        self.mother.add_child(self.sister)
        self.mother.add_child(self.brother)
        self.brother.set_spouse(self.brother_spouse)

        # check for None case
        self.assertIsNone(self.mother.get_sister_in_law())

        # check for brother's spouses
        self.assertEqual(self.sister.get_sister_in_law(), [self.brother_spouse])

        # check for spouse's sisters
        self.assertEqual(self.brother_spouse.get_sister_in_law(), [self.sister])

    def test_get_brother_in_law(self):
        # create mock family
        self.mother.set_spouse(self.father)
        self.mother.add_child(self.sister)
        self.sister.set_spouse(self.sister_spouse)
        self.mother.add_child(self.brother)

        # check for None case
        self.assertIsNone(self.mother.get_brother_in_law())

        # check for sister's spouses
        self.assertEqual(self.brother.get_brother_in_law(), [self.sister_spouse])

        # check for spouse's brothers
        self.assertEqual(self.sister_spouse.get_brother_in_law(), [self.brother])
