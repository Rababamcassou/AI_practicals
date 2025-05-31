def print_board(board):
    for row in board:
        line = ""
        for col in range(8):
            if col == row:
                line += "Q "
            else:
                line += ". "
        print(line)
    print()


def is_safe(queens, row, col):
    for r in range(row):
        c = queens[r]
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True


def solve_n_queens(row, queens, solutions):
    if row == 8:
        solutions.append(queens[:])
        return

    for col in range(8):
        if is_safe(queens, row, col):
            queens[row] = col
            solve_n_queens(row + 1, queens, solutions)


def main():
    queens = [-1] * 8
    solutions = []
    solve_n_queens(0, queens, solutions)

    print(f"Total solutions: {len(solutions)}\n")
    for sol in solutions:
        board = [["."] * 8 for _ in range(8)]
        for row in range(8):
            board[row][sol[row]] = "Q"
        for row in board:
            print(" ".join(row))
        print()


if __name__ == "__main__":
    main()
