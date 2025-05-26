"""Sudoku puzzle generator and solver supporting multiple grid sizes.

Auto‑generated documentation to improve code clarity.
"""


import random, math, json, hashlib
from typing import List, Tuple

def factor_pairs(n: int):
    """Factor pairs."""
    for i in range(1, int(n**0.5)+1):
        if n % i == 0:
            yield i, n//i

def get_subgrid_shape(size: int) -> Tuple[int,int]:
    """Get subgrid shape."""
    # Return (rows, cols) of subgrid
    # Prefer square subgrids when possible else pick closest factors
    root = int(math.isqrt(size))
    if root*root == size:
        return root, root
    # For 6, return 2x3
    # For 12, 3x4
    best = None
    for r,c in factor_pairs(size):
        if r==1: continue
        diff = abs(r-c)
        if best is None or diff < abs(best[0]-best[1]):
            best = (r,c)
    return best

def create_empty(size:int)->List[List[int]]:
    """Create empty."""
    return [[0]*size for _ in range(size)]

def is_valid(board:List[List[int]], row:int,col:int,num:int, sub_r:int, sub_c:int)->bool
    """Is valid."""
    size=len(board)
    # row/col
    if num in board[row]: return False
    if any(board[r][col]==num for r in range(size)): return False
    # subgrid
    start_r = (row//sub_r)*sub_r
    start_c = (col//sub_c)*sub_c
    for r in range(start_r,start_r+sub_r):
        for c in range(start_c,start_c+sub_c):
            if board[r][c]==num: return False
    return True

def solve(board:List[List[int]], sub_r:int, sub_c:int)->bool:
    """Solve."""
    size=len(board)
    for r in range(size):
        for c in range(size):
            if board[r][c]==0:
                nums=list(range(1,size+1))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board,r,c,num,sub_r,sub_c):
                        board[r][c]=num
                        if solve(board,sub_r,sub_c):
                            return True
                        board[r][c]=0
                return False
    return True

def generate_full_board(size:int)->List[List[int]]:
    """Generate full board."""
    sub_r, sub_c = get_subgrid_shape(size)
    board=create_empty(size)
    solve(board,sub_r,sub_c)
    return board

def remove_numbers(board:List[List[int]], difficulty:str, sub_r:int, sub_c:int)->List[List[int]]:
    """Remove numbers."""
    size=len(board)
    difficulty_map={
        "easy": int(size*size*0.35),
        "medium": int(size*size*0.45),
        "hard": int(size*size*0.55),
        "expert": int(size*size*0.65)
    }
    removals = difficulty_map.get(difficulty, difficulty_map["easy"])
    while removals>0:
        r=random.randrange(size); c=random.randrange(size)
        if board[r][c]!=0:
            board[r][c]=0
            removals-=1
    return board

def generate_puzzle(size:int=9,difficulty:str="easy"):
    """Generate puzzle."""
    sub_r,sub_c=get_subgrid_shape(size)
    full=generate_full_board(size)
    puzzle=remove_numbers([row[:] for row in full], difficulty, sub_r, sub_c)
    solution_hash = hashlib.sha256(json.dumps(full).encode()).hexdigest()
    return puzzle, solution_hash
