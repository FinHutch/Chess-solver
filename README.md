# Chess Solver

I used this project to help me understand the Minimax algorithm with Alpha-Beta pruning. I plan to use it in the future in a more useful case.
In the program it is 'cheaper' to search through checks and captures so it is more likely to capture tactics, however it still has to explore ~50,000 states to look 4 moves ahead.

The value of a position once it is done searching is calculated by adding up the value of each piece, I have given the pieces more value when they are attacking the center of the board and also given more points
when the king is safe. This is somewhat arbritrary



## Future Improvements

While the current implementation is functional and can defeat a 1200-rated player, there are several areas for potential improvement:

- **Optimization:** Not optimised at all, everything is recalculated for each board node, indluding looking back through the history to look for the 50 move rule
- **Advanced Heuristics:** the position values are arbritrary and were not thoroughly thought through
- **User Interface:** The interface is WACK it uses pygame and is not smooth to use at all.
- **Support for Different Difficulty Levels:** this would be super easy to implement

