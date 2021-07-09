import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # if number of cells in sentence is equal to count
        # this means that all cells are mines
        # if not, we don't know which cells are mines
        if len(self.cells) == self.count and self.count > 0:
            return self.cells
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if count is equal to 0, then all cells are safe
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # if cell is in sentence's set
        # remove the cell from sentence's cell set and reduce count
        # because that cell won't count towards the sentence count
        if cell in self.cells:
            self.count -= 1
            self.cells.remove(cell)

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # if cell is in sentence's set
        # remove it from cell set
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def get_neighbor_cells(self, cell):
        """
        Gets neigboring cells which are on the board
        and have not been visited yet
        """
        neigbors = set()
        # Loop through all neigboring cells of passed cell
        for i in range(cell[0]-1, cell[0]+2):
            for j in range(cell[1]-1, cell[1]+2):
                tempCell = (i, j)
                # ignore cells which fall off the board
                # ignore cells which are current cell
                # ignore cells which are in moves_made set
                if i > -1 and i < self.height and \
                        j > -1 and j < self.width and \
                        not (i == cell[0] and j == cell[1]) and \
                        tempCell not in self.moves_made:
                    neigbors.add(tempCell)
        return neigbors

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        # Add cell to mines set
        self.mines.add(cell)

        # Update sentences in knowledge that the cell is a mine
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        # add cell to safe cells set
        self.safes.add(cell)
        # mark cell safe in all sentences
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def reassess_knowledge(self):
        """
        Draws inferences from newly added knowledge
        """

        # compare each sentence with every senctence in knolwedge base
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                # if a sentence is a subset of another sentence
                if sentence2 != sentence1 and \
                   sentence2.cells.issubset(sentence1.cells):
                    # reduce the mine count in superset by subset count
                    sentence1.count -= sentence2.count
                    # remove the cells of subset from super set
                    sentence1.cells = sentence1.cells.difference(
                        sentence2.cells)

        # mark any newly discovered mines or safes
        for sentence in self.knowledge:
            safes = sentence.known_safes()
            mines = sentence.known_mines()

            unmarked_mines = set()
            unmarked_safes = set()

            # Find any safe cells which are not
            # in global safe cells set
            if safes is not None:
                for safe in safes:
                    if safe not in self.safes:
                        unmarked_safes.add(safe)

            # Find any mines cells which are not
            # in global mines cells set
            if mines is not None:
                for mine in mines:
                    if mine not in self.mines:
                        unmarked_mines.add(mine)

            # mark all safe cells a safe - update knowledge
            for unmarked_safe in unmarked_safes:
                self.mark_safe(unmarked_safe)

            # mark all mine cells as mines - update knowledge
            for unmarked_mine in unmarked_mines:
                self.mark_mine(unmarked_mine)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Add selected cell to moves made
        self.moves_made.add(cell)

        # Mark that cell safe - update knowledge
        self.mark_safe(cell)

        # Create sentence from new information gained from newly added cell
        self.knowledge.append(Sentence(self.get_neighbor_cells(cell), count))

        # Make inferences from new knowledge
        self.reassess_knowledge()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # get cells which are marked safe
        # and are not in moves made or mines set
        safes = self.safes.difference(self.moves_made).difference(self.mines)

        # pick the first element from set of possible safe moves
        if len(safes) > 0:
            iterator = iter(safes)
            cell = next(iterator, None)
            print("Making AI move: ", cell)
            return cell

        # if no possible safe moves exist return None
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = set()

        # create a set of possible random moves
        # any cell is possible that is not in mine or moves_made set
        for i in range(0, self.height):
            for j in range(0, self.width):
                cell = (i, j)
                if cell not in self.mines and cell not in self.moves_made:
                    possible_moves.add(cell)

        # if possible moves are 0 then return None
        if len(possible_moves) == 0:
            return None

        # otherwise pick a random possible move
        cell = random.sample(possible_moves, 1)[0]
        print("Making Random move: ", cell)
        return cell
