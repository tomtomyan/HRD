#!/bin/bash

# $1: algorithm to solve puzzle (astar, bfs, dfs)
# $2: puzzle to solve (puzzle1, puzzle2) (Do not include trailing ".txt")

python3 huarongdao.py $1 $2.txt > $2sol_$1.txt
