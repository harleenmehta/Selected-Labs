"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 26, 2020
"""

def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != " ":
                return False
    return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    if d_y == 0 and d_x == 1:
        if x_end + 1 > length:
            if board[y_end][x_end-length] != " ":
                left_end_open = False
            else:
                left_end_open = True
        elif x_end + 1 == length:
            left_end_open = False

        if x_end == 7:
            right_end_open = False
        else:
            if board[y_end][x_end + 1] != " ":
                right_end_open = False
            else:
                right_end_open = True

        if left_end_open and right_end_open:
            return "OPEN"
        elif not left_end_open and not right_end_open:
            return "CLOSED"
        else:
            return "SEMIOPEN"

    elif d_y == 1 and d_x == 0:
        if y_end + 1 > length:
            if board[y_end-length][x_end] != " ":
                top_open = False
            else:
                top_open = True
        elif y_end + 1 == length:
            top_open = False

        if y_end == 7:
            bottom_open = False
        else:
            if board[y_end + 1][x_end] != " ":
                bottom_open = False
            else:
                bottom_open = True

        if top_open and bottom_open:
            return "OPEN"
        elif not top_open and not bottom_open:
            return "CLOSED"
        else:
            return "SEMIOPEN"

    elif d_y == 1 and d_x == 1:

        if y_end + 1 > length and x_end + 1 > length:
            if board[y_end-length][x_end-length] != " ":
                left_top_open = False
            else:
                left_top_open = True
        elif y_end + 1 == length or x_end + 1 == length:
            left_top_open = False


        if y_end == 7 or x_end == 7:
            right_bottom_open = False
        else:
            if board[y_end + 1][x_end + 1] != " ":
                right_bottom_open = False
            else:
                right_bottom_open = True

        if left_top_open and right_bottom_open:
            return "OPEN"
        elif not left_top_open and not right_bottom_open:
            return "CLOSED"
        else:
            return "SEMIOPEN"


    elif d_y == 1 and d_x == -1:
        if y_end + 1 > length and x_end + length - 1 < 7:
            if  board[y_end - length][x_end + length] != " ":
                right_top_open = False
            else:
                right_top_open = True
        elif y_end + 1 == length or x_end - 1 + length == 7:
            right_top_open = False


        if x_end == 0 or y_end == 7:
            left_bottom_open = False
        else:
            if board[y_end + 1][x_end - 1] != " ":
                left_bottom_open = False
            else:
                left_bottom_open = True

        if left_bottom_open and right_top_open:
            return "OPEN"
        elif not left_bottom_open and not right_top_open:
            return "CLOSED"
        else:
            return "SEMIOPEN"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count, semi_open_seq_count = 0, 0
    if d_y == 0 and d_x == 1:
        for i in range(len(board) - length + 1):
            if board[y_start][x_start + i] == col:
                if i > 0:
                    if board[y_start][x_start + i - 1] == col:
                        continue
                for j in range(1, length):
                    if board[y_start][x_start + i + j] != col:
                        break
                    elif j == length - 1 and board[y_start][x_start + i + j] == col:
                        if x_start + i + j < len(board) - 1:
                            if board[y_start][x_start + i + j + 1] == col:
                             continue
                        if is_bounded(board, y_start, x_start + i + j, length, d_y, d_x) == "OPEN":
                            open_seq_count += 1
                        elif is_bounded(board, y_start, x_start + i + j, length, d_y, d_x) == "SEMIOPEN":
                            semi_open_seq_count += 1


    elif d_y == 1 and d_x == 0:
        for i in range(len(board)- length + 1):
            if board[y_start + i][x_start] == col:
                if i > 0:
                    if board[y_start + i - 1][x_start] == col:
                        continue
                for j in range(1, length):
                    if board[y_start + i + j][x_start] != col:
                        break
                    elif j == length - 1 and board[y_start + i + j][x_start] == col:
                        if y_start + i + j < len(board) - 1:
                            if board[y_start + i + j + 1][x_start] == col:
                                continue
                        if is_bounded(board, y_start + i + j, x_start, length, d_y, d_x) == "OPEN":
                            open_seq_count += 1
                        elif is_bounded(board, y_start + i + j, x_start, length, d_y, d_x) == "SEMIOPEN":
                            semi_open_seq_count += 1

    elif d_y == 1 and d_x == 1:
        for i in range(len(board) - max(y_start, x_start) - length + 1):
            if board[y_start + i][x_start + i] == col:
                if i > 0:
                    if board[y_start + i - 1][x_start + i - 1] == col:
                        continue
                for j in range(1, length):
                    if board[y_start + i + j][x_start + i + j] != col:
                        break
                    elif j == length - 1 and board[y_start + i + j][x_start + i + j] == col:
                        if y_start + i + j < len(board) - 1 and x_start + i + j < len(board) - 1:
                            if board[y_start + i + j + 1][x_start + i + j + 1] == col:
                                continue
                        if is_bounded(board, y_start + i + j, x_start + i + j, length, d_y, d_x) == "OPEN":
                            open_seq_count += 1
                        elif is_bounded(board, y_start + i + j, x_start + i + j, length, d_y, d_x) == "SEMIOPEN":
                            semi_open_seq_count += 1


    elif d_y == 1 and d_x == -1:
        for i in range(max(y_start, x_start) - min(y_start, x_start) - length + 2):
            if board[y_start + i][x_start - i] == col:
                if i > 0:
                    if board[y_start + i - 1][x_start - i + 1] == col:
                        continue
                for j in range(1, length):
                    if board[y_start + i + j][x_start - i - j] != col:
                        break
                    elif j == length - 1 and board[y_start + i + j][x_start - i - j] == col:
                        if y_start + i + j < len(board) - 1 and x_start - i - j > 0:
                            if board[y_start + i + j + 1][x_start - i - j - 1] == col:
                                continue
                        if is_bounded(board, y_start + i + j, x_start - i - j, length, d_y, d_x) == "OPEN":
                            open_seq_count += 1
                        elif is_bounded(board, y_start + i + j, x_start - i - j, length, d_y, d_x) == "SEMIOPEN":
                            semi_open_seq_count += 1



    return open_seq_count, semi_open_seq_count

def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    directions = [(0, 1),(1, 0),(1, 1),(1, -1)]
    for d_y, d_x in directions:
        if (d_y, d_x) == (0, 1):
            x_start = 0
            for y_start in range(len(board)):
                open_seq_count += detect_row(board, col, y_start, x_start, length, d_y, d_x)[0]
                semi_open_seq_count += detect_row(board, col, y_start, x_start, length, d_y, d_x)[1]
        elif (d_y, d_x) == (1, 0):
            y_start = 0
            for x_start in range(len(board)):
                open_seq_count += detect_row(board, col, y_start, x_start, length, d_y, d_x)[0]
                semi_open_seq_count += detect_row(board, col, y_start, x_start, length, d_y, d_x)[1]
        elif (d_y, d_x) == (1, 1):
            x_start = 0
            for y_start in range(len(board)-1):
                open_seq_count += detect_row(board, col, y_start, x_start, length, d_y, d_x)[0]
                semi_open_seq_count += detect_row(board, col, y_start, x_start, length, d_y, d_x)[1]
            y_start = 0
            for x_start in range(1, len(board)-1):
                open_seq_count += detect_row(board, col, y_start, x_start, length, d_y, d_x)[0]
                semi_open_seq_count += detect_row(board, col, y_start, x_start, length, d_y, d_x)[1]
        elif (d_y, d_x) == (1, -1):
            x_start = 7
            for y_start in range(0, len(board)-1):
                open_seq_count += detect_row(board, col, y_start, x_start, length, d_y, d_x)[0]
                semi_open_seq_count += detect_row(board, col, y_start, x_start, length, d_y, d_x)[1]
            y_start = 0
            for x_start in range(1, len(board)-1):
                open_seq_count += detect_row(board, col, y_start, x_start, length, d_y, d_x)[0]
                semi_open_seq_count += detect_row(board, col, y_start, x_start, length, d_y, d_x)[1]
    return open_seq_count, semi_open_seq_count

def search_max(board):
    empty_coords = []
    scores = {}
    move_y, move_x = 0, 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == " ":
                empty_coords.append((i, j))

    for empty_coord in empty_coords:
        board[empty_coord[0]][empty_coord[1]] = "b"
        scores[empty_coord] = score(board)
        board[empty_coord[0]][empty_coord[1]] = " "
    coords = list(scores.keys())
    values = list(scores.values())
    move_y, move_x = coords[values.index(max(values))]

    return move_y, move_x

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):

    # check from top to bottom
    for col in ["w","b"]:
        for i in range(len(board)//2):
            for j in range(len(board[0])):
                if board[i][j] == col:
                    for k in range(5):
                        if board[i+k][j]!= col:
                            break
                        elif k==4 and board[i+k][j] == col:
                            if col == "w":
                                return "White won"
                            elif col == "b":
                                return "Black won"

    #check from left to right
    for col in ["w","b"]:
        for i in range(len(board)):
            for j in range(len(board[0])//2):
                if board[i][j] == col:
                    for k in range(5):
                        if board[i][j+k]!= col:
                            break
                        elif k==4 and board[i][j+k] == col:
                            if col == "w":
                                return "White won"
                            elif col == "b":
                                return "Black won"

    # check from left-top to right-bottom (1, 1)
    for col in ["w","b"]:
        for i in range(len(board)//2):
            for j in range(len(board[0])//2):
                if board[i][j] == col:
                    for k in range(5):
                        if board[i+k][j+k]!= col:
                            break
                        elif k==4 and board[i+k][j+k] == col:
                            if col == "w":
                                return "White won"
                            elif col == "b":
                                return "Black won"

    # check from right-top to left-bottom (1, -1)
    for col in ["w","b"]:
        for i in range(len(board)//2):
            for j in range(len(board[0])-1,len(board[0])-len(board[0])//2 - 1, -1):
                if board[i][j] == col:
                    for k in range(5):
                        if board[i+k][j-k]!= col:
                            break
                        elif k==4 and board[i+k][j-k] == col:
                            if col == "w":
                                return "White won"
                            elif col == "b":
                                return "Black won"

    # check for draw
    is_full = True
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == " ":
                is_full = False
    if is_full:
        return "Draw"

    return "Continue playing"







def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))


def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0




if __name__ == '__main__':


    play_gomoku(8)

