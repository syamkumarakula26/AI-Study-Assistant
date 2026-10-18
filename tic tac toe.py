board=[str(i) for i in range(1,10)]
turn=0
while turn<9:
    choice=''
    while not choice.isdigit() or int(choice) < 1 or int(choice) > 9:
        choice = input(f"Player {'1 (X)' if turn % 2 == 0 else '2 (O)'} ")
    if board[int(choice)-1] in ['X', 'O']:
        print("That position is already taken. Please choose another.")
        continue
    if turn%2==0:
        board[int(choice)-1]='X'
    else:
        board[int(choice)-1]='O'
    turn+=1
print(f"{board[0]} | {board[1]} | {board[2]}\n---------\n{board[3]} | {board[4]} | {board[5]}\n---------\n{board[6]} | {board[7]} | {board[8]}")
win_possibilities = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
for pos in win_possibilities:
    if board[pos[0]] == board[pos[1]] == board[pos[2]]:
        print(f"Player {'1 (X)' if board[pos[0]] == 'X' else '2 (O)'} wins!")
        break
else:
    print("It's a tie!")
