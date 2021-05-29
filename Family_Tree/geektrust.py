import sys
from Family_Tree.family_tree import FamilyTree
from Family_Tree.person import Person
from Family_Tree import constants


class Geektrust:

    def __init__(self):
        self.family_tree = FamilyTree()

    def add_member_call(self, *args):
        # create call for adding new member
        if len(args) != 2:
            return None

        return f"self.family_tree.add_member('{args[0]}', '{args[1]}')"

    def add_spouse_call(self, *args):
        # create call for adding a spouse
        if len(args) != 3:
            return None

        return f"self.family_tree.add_spouse('{args[0]}', '{args[1]}', '{args[2]}')"

    def add_child_call(self, *args):
        # create call for ADD_CHILD
        if len(args) != 3:
            return None

        return f"self.family_tree.add_child('{args[0]}', '{args[1]}', '{args[2]}')"

    def get_relatives_call(self, *args):
        # create call for GET_RELATIONSHIP
        if len(args) != 2:
            return None

        return f"self.family_tree.get_relatives('{args[0]}', '{args[1]}')"

    def readfile(self, filename):
        # get instructions from input file
        with open(filename, 'r') as fr:
            return fr.readlines()

    def get_tokens(self, instruction):
        # split user instruction into appropriate tokens
        return tuple(instruction.strip().split(" "))

    def get_method(self, *args):
        # get method call based on instruction
        switch_method = {
            "ADD_MEMBER": self.add_member_call,
            "ADD_SPOUSE": self.add_spouse_call,
            "ADD_CHILD": self.add_child_call,
            "GET_RELATIONSHIP": self.get_relatives_call
        }

        method_call = switch_method.get(args[0])

        if not method_call:
            raise ValueError("Invalid Instruction")

        return method_call(*tuple(args[1:]))

    def translate(self, filename):
        # translate instructions from input file

        results = []
        instructions = self.readfile(filename)

        for instruction in instructions:
            tokens = self.get_tokens(instruction)
            result = self.get_method(*tokens)

            if not result:
                continue

            results.append(result)

        return results

    def execute(self, instructions):
        # executes set of method_calls (instructions) in string form
        results = []

        for instruction in instructions:
            result = eval(instruction)

            if not result:
                results.append(constants.NONE)
                continue

            results.append(result)

        return results

    def get_names(self, persons):
        # get names of people
        if not persons:
            return None

        names = []

        for person in persons:
            if isinstance(person, Person):
                names.append(person.name)

        return names

    def format_names(self, names):
        # sort a list of names -> return string with each name separated by space
        return constants.NONE if not names else " ".join(names)

    def format_result(self, results):
        # modify the results to desired output formats
        formatted_results = []

        for result in results:
            if isinstance(result, str):
                formatted_results.append(result)
                continue

            names = self.get_names(result)
            formatted_results.append(self.format_names(names))

        return formatted_results

    def log(self, results):
        # print results
        for result in results:
            print(result)

    def run(self, filename):
        # run instructions from input file
        instructions = self.translate(filename)
        return self.execute(instructions)

    def main(self):
        # initiating the tree
        self.run('./initiation.txt')

        # run program with input file
        filename = sys.argv[1]
        results = self.run(filename)

        # log results
        self.log(self.format_result(results))


if __name__ == "__main__":
    geektrust_app = Geektrust()
    geektrust_app.main()
