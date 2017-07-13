import random

assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]


# GLOABL VARIABLES
rows = 'ABCDEFGHI'
cols = '123456789'
cols_rev = cols[::-1]
boxes = cross(rows, cols)

# Rows columsn and squares
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# Add diaganols
diag_1_units = [rows[i] + cols[i] for i in range(0,len(rows))]
#print(diag_1_units)
diag_2_units = [rows[i] + cols[-i-1] for i in range(0,len(rows))]
#print(diag_2_units)

diag_units = [diag_1_units, diag_2_units]

# Create Unitlist
unitlist = row_units + column_units + square_units + diag_units


units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values



def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    
    # Find POSSIBLE twins 
    # Iterate each one
    for unit in unitlist:
        
        # Iterate over each 
        values_in_unit = [values[box] for box in unit] 
        
        # Find the duplicates 
        duplicates = [v for v in values_in_unit if values_in_unit.count(v) == 2 and len(v) == 2]
		
        # Iterate each duplicate, each char in the duplicates, then find the box in the unit
        for d in duplicates:
            for char in d:
                for box in unit:
                    if values[box] != d:
                        values = assign_value(values,box,values[box].replace(char,''))
    return values



def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    numerals = '123456789'
    for g in grid:
        if g in numerals:
            values.append(g)
        if g == '.':
            values.append(numerals)
    assert len(values) == 81
    return dict(zip(boxes, values))
            

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    # Find total width from each box row

    width = 1+max(len(values[s]) for s in boxes)
    
    lines =  '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(lines)
    return
    

def eliminate(values):
    # Find each key or value which is len == 1, add them to a list
    solvedList = []
    for keys, v in values.items():
        if len(v) == 1:
            solvedList.append(keys)
    # print (solvedList)
        
    # Check against dictionary
    for s in solvedList:
        num = values[s]
        for p in peers[s]:
            values[p] = values[p].replace(num,'')
        
    return values

def only_choice(values):
    # NB: Udacity solution WAY mor elegant
    
    for unit in unitlist:
        # This is a list of lists (each list is the ones in square)
        listOfUnchosen = []
        listOfUnchosenValues = []
        listOfUnique = []
        uniqueValues = []
        flipped = {}
        dictx = {}
        # iterate firstly over all the values to find non len 1 ones
        for s in unit:

            listOfUnchosen.append(s)
            listOfUnchosenValues.append(list(values[s]))

        dictx = dict(zip(listOfUnchosen,listOfUnchosenValues))
        # print(dictx)
        
        # Check for unique values

        for k, v in dictx.items():
            for l in v:
                if l not in flipped:
                    flipped[l] = [k]
                else:
                    flipped[l].append(k)

        for f, g in flipped.items():
            if len(g) == 1:
                for pos in g:
                    listOfUnique.append(pos)
                    uniqueValues.append(f)

        for l in listOfUnique:
            # Make sure nothing else in the list has this number!!!
            tempCheck = []
            for u in unit:
                tempCheck.append(values[u])

            #if uniqueValues[listOfUnique.index(l)] not in tempCheck:
            #print(tempCheck)
            values[l] = uniqueValues[listOfUnique.index(l)]
   
        
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if values is False:
        return False 
    if all(len(values[s]) == 1 for s in boxes): 
        return values 
        
    # Choose one of the unfilled squares with the fewest possibilities
    # Each key values.keys will have a box, so you find the length of each box
    box_lengths = [len(values[box]) for box in values.keys() if len(values[box]) > 1] 
    
    # find the lowest 
    min_box = min(box_lengths)
    
    # Find squares
    sq = [box for box in values.keys() if len(values[box]) == min_box]
    s = random.choice(sq)
   
    # Recursion to solve EACH sudoku
    # for value in values[s]
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    print("\n1. Set up the Board")
    values = grid_values(grid)
    display(values)

    print("\n")
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')