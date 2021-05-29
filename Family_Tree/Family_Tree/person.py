from Family_Tree import constants


class Person:

    def __init__(self, name, gender):

        self.name = name
        self.set_gender(gender)
        self.mother = None
        self.father = None
        self.spouse = None
        self.children = []

    def set_gender(self, gender):
        # set gender for person
        if gender in (constants.MALE, constants.FEMALE):
            self.gender = gender
        else:
            raise ValueError("GENDER INPUT FAILED")

    def set_spouse(self, spouse):
        # sets spouse
        if self.gender == spouse.gender:
            raise ValueError("Spouse Gender Mismatch")

        self.spouse = spouse
        spouse.spouse = self

    def set_parents(self, mother):
        # set parents for new child
        if not mother.spouse:
            raise ValueError("Invalid Parents")

        self.mother = mother
        self.father = mother.spouse

    def add_child(self, child):
        # add's a child
        if self.gender != constants.FEMALE:
            raise ValueError("Invalid Input for Mother")

        spouse = self.spouse

        self.children.append(child)
        spouse.children.append(child)
        child.set_parents(self)

    def get_son_daughter(self, gender):
        # get sons/daughters based on gender input
        children = self.children

        if not children:
            return None

        if gender not in (constants.MALE, constants.FEMALE, 'BOTH'):
            raise ValueError("Gender Value Mismatch")

        if gender == "BOTH":
            return children
        else:
            return list(filter(lambda x: x.gender == gender, children))

    def get_siblings(self, gender):
        # get siblings based on gender input; takes "BOTH" as input for all siblings
        if gender not in (constants.MALE, constants.FEMALE, 'BOTH'):
            raise ValueError("Gender Value Mismatch")

        if not self.mother:
            return None

        other_children = list(filter(lambda x: x != self, self.mother.children))

        if gender == "BOTH":
            return other_children
        else:
            return list(filter(lambda x: x.gender == gender, other_children))

    def get_pibling(self, relation):
        # get parent's siblings based on the specific relation
        piblings = ('Paternal-Uncle', 'Paternal-Aunt', 'Maternal-Uncle', 'Maternal-Aunt')

        if relation not in piblings:
            raise ValueError("Relation Input Mismatch")

        tokens = relation.split("-")
        parent = self.father if tokens[0] == "Paternal" else self.mother

        if not parent:
            return None

        if tokens[1] == "Uncle":
            return parent.get_siblings(constants.MALE)
        else:
            return parent.get_siblings(constants.FEMALE)

    def get_sibling_spouses(self, siblings_gender):
        # get sibling spouses based on siblings gender
        siblings = self.get_siblings(siblings_gender)
        sibling_spouses = []

        if siblings:
            for sibling in siblings:
                sibling_spouses.append(sibling.spouse)

        return list(filter(lambda x: x is not None, sibling_spouses))

    def get_spouse_siblings(self, siblings_gender):
        # get spouse siblings based on siblings gender
        if not self.spouse:
            return []

        return self.spouse.get_siblings(siblings_gender)

    def get_sister_in_law(self):
        # get sister-in-laws
        brothers_spouses = self.get_sibling_spouses(constants.MALE)
        spouse_sisters = self.get_spouse_siblings(constants.FEMALE)

        return brothers_spouses if brothers_spouses else spouse_sisters

    def get_brother_in_law(self):
        # get brother-in-laws
        sisters_spouses = self.get_sibling_spouses(constants.FEMALE)
        spouse_brothers = self.get_spouse_siblings(constants.MALE)

        return sisters_spouses if sisters_spouses else spouse_brothers

    def get_parent(self, gender):
        # get parent based on the gender input

        if gender == constants.MALE:
            return self.father
        else:
            return self.mother

    def get_grandparent(self, gender):
        # get grandparents
        mother = self.get_parent(constants.FEMALE)
        father = self.get_parent(constants.MALE)

        grandparents = []
        
        grandparents.append(mother.get_parent(gender))
        grandparents.append(father.get_parent(gender))

        return grandparents
