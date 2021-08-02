import sys
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # for each variable
        # remove any domain value that is not of length
        # specified by variable
        for variable in self.crossword.variables:
            values_to_remove = set()
            for value in self.domains[variable]:
                if len(value) != variable.length:
                    values_to_remove.add(value)
            self.domains[variable] = self.domains[variable].difference(
                values_to_remove)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revision_made = False
        x_domain = self.domains[x]
        y_domain = self.domains[y]
        overlap = self.crossword.overlaps[(x, y)]
        values_to_remove = set()

        # find values from var x domain that
        # do not have overlapping values in y domain
        for x_value in x_domain:
            has_overlap = False
            for y_value in y_domain:
                if x_value[overlap[0]] == y_value[overlap[1]]:
                    has_overlap = True
                    break
            if has_overlap is False:
                revision_made = True
                values_to_remove.add(x_value)

        # remove values without overlaps from x's domain
        self.domains[x] = self.domains[x].difference(values_to_remove)
        return revision_made

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # if arcs is not passed as a parameter
        # find all overlapping variables and store them in arcs
        if arcs is None:
            arcs = []
            for overlap in self.crossword.overlaps:
                if self.crossword.overlaps[overlap] is not None:
                    arcs.append(overlap)

        while len(arcs):
            arc = arcs.pop(0)
            x = arc[0]
            y = arc[1]
            if self.revise(x, y):
                # if there are any domains with no values, return False
                if len(self.domains[arc[0]]) == 0:
                    return False
                # get all neighbors which are not variable 'y'
                neighbors = self.crossword.neighbors(x).difference({y})
                for z in neighbors:
                    arcs.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # if a variable is not in assignment then assignment is not complete
        for variable in self.crossword.variables:
            if variable not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # finding duplicates in assignments
        # dict duplicates source:
        # https://www.geeksforgeeks.org/python-find-keys-with-duplicate-values-in-dictionary/

        rev_dict = {}

        for key, value in assignment.items():
            rev_dict.setdefault(value, set()).add(key)
        dupes = [key for key, values in rev_dict.items()
                 if len(values) > 1]

        # Return false if there are duplicate items
        if len(dupes) > 0:
            return False

        for variable in assignment:
            # Check if assignment fulfils the length constraint
            if len(assignment[variable]) != variable.length:
                return False

            neighbors = self.crossword.neighbors(variable)

            # Check if there are conflicts with neighbors
            for neighbor in neighbors:
                if neighbor in assignment:
                    overlap = self.crossword.overlaps[(variable, neighbor)]
                    if assignment[variable][overlap[0]] \
                            != assignment[neighbor][overlap[1]]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        neighbors = set()

        # Exclude neigbors that are not in assignment
        for neighbor in self.crossword.neighbors(var):
            if neighbor not in assignment:
                neighbors.add(neighbor)

        domain_ranks = {}

        # rank domain values according to how many values
        # they rule out in neighbors
        for var_value in self.domains[var]:
            rule_out_count = 0
            for neighbor in neighbors:
                overlap = self.crossword.overlaps[(var, neighbor)]
                neighbor_domains = self.domains[neighbor]
                for neighbor_value in neighbor_domains:
                    if var_value[overlap[0]] != neighbor_value[overlap[1]]:
                        rule_out_count += 1
            domain_ranks[var_value] = rule_out_count

        # sort the domains according to rule out rank
        # dict sort source:
        # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
        domain_ranks = dict(
            sorted(
                domain_ranks.items(),
                key=lambda item: item[1]))

        # return keys of dictionary as a list
        return [*domain_ranks]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        unassigned_variable = None
        for variable in self.crossword.variables:

            # Skip variable that's already in assignment
            if variable in assignment:
                continue
            if unassigned_variable is None:
                unassigned_variable = variable

            # select variable with fewer values in its domain
            elif len(self.domains[unassigned_variable]) > \
                    len(self.domains[variable]):
                unassigned_variable = variable

            # if there are more than one variables with lowest
            # domain value, select variable whith highest degree
            elif len(self.domains[unassigned_variable]) == \
                    len(self.domains[variable]) \
                    and len(self.crossword.neighbors(variable)) > \
                    len(self.crossword.neighbors(unassigned_variable)):
                unassigned_variable = variable
        return unassigned_variable

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # Backtrack is based on Queens.py shown
        # Chris Sorenson's section

        # check if we've solved the crossword
        if self.assignment_complete(assignment):
            return assignment

        # get next variable to fill
        unassigned = self.select_unassigned_variable(assignment)

        # try all values in variable's domain
        for value in self.order_domain_values(unassigned, assignment):
            assignment[unassigned] = value

            # if value is not consistent, remove it
            # and try another
            if not self.consistent(assignment):
                del assignment[unassigned]
                continue

            # if value is consistent
            # try filling out another variable
            result = self.backtrack(assignment)

            if result:
                return result

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
