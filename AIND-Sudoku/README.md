# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The naked twins problem is a strategy to identify PAIRS to a set of peers that have the same 2 numbers of possibility. You eliminate these two numbers from all the boxes that have these as peers. 

![Alt text](images/nakedtwinpairs.png?raw=true "Naked Twins")

We use constraint propagation to eliminate firstly the pair of numbers that are found in a naked twin pair to other peers (same row, column, diaganol and box) and then continue this to find the solution of the grid. This method of continually reducing the solution by 'constraining' the puzzle is knwon as constraint propagation. 


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We implement the diagonal by adding it to the unitlist (a list of constraints for a unit in sudoku. Consequently, this limits and constrains the puzzle search further by NOT accepting solutions that do not satisfy the diagonal limitation. I have attached an example of how I did this in the code (solution.py)

![Alt text](images/diags.png?raw=true "Diag added to unitlist")

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

