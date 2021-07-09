from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And()

# If A is a Knight, then A is both a Knave and a Knight
knowledge0.add(Implication(AKnight, And(AKnight, AKnave)))

# If A is a Knave, then A can't be both a Knave and a Knight
knowledge0.add(Implication(AKnave, Not(And(AKnight, AKnave))))

# XOR Each Character can either be a Knight or Knave, but not both
knowledge0.add(And(Or(AKnave, AKnight), Not(And(AKnave, AKnight))))

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And()

# If A is a Knight, then both A and B are Knaves
knowledge1.add(Implication(AKnight, And(BKnave, AKnave)))

# If A is a Knave, then both A and B are not Knaves
knowledge1.add(Implication(AKnave, Not(And(BKnave, AKnave))))

# XOR Each Character can either be a Knight or Knave, but not both
knowledge1.add(And(Or(AKnave, AKnight), Not(And(AKnave, AKnight))))
knowledge1.add(And(Or(BKnave, BKnight), Not(And(BKnave, BKnight))))

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And()

# If A is a knight, then either A & B are knights or A & B are knaves
knowledge2.add(Implication(AKnight, Or(
    And(AKnight, BKnight), And(AKnave, BKnave))))

# If A is a knave, then either A & B are not knights or A & B are not knaves
knowledge2.add(Implication(AKnight, Or(
    Not(And(AKnight, BKnight)), Not(And(AKnave, BKnave)))))

# If B is a knight, then B is knight and A is knave
knowledge2.add(Implication(BKnight, And(BKnight, AKnave)))

# If B is a knave, then it is not true that B is knight and A is knave
knowledge2.add(Implication(BKnave, Not(And(BKnave, AKnave))))

# XOR Each Character can either be a Knight or Knave, but not both
knowledge2.add(And(Or(AKnave, AKnight), Not(And(AKnave, AKnight))))
knowledge2.add(And(Or(BKnave, BKnight), Not(And(BKnave, BKnight))))

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And()

# If A says the truth and is either a knight or a knave, then A is Knight
knowledge3.add(Implication(AKnight, Or(AKnave, AKnight)))

# If A lies and is not a knight or a knave, then A is a Knave
knowledge3.add(Implication(AKnave, Not(Or(AKnave, AKnight))))

# If B is a knight, then it is true
# that A is a knight and A said that I am a Knave
knowledge3.add(Implication(BKnight, Or(Implication(
    AKnight, AKnave), Implication(AKnave, AKnave))))

# If B is a knight, then C is a knave
knowledge3.add(Implication(BKnight, CKnave))

# if B is lying, then C is not a knave
knowledge3.add(Implication(BKnave, Not(CKnave)))

# If C is a knight, then A is a knight
knowledge3.add(Implication(CKnight, AKnight))

# If C is a knave, then A is not a AKnight
knowledge3.add(Implication(CKnave, Not(AKnight)))

# XOR Each Character can either be a Knight or Knave, but not both
knowledge3.add(And(Or(AKnave, AKnight), Not(And(AKnave, AKnight))))
knowledge3.add(And(Or(BKnave, BKnight), Not(And(BKnave, BKnight))))
knowledge3.add(And(Or(CKnave, CKnight), Not(And(CKnave, CKnight))))


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
