# Day 2a

# Score table
OP_ROCK, OP_PAPER, OP_SCISSORS = "A", "B", "C"
ROCK, PAPER, SCISSORS = "X", "Y", "Z"
FORCE_LOSE, FORCE_DRAW, FORCE_WIN = "X", "Y", "Z"

VAL_LOSS, VAL_DRAW, VAL_WIN = 0, 3, 6
VAL_ROCK, VAL_PAPER, VAL_SCISSORS = 1, 2, 3

# part1 and part2 correspond to parts 1 and 2 of the problem
moves = {
    OP_ROCK: {
        "part1": {ROCK: VAL_ROCK + VAL_DRAW,
                  PAPER: VAL_PAPER + VAL_WIN,
                  SCISSORS: VAL_SCISSORS + VAL_LOSS},
        "part2": {FORCE_LOSE: VAL_SCISSORS + VAL_LOSS,
                  FORCE_DRAW: VAL_ROCK + VAL_DRAW,
                  FORCE_WIN: VAL_PAPER + VAL_WIN}
    },
    OP_PAPER: {
        "part1": {ROCK: VAL_ROCK + VAL_LOSS,
                  PAPER: VAL_PAPER + VAL_DRAW,
                  SCISSORS: VAL_SCISSORS + VAL_WIN},
        "part2": {FORCE_LOSE: VAL_ROCK + VAL_LOSS,
                  FORCE_DRAW: VAL_PAPER + VAL_DRAW,
                  FORCE_WIN: VAL_SCISSORS + VAL_WIN}
    },
    OP_SCISSORS: {
        "part1": {ROCK: VAL_ROCK + VAL_WIN,
                  PAPER: VAL_PAPER + VAL_LOSS,
                  SCISSORS: VAL_SCISSORS + VAL_DRAW},
        "part2": {FORCE_LOSE: VAL_PAPER + VAL_LOSS,
                  FORCE_DRAW: VAL_SCISSORS + VAL_DRAW,
                  FORCE_WIN: VAL_ROCK + VAL_WIN}
    }
}

# Let's Play Rock Paper Scissors
score1, score2 = 0, 0
with open("input.csv", "r") as inp:
    for line in inp:
        opponent, player = line.split()
        score1 += moves[opponent]["part1"][player]
        score2 += moves[opponent]["part2"][player]
print(score1)
print(score2)
