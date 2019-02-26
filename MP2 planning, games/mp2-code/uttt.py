from time import sleep
from math import inf
from random import randint

class ultimateTicTacToe:
    def __init__(self):
        """
        Initialization of the game.
        """
        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]
        """        self.board=[['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','X','X','_','_','_','_'],
                    ['_','_','_','O','X','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_'],
                    ['_','_','_','_','_','_','_','_','_']]"""
        """[[x for x in range(9)] for i in range(9)]"""
        self.maxPlayer='X'
        self.minPlayer='O'
        self.maxDepth=3
        #The start indexes of each local board
        self.globalIdx=[(0,0),(0,3),(0,6),(3,0),(3,3),(3,6),(6,0),(6,3),(6,6)]

        #Start local board index for reflex agent playing
        self.startBoardIdx=4
        #self.startBoardIdx=randint(0,8)

        #utility value for reflex offensive and reflex defensive agents
        self.winnerMaxUtility=10000
        self.twoInARowMaxUtility=500
        self.preventThreeInARowMaxUtility=100
        self.cornerMaxUtility=30

        self.winnerMinUtility=-10000
        self.twoInARowMinUtility=-100
        self.preventThreeInARowMinUtility=-500
        self.cornerMinUtility=-30

        self.expandedNodes=0
        self.currPlayer=True

    def printGameBoard(self):
        """
        This function prints the current game board.
        """
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[:3]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[3:6]])+'\n')
        print('\n'.join([' '.join([str(cell) for cell in row]) for row in self.board[6:9]])+'\n')


    
    def all3combos(self):
        """"
        Just calls small3combos for all small boards on the big one
        input: none
        output: list of all 3 combos to look at in the board
        """
        ret =[]
        for g in self.globalIdx:
            set=self.checkcombos(g)
            ret+=set
        return ret
            
    def checkcombos(self,gi):
        """"
        This is a helper function that outputs all valid 3 combos to check for in a small tic tac toe board as lists
        input: global index of board you're looking at
        output: list of lists, each with 3 elements representing a row col or diagonal
        """
        x,y=gi
        ret =[]
        for i in range(3):
            ret.append(self.board[x+i][y:y+3]) #rows
            ret.append([self.board[x+j][y+i] for j in range(0,3)]) #cols
        ret.append([self.board[x][y], self.board[x+1][y+1],self.board[x+2][y+2]]) #diagonal left right
        ret.append([self.board[x+2][y], self.board[x+1][y+1], self.board[x][y+2]]) # diagonal right left
        return ret 

    def evaluatePredifined(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for predifined agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        score=0
        won = checkWinner()
        if won: #rule 1
            return 10000*won 
        
        #rule 2
        rows= all3combos() #all possible connections of 3 on the board
        score=0
        for r in rows:
            if isMax:
                if r.count(self.maxPlayer)==2 and (self.minPlayer not in r): #two in a row unblocked
                    score+=self.twoInARowMaxUtility()
                if r.count(self.minPlayer)==2 and r.count(self.maxPlayer)==1: #block min
                    score+=self.preventThreeInARowMaxUtility
            else:
                if r.count(self.minPlayer)==2 and (self.maxPlayer not in r): #two in a row unblocked
                    score+=self.twoInARowMinUtility()
                if r.count(self.maxPlayer)==2 and r.count(self.minPlayer)==1:#block max
                    score+=self.preventThreeInARowMinUtility


        #don't do rule 3 if it was evaluated under rule 2
        if score!=0: return score 
        corners = []
        for i in range(9):
            for j in range(9):
                if i%3!=1 and j%3!=1:
                    if isMax and self.board[i][j]==self.maxPlayer:
                        self.cornerMaxUtility+=30
                    elif (not isMax) and self.board[i][j]==self.minPlayer:
                        self.cornerMinUtility-=30     


        return score


    def evaluateDesigned(self, isMax):
        """
        This function implements the evaluation function for ultimate tic tac toe for your own agent.
        input args:
        isMax(bool): boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        score(float): estimated utility score for maxPlayer or minPlayer
        """
        #YOUR CODE HERE
        score=0
        return score

    def checkMovesLeft(self):
        """
        This function checks whether any legal move remains on the board.
        output:
        movesLeft(bool): boolean variable indicates whether any legal move remains
                        on the board.
        """
        #YOUR CODE HERE
        for i in self.board: #go through board and check for empty spots
            if i.count('_')!=0: return True
        #if you went through whole board then, u right no valid moves left
        return False

    def checkWinner(self):
        #Return termimnal node status for maximizer player 1-win,0-tie,-1-lose
        """
        This function checks whether there is a winner on the board.
        output:
        winner(int): Return 0 if there is no winner.
                     Return 1 if maxPlayer is the winner.
                     Return -1 if miniPlayer is the winner.
        """
        #YOUR CODE HERE
        combos=self.all3combos()
        for i in combos: # go through all row combinations... if you have 3 of same kind in a row. that person wins!
            if i.count(self.maxPlayer)==3: return 1
            if i.count(self.minPlayer)==3: return -1
        winner=0
        return 0

    def alphabeta(self,depth,currBoardIdx,alpha,beta,isMax):
        """
        This function implements alpha-beta algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        alpha(float): alpha value
        beta(float): beta value
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        #YOUR CODE HERE

        bestValue=0.0
        return bestValue

    def minimax(self, depth, currBoardIdx, isMax):
        """
        This function implements minimax algorithm for ultimate tic-tac-toe game.
        input args:
        depth(int): current depth level
        currBoardIdx(int): current local board index
        isMax(bool):boolean variable indicates whether it's maxPlayer or minPlayer.
                     True for maxPlayer, False for minPlayer
        output:
        bestValue(float):the bestValue that current player may have
        """
        if depth==self.maxDepth: #if you are at maxdepth, evaluate predefined
            return evaluatePredifined(isMax)
        
        values = []
        options = {} #holds potential moves so we know which one returns the max
        for i in range(9):
            #check if there is an available spot there
            gi= self.globalIdx[currBoardIdx]
            if self.board[gi[0]+i/3][gi[1]+i%3]!='_': continue
            
            #if so add it to the board and evaluate
            self.board[gi[0]+i/3][gi[1]+i%3]=self.maxPlayer if isMax else self.minPlayer
            self.expandedNodes+=1
            val = minimax(depth+1,i,(not isMax))
            self.board[gi[0]+i/3][gi[1]+i%3]='_' #remove it for other tests
            values.append(val)
            options[val]=i
        #now find min or max
        if isMax: return max(values)
        else: return min(values)
      #  bestValue=0.0
       # return bestValue

    def playGamePredifinedAgent(self,maxFirst,isMinimaxOffensive,isMinimaxDefensive):
        """
        This function implements the processes of the game of predifined offensive agent vs defensive agent.
        input args:
        maxFirst(bool): boolean variable indicates whether maxPlayer or minPlayer plays first.
                        True for maxPlayer plays first, and False for minPlayer plays first.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for offensive agent.
                        True is minimax and False is alpha-beta.
        isMinimaxOffensive(bool):boolean variable indicates whether it's using minimax or alpha-beta pruning algorithm for defensive agent.
                        True is minimax and False is alpha-beta.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        bestValue(list of float): list of bestValue at each move
        expandedNodes(list of int): list of expanded nodes at each move
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #max is offensive, min is defensive
        #YOUR CODE HERE
        bestMove=[]
        bestValue=[]
        gameBoards=[]
        expandedNodes=[]
        winner=0

        while (self.checkMovesLeft() and not self.checkWinner()):
            atglobal=0 #stores which global index we are at
            if isMinimaxOffensive and isMinimaxDefensive: #case of minimax vs minimax offensive (max) ifrst
                if maxFirst:
                    values = []
                    options = {} #holds potential moves so we know which one returns the max
                    for i in range(9):
                        #check if there is an available spot there
                        gi= self.globalIdx[atglobal]
                        if self.board[gi[0]+i/3][gi[1]+i%3]!='_': continue
                        
                        #if so add it to the board and evaluate
                        self.board[gi[0]+i/3][gi[1]+i%3]=self.maxPlayer 
                        self.expandedNodes+=1
                        val = minimax(depth+1,i,(not isMax))
                        self.board[gi[0]+i/3][gi[1]+i%3]='_' #remove it for other tests
                        values.append(val)
                        options[val]=i

                    #now find max and do the move, and store the values...
                    maxval=max(values)
                    bestValue.append(maxval)
                    bestidx=min(options[maxval]) #this is just if multiple idices had same value, chose smallest index
                    best=(self.globalIdx[atglobal][0]+bestidx/3,self.globalIdx[atglobal][1]+bestidx%3)
                    bestMove.append(best)
                    self.board[best[0]][best[1]]=self.maxPlayer
                    gameBoards.append(self.board)
                    expandedNodes.append(self.exapndedNodes)
                    self.expandedNodes=0
        ##NOTE: STILL NEED TO ADD SECOND PLAYER'S RESPONSE!


        return gameBoards, bestMove, expandedNodes, bestValue, winner

    def playGameYourAgent(self):
        """ rocesses of the game of your own agent vs predifined offensive agent.
        input args:
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner


    def playGameHuman(self):
        """
        This function implements the processes of the game of your own agent vs a human.
        output:
        bestMove(list of tuple): list of bestMove coordinates at each step
        gameBoards(list of 2d lists): list of game board positions at each move
        winner(int): 1 for maxPlayer is the winner, -1 for minPlayer is the winner, and 0 for tie.
        """
        #YOUR CODE HERE
        bestMove=[]
        gameBoards=[]
        winner=0
        return gameBoards, bestMove, winner

if __name__=="__main__":
    uttt=ultimateTicTacToe()
    gameBoards, bestMove, expandedNodes, bestValue, winner=uttt.playGamePredifinedAgent(True,True,True)#(True,False,False)
   # c=uttt.checkcombos(uttt.globalIdx[0])
   # for ca in c: print(ca)
    uttt.printGameBoard()
    if winner == 1:
        print("The winner is maxPlayer!!!")
    elif winner == -1:
        print("The winner is minPlayer!!!")
    else:
        print("Tie. No winner:(")
