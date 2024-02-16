from typing import Any, Set, Tuple
from grid import Grid
import utils

def locate(grid: Grid, item: Any) -> Set[Tuple[int,int]]:
    '''
    This function takes a 2D grid and an item
    It should return a list of (x, y) coordinates that specify the locations that contain the given item
    To know how to use the Grid class, see the file "grid.py"  
    '''
    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()
    result=set()
    for y in range(grid.height):
        for x in range(grid.width):
            key=(x,y)
            if grid.__getitem__(key)==item:
               result.add(key)
    print(result)
    return result
             
# print(locate(Grid.GridFromArray([[0,1,0],[1,0,1],[0,1,0]]), 1))
              
    