import random
import ipdb
import sys
sys.path.append("..")  #so other modules can be found in parent dir
from Player import *
from Constants import *
from Construction import CONSTR_STATS
from Ant import UNIT_STATS
from Move import Move
from GameState import *
from AIPlayerUtils import *


##
#AIPlayer
#Description: The responsbility of this class is to interact with the game by
#deciding a valid move based on a given game state. This class has methods that
#will be implemented by students in Dr. Nuxoll's AI course.
#
#co-authors of Hussaih variant: Jenkin Schibel, James Conn
#
#Variables:
#   playerId - The id of the player.
##



class AIPlayer(Player):

    #__init__
    #Description: Creates a new Player
    #
    #Parameters:
    #   inputPlayerId - The id to give the new player (int)
    #   cpy           - whether the player is a copy (when playing itself)
    ##
    def __init__(self, inputPlayerId):
        super(AIPlayer,self).__init__(inputPlayerId, "Hussaih")
        self.enemyId = 1 - self.playerId


    def heuristicStepsToGoal(self,currentState):
        myInv=getCurrPlayerInventory(currentState)
        enemyInv=getEnemyInv(currentState)
        mySoldiers=getAntList(currentState,self.playerId,(SOLDIER,DRONE,R_SOLDIER))

        totalDistToQueen = 0
        for soldier in mySoldiers:
            totalDistToQueent=totalDistToQueen+approxDist(soldier.coords,enemyInv.getQueen().coords)
        if len(mySoldiers) == 0:
            avgDistToQueen=0
        else:
            avgDistToQueen=totalDistToQueen/len(mySoldiers)

        foodVal=myInv.foodCount - enemyInv.foodCount

        anthillCapture=enemyInv.getAnthill().captureHealth

        #number of attacks on average it takes to kill the queen
        queenHealthVal=(10/3)

        return avgDistToQueen+foodVal+anthillCapture+queenHealthVal


    def buildNode(self,move,reachedState,depth=0,parentNode=None):
        nodeDict = {
            "move":move,
            "reachedState":reachedState,
            "depth":depth,
            "parentNode":parentNode,
            "stateEvaluation":self.heuristicStepsToGoal(reachedState) + depth
        }
        return nodeDict

    def bestMove(self,nodes):
        bestNodes = []
        bestNodes.append(nodes[0])
        for node in nodes[1:]:
            if node['stateEvaluation'] == bestNodes[0]['stateEvaluation']:
                bestNodes.append(node)
                continue
            if node['stateEvaluation'] > bestNodes[0]['stateEvaluation']:
                bestNodes.clear()
                bestNodes.append(node)
        # if there are multiple nodes with the same rating then randomly pick one
        if len(bestNodes) > 1:
            return bestNodes[random.randint(0,len(bestNodes)-1)]
        # if there is a unique node then use that one
        else:
            return bestNodes[0]
    def printBestMove(self,bestMove):
        print("move: {} \nreachedState: {} \ndepth: {} \nparentNode: {} \nstateEvaluation : {}\n\n".format(bestMove['move'],bestMove['reachedState'],bestMove['depth'],bestMove['parentNode'],bestMove['stateEvaluation']))




    ##
    #getPlacement
    #
    #Description: called during setup phase for each Construction that
    #   must be placed by the player.  These items are: 1 Anthill on
    #   the player's side; 1 tunnel on player's side; 9 grass on the
    #   player's side; and 2 food on the enemy's side.
    #
    #Parameters: #   construction - the Construction to be placed.
    #   currentState - the state of the game at this point in time.
    #
    #Return: The coordinates of where the construction is to be placed
    ##
    def getPlacement(self, currentState):
        numToPlace = 0
        #implemented by students to return their next move
        if currentState.phase == SETUP_PHASE_1:    #stuff on my side
            numToPlace = 11
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on your side of the board
                    y = random.randint(0, 3)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        elif currentState.phase == SETUP_PHASE_2:   #stuff on foe's side
            numToPlace = 2
            moves = []
            for i in range(0, numToPlace):
                move = None
                while move == None:
                    #Choose any x location
                    x = random.randint(0, 9)
                    #Choose any y location on enemy side of the board
                    y = random.randint(6, 9)
                    #Set the move if this space is empty
                    if currentState.board[x][y].constr == None and (x, y) not in moves:
                        move = (x, y)
                        #Just need to make the space non-empty. So I threw whatever I felt like in there.
                        currentState.board[x][y].constr == True
                moves.append(move)
            return moves
        else:
            return [(0, 0)]
    
    ##
    #getMove
    #Description: Gets the next move from the Player.
    #
    #Parameters:
    #   currentState - The state of the current game waiting for the player's move (GameState)
    #
    #Return: The Move to be made
    ##
    def getMove(self, currentState):

        # get all the legal Moves
        moves = listAllLegalMoves(currentState)

        nodes = []
        for move in moves:
            # nodes.append(getNextState(currentState,move))
            nodes.append(self.buildNode(move,getNextState(currentState,move),0,None))

        bestMove=self.bestMove(nodes)
        self.printBestMove(bestMove)
        return bestMove['move']

    ##
    #getAttack
    #Description: Gets the attack to be made from the Player
    #
    #Parameters:
    #   currentState - A clone of the current state (GameState)
    #   attackingAnt - The ant currently making the attack (Ant)
    #   enemyLocation - The Locations of the Enemies that can be attacked (Location[])
    ##
    def getAttack(self, currentState, attackingAnt, enemyLocations):
        #Attack a random enemy.
        return enemyLocations[random.randint(0, len(enemyLocations) - 1)]

    ##
    #registerWin
    #
    # This agent doens't learn
    #
    def registerWin(self, hasWon):
        #method templaste, not implemented
        pass
