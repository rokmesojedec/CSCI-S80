import tictactoe as ttt
EMPTY = None
X = "X"
O = "O"
board = [[X, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, O, EMPTY]]
# user = ttt.player(
#     [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]])
# print(user)


# pa = ttt.actions([[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]])
# print(pa)

# pa = ttt.actions([[EMPTY, X, EMPTY], [EMPTY, EMPTY, X], [EMPTY, EMPTY, X]])
# print(pa)

# pa = ttt.actions([[X, X, X], [X, EMPTY, X], [EMPTY, EMPTY, X]])
# print(pa)

# board2 = ttt.result(board, (2,1))
# result = ttt.result(board2, (0,0))
# result = ttt.result(result, (1,1))
# result = ttt.result(result, (0,2))
# result = ttt.result(result, (1,2))
# result = ttt.result(result, (2,2))
# result = ttt.result(result, (1,0))


#print(result)
test = [[X,X,X],[O,O,O], [EMPTY, X, EMPTY]]
winner = ttt.winner(test)

# print(test)

# print(winner)

print(ttt.minimax(board))