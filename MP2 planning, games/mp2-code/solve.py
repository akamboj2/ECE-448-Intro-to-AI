# -*- coding: utf-8 -*-
import numpy as np
soln = {}

def solve(board_p, pents_p):
    """
    This is the function you will implement. It will take in a numpy array of the board
    as well as a list of n tiles in the form of numpy arrays. The solution returned
    is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
    where pi is a tile (may be rotated or flipped), and (rowi, coli) is 
    the coordinate of the upper left corner of pi in the board (lowest row and column index 
    that the tile covers).
    
    -Use np.flip and np.rot90 to manipulate pentominos.
    
    -You can assume there will always be a solution.
    """
 #   print("TYPE!: ",type(pents_p))

    board=np.copy(board_p)
    pents=np.copy(pents_p).tolist() 
    b=pent_init(pents,board)
    locations=list(b.keys())
    print(soln)
    print(Pent.win)
    # for ind in b:
    #     print(ind,":")
    #     for i in b[ind]:
    #         print("\t",i.id,i.arr)
    while(len(soln)!=len(pents_p)):
        backtrack(b,locations)
        
   # put_on_board(board)
    print(board)
   # print(soln)
    return soln
   # raise NotImplementedError

class Pent():
    #these two variable declared outside init without self are static/class variables (consistent throughout all instances of class)
    #they're essentially so all objects can see
    count_spots=[]
    available=[]
    win=0
    def __init__(self,givenID,array,givenr=0,givenc=0,fn=0,rn=0):
        self.id=givenID
        self.r=givenr #note this r,c is the topleft of the corner array.
        self.c=givenc
        self.flipnum=fn
        self.rotnum=rn
        self.arr=array
        self.orientation_used=False     

def pent_init(pents,board):
    """
    Initializes needed dictionary/data structures for algorithm
    input: pent arrays, and board
    Returns a dicitonary of Pent objects covering every space of the board
    """
    b={}
    for p in pents:
        Pent.count_spots.append(0) #for every pent add a corresponding count and available bool
        Pent.available.append(True)
        id=get_pent_idx(p)
        for row in range(board.shape[0]):
            for col in range(board.shape[1]):
                if board[row][col]==0: continue #we're only tiling the 1s on the board
              #  print("at",row,",",col)
                for flipnum in range(3): #for rotations (just using is_pentomino's method)
                    if flipnum > 0:
                        p = np.flip(p, flipnum-1)
                    for rot_num in range(4):
                #        print(p)
                #        print('\t',row,p.shape[0],col,p.shape[1])
                        if row+len(p) <= board.shape[0] and col+len(p[0]) <= board.shape[1]: #this means it fits on board at this position
                #            print("fits board dimensions")
                            p_obj=Pent(id,p,row,col,flipnum,rot_num)
                            p_obj.count_spots[p_obj.id-1]+=1 #because we are adding a potential spot of where it can be
                            #now loop through pent array and add r,c locations to dictionary if needed
                            for r in range(len(p)): 
                                for c in range(len(p[0])):
                 #                   print('\t',r,len(p),c,len(p[0]))
                                    if p[r][c] != 0:
                                        if (row+r,col+c) in b.keys():
                                            pent_in=False   #check to make sure you're not reusing the rotations that are equivalent (rotating squre vs. L shape)
                                            for checkp in b[(row+r,col+c)]:
                                                if np.array_equal(p,checkp.arr):
                                                    pent_in=True
                                            if not pent_in:
                                                b[(row+r,col+c)].append(p_obj)
                                        else:
                                            b[(row+r,col+c)]=[p_obj]
                        p=np.rot90(p)

    return b

def backtrack(b,available_locs):#available locations will have to hold the values of locations with 1 in them ( available_locs should be list of tuples)
    #first chose row,col location with fewest possible pents. need list of row,col locations
    if len(available_locs)==0:
        Pent.win=1
        return
    small_loc=available_locs[0] 
    for l in available_locs:
        if len(b[l])<len(b[small_loc]): #len runs in O(1) so don't be afraid to use it!
            small_loc=l

    #now go through each pents and make a list with first being least possible locations
    p_avail=False
    possible_pents=[]
    for p in b[small_loc]:
        if not p.orientation_used: 
            if p_avail==False: #first available pent
                p_avail=True
            possible_pents.append(p) #save as a pent option to check
            p.orientation_used=True #make sure to change all pent/orientations on this r,c location to used! (bc nothing can occupy this spot!)
            Pent.count_spots[p.id-1]-=1
        #if by the end of this loop p-avail is false... then there's no available pent orientations for this spot! GG! Backtrack!
        if p_avail==False: return
    
    #this should sort the possible pents in order from least spots it can go on to most!
    possible_pents.sort(key=lambda x: Pent.count_spots[x.id-1]) #index minus one bc pents indices start from 1 unlike lists

    for p in possible_pents: #now we have pent and location! Sooo. Place the pent!
        soln[small_loc]=p #add it to solution dict (or change it from previous p if not in first round of this loop)
        #go through locations in pent and remove them from available locations
        removed=[] # locations removed from availble
        changed=[] #pents changed to used=true
        for r in range(len(p.arr)):
            for c in range(len(p.arr[0])):
                if (r+p.r,c+p.c) in available_locs:
                    available_locs.remove((r+p.r, c+p.c)) #this should remove small_loc too
                    removed.append((r+p.r, c+p.c))
                for overlap_pent in b[(r+p.r,c+p.c)]: #NOTE: These are pents at this location... this is changing possible pents at other locations that the pent you are place at
                    if overlap_pent.orientation_used==False: #need to do this to make sure u don't change pents that were already used by other locations back to true when backtracking
                        overlap_pent.orientation_used=True 
                        Pent.count_spots[p.id-1]-=1
                        changed.append(overlap_pent)
        backtrack(b,available_locs)
        if Pent.win==1: return #if you win yay ur done!
        #if u didn't win something didn't go right along this path so we got to back track and try next pent
        available_locs.extend(removed)
        for op in changed: #fix all the overlapping pents that u switched   |
            op.orientation_used=False #think about case like _._._.| with  .|. .  the second one starts outside of the first but should still be marked as unavialbe
                                        #which doesn't happen if you don't change all pieces in block to used=True
            Pent.count_spots[p.id-1]+=1

    #if u finished trying all the pents then something must have gone wrong before your move, so back track even more
    del soln[p] #this p should be at the end of possible_pents so should be same as possible_pents.pop()
    for p in possible_pents:
        p.orientation_used=False 

     


    #probs need looping through ALL locations and ALL pents changing orientation used to false, bc if u use a pent 
    #on some unrelated pent possible orientation across the board it would change how many pents are available !
    #don't we need a big for loop outside of small loc, constantly chosing small locations? --maybe not let's see
    #also where is the win condition? where do i set win=1

def get_pent_idx(pent):
    """
    Returns the index of a pentomino.
    """
    pidx = 0
    
    for i in range(len(pent)):
        for j in range(len(pent[0])):
            if pent[i][j] != 0:
                pidx = pent[i][j]
                break
        if pidx != 0:
            break
    if pidx == 0:
        return -1
    return pidx - 1

def put_on_board(board):
    for loc in soln:
        p=soln[loc]
        for r in range(len(p.arr)):
            for c in range(len(p.arr[0])):
                print(loc[0],r,loc[1],c)
                board[loc[0]+r][loc[1]+c]=p.arr[r][c]

if __name__=="__main__":
    #THIS PART TESTS PENT INIT!
   # pents= [np.array([[1],[1]]),np.array([[2],[2]])]
    pents=[np.array([[1,0],[1,1]]),np.array([[2,0],[2,2]])]
   # board = np.ones((2,2))
    board=np.ones((2,3))
    # print(pents,'\n',board)
    # b=pent_init(pents,board)
    # for ind in b:
    #     print(ind,":")
    #     for i in b[ind]:
    #         print("\t",i.id,i.arr)

    solve(board,pents)
    for ind in soln:
        print(ind,":")
        for i in soln[ind].arr:
            print(i)
            #print("\t",i.id,i.arr)
