from Family_Tree.person import Person
from Family_Tree import constants


class FamilyTree:

    def __init__(self):

        self.family_tree = {}

    def add_member(self, person_name, person_gender):
        # add new member to tree
        person = Person(person_name, person_gender)

        if not self.family_tree.get(person.name):
            self.family_tree.update({person_name: person})
        else:
            raise ValueError("Person Already Exists")

        return person

    def add_spouse(self, person_name, spouse_name, spouse_gender):
        # add spouse member to tree
        person = self.family_tree.get(person_name)

        if not person:
            raise ValueError(constants.PERSON_NOT_FOUND)

        try:
            spouse = self.add_member(spouse_name, spouse_gender)
        except(ValueError):
            return constants.SPOUSE_ADDITION_FAILED

        try:
            person.set_spouse(spouse)
        except(ValueError):
            self.family_tree.popitem()
            return constants.SPOUSE_ADDITION_FAILED

        return constants.SPOUSE_ADDITION_SUCCEEDED

    def add_child(self, mother_name, child_name, child_gender):
        # add child to tree given a mother's name, child's name and child's gender
        mother = self.family_tree.get(mother_name)

        if not mother:
            return constants.PERSON_NOT_FOUND

        if mother.gender != constants.FEMALE:
            return constants.CHILD_ADDITION_FAILED

        if not mother.spouse:
            return constants.CHILD_ADDITION_FAILED

        try:
            child = self.add_member(child_name, child_gender)
        except(ValueError):
            return constants.CHILD_ADDITION_FAILED

        mother.add_child(child)
        return constants.CHILD_ADDITION_SUCCEEDED

    def get_relatives(self, person_name, relation):
        # get names of relatives given a person's name and the relation to find
        person = self.family_tree.get(person_name)

        if not person:
            return constants.PERSON_NOT_FOUND

        relation_switch = {
            "Paternal-Aunt": 'person.get_pibling(relation)',
            "Maternal-Aunt": 'person.get_pibling(relation)',
            "Paternal-Uncle": 'person.get_pibling(relation)',
            "Maternal-Uncle": 'person.get_pibling(relation)',
            "Sister-In-Law": 'person.get_sister_in_law()',
            "Brother-In-Law": 'person.get_brother_in_law()',
            "Son": 'person.get_son_daughter(constants.MALE)',
            "Daughter": 'person.get_son_daughter(constants.FEMALE)',
            "Siblings": 'person.get_siblings("BOTH")',
            "Grandfather": 'person.get_grandparent(constants.MALE)',
            "Grandmother": 'person.get_grandparent(constants.FEMALE)'
        }

        return eval(relation_switch.get(relation))
