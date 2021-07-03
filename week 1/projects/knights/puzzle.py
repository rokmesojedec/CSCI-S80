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
knowledge0.add(Implication(AKnight, And(AKnight, AKnave)))

# XOR Each Character can either be a Knight or Knave, but not both
knowledge0.add(And(Or(AKnave,AKnight), Not(And(AKnave,AKnight))))

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And()
knowledge1.add(Implication(AKnight, And(BKnave, AKnave)))
knowledge1.add(Implication(AKnave, Not(And(BKnave, AKnave))))

# XOR Each Character can either be a Knight or Knave, but not both
knowledge1.add(And(Or(AKnave,AKnight), Not(And(AKnave,AKnight))))
knowledge1.add(And(Or(BKnave,BKnight), Not(And(BKnave,BKnight))))

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And()
knowledge2.add(Implication(AKnight, Or(And(AKnight, BKnight),And(AKnave, BKnave))))
knowledge2.add(Implication(AKnight, Or(Not(And(AKnight, BKnight)),Not(And(AKnave, BKnave)))))

knowledge2.add(Implication(BKnight, And(BKnight, AKnave)))
knowledge2.add(Implication(BKnave, Not(And(BKnave, AKnave))))

# XOR Each Character can either be a Knight or Knave, but not both
knowledge2.add(And(Or(AKnave,AKnight), Not(And(AKnave,AKnight))))
knowledge2.add(And(Or(BKnave,BKnight), Not(And(BKnave,BKnight))))

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And()
knowledge3.add(Implication(AKnight, Or(AKnave, AKnight)))
knowledge3.add(Implication(AKnave, Not(Or(AKnave, AKnight))))

knowledge3.add(Implication(BKnight, Implication(AKnight, AKnave)))
knowledge3.add(Implication(BKnight, CKnave))
knowledge3.add(Implication(BKnave, Not(CKnave)))
knowledge3.add(Implication(CKnight, AKnight))
knowledge3.add(Implication(CKnave, Not(AKnight)))

# XOR Each Character can either be a Knight or Knave, but not both
knowledge3.add(And(Or(AKnave,AKnight), Not(And(AKnave,AKnight))))
knowledge3.add(And(Or(BKnave,BKnight), Not(And(BKnave,BKnight))))
knowledge3.add(And(Or(CKnave,CKnight), Not(And(CKnave,CKnight))))

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
