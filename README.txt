The program can be run with the following command:

./run.sh <solve_alg> <file_name>

where <solve_alg> is one of 'astar', 'bfs', or 'dfs'
and <file_name> is the location of the puzzle file without the trailing ".txt" (eg. puzzle1, puzzle2)

Example:
./run.sh astar puzzle1

This will run the astar algorithm on puzzle1.txt and produce a file named "puzzle1sol_astar.txt" which contains the output
