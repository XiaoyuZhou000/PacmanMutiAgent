# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).



from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPacmanPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # print("successorGameState: ", successorGameState)
        # print("newPos: ", newPos)
        # print("newFood: ", newFood)
        # print("newGhostStates: ", str(newGhostStates))
        # print("newScaredTimes: ", str(newScaredTimes))
        """
        Goal:
        1. Find the shortest path to the nearest food
        2. Find food and capsules
        4. Record the scores
        """

        # 1. Find the ghost position and the path to the ghost
        # newGhostPos = successorGameState.getGhostPosition(1)
        # pathPacGhost = manhattanDistance(newGhostPos, newPacmanPos)

        # 2. Find food
        foodList = newFood.asList()
        shortestPathToFood = 99999999999999
        for food in foodList:
            foodDistance = manhattanDistance(food, newPacmanPos)
            if (foodDistance < shortestPathToFood):
                shortestPathToFood = foodDistance

        # 4. Record the scores
        score = successorGameState.getScore()
        # Eat ghost
        # if (pathPacGhost == 0):
        #     score += 200
        # Eat food
        # if ( len(foodList) < len(newFood.asList()) ):
        #     score += 10
        score += 10 / shortestPathToFood
        # score -= 1

        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"                                                                                                        
        
        def miniMax(gameState, agentIndex, depth):

            def minValue(actions, agentIndex, nextAgentIndex, depth):
                min = 999999999999999
                for action in actions:
                    nextMin, nextAction = miniMax(gameState.generateSuccessor(agentIndex, action), nextAgentIndex, depth)
                    if nextMin < min:
                        min, bestAction = nextMin, action
                return min, bestAction

            def maxValue(actions, agentIndex, nextAgentIndex, depth):
                max = -999999999999999
                for action in actions:
                    nextMax, nextAction = miniMax(gameState.generateSuccessor(agentIndex, action), nextAgentIndex, depth)
                    if nextMax > max:
                        max, bestAction = nextMax, action
                return max, bestAction


            action = gameState.getLegalActions(agentIndex)
            agentNum = gameState.getNumAgents() - 1
            bestAction = None

            if gameState.isLose() or gameState.isWin() or (depth == self.depth):
                return self.evaluationFunction(gameState), None

            if agentIndex == agentNum:
                depth += 1
                nextAgentIndex = self.index
            else:
                nextAgentIndex = agentIndex + 1


            if agentIndex == 0:
                max, bestAction = maxValue(action, agentIndex, nextAgentIndex, depth)
            else:
                return minValue(action, agentIndex, nextAgentIndex, depth)
            return max, bestAction

        score, action = miniMax(gameState, self.index, 0)
        return action
                                                    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def miniMax(gameState, agentIndex, depth, alpha, beta):

            def minValue(actions, agentIndex, nextAgentIndex, depth, alpha, beta):
                min = 999999999999999
                for action in actions:
                    nextMin, nextAction = miniMax(gameState.generateSuccessor(agentIndex, action), nextAgentIndex, depth, alpha, beta)
                    if nextMin < min:
                        min, bestAction = nextMin, action
                    if min < alpha:
                        return min, action
                    if min < beta:
                        beta = min
                return min, bestAction

            def maxValue(actions, agentIndex, nextAgentIndex, depth, alpha, beta):
                max = -999999999999999
                for action in actions:
                    nextMax, nextAction = miniMax(gameState.generateSuccessor(agentIndex, action), nextAgentIndex, depth, alpha, beta)
                    if nextMax > max:
                        max, bestAction = nextMax, action
                    if max > beta:
                        return max, action
                    if alpha < max:
                        alpha = max
                return max, bestAction

            action = gameState.getLegalActions(agentIndex)
            agentNum = gameState.getNumAgents() - 1
            bestAction = None

            if gameState.isLose() or gameState.isWin() or (depth == self.depth):
                return self.evaluationFunction(gameState), None

            if agentIndex == agentNum:
                depth += 1
                nextAgentIndex = self.index
            else:
                nextAgentIndex = agentIndex + 1

            if agentIndex == 0:
                max, bestAction = maxValue(action, agentIndex, nextAgentIndex, depth, alpha, beta)
            else:
                return minValue(action, agentIndex, nextAgentIndex, depth, alpha, beta)
            return max, bestAction

        score, action = miniMax(gameState, self.index, 0, -1e10, 1e10)
        return action


    


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def miniMax(gameState, agentIndex, depth):

            def minValue(actions, agentIndex, nextAgentIndex, depth):
                p = 1/len(actions)
                total = 0
                min = 999999999999999
                for action in actions:
                    nextMin, nextAction = miniMax(gameState.generateSuccessor(agentIndex, action), nextAgentIndex, depth)
                    if nextMin < min:
                        min, bestAction = nextMin, action
                    total += p * nextMin
                
                return total, bestAction

            def maxValue(actions, agentIndex, nextAgentIndex, depth):
                max = -999999999999999
                for action in actions:
                    nextMax, nextAction = miniMax(gameState.generateSuccessor(agentIndex, action), nextAgentIndex, depth)
                    if nextMax > max:
                        max, bestAction = nextMax, action
                return max, bestAction


            action = gameState.getLegalActions(agentIndex)
            agentNum = gameState.getNumAgents() - 1
            bestAction = None

            if gameState.isLose() or gameState.isWin() or (depth == self.depth):
                return self.evaluationFunction(gameState), None

            if agentIndex == agentNum:
                depth += 1
                nextAgentIndex = self.index
            else:
                nextAgentIndex = agentIndex + 1


            if agentIndex == 0:
                max, bestAction = maxValue(action, agentIndex, nextAgentIndex, depth)
            else:
                return minValue(action, agentIndex, nextAgentIndex, depth)
            return max, bestAction

        score, action = miniMax(gameState, self.index, 0)
        return action
        
    

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
