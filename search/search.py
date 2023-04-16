# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
#stack이랑 queue 여기에 class로 define 되어있음

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    '''fringe의 요소 -> 튜플 ( (x좌표,y좌표), [지금까지 방향의 리스트] ) '''
    ''' Should be avoiding places already visited -> closed set '''

    visit = set() #the visit check must be implemented with a closed set instead of a list for efficiency reasons.
    fringe = util.Stack() # DFS uses stack with First In Last Out strategy
    fringe.push( ( problem.getStartState(), [] )) #we push (enqueue) the current state to the queue
    #Because it is the start state, the list (containing paths to get to that node) is empty
    while not fringe.isEmpty():
        nextstate = fringe.pop()
        # we then consider the node that is highest in priority from the fringe
        if problem.isGoalState(nextstate[0]):  # if the poped node (current one that we are considering) is a goal
            return nextstate[1]  # we return the path that we took to get to that point
        if nextstate[0] not in visit:
            # becasue this is a graph search, we do not consider the node that we already searched.
            # because in a tree the childs will be identical, it is highly inefficient for us to consider the visited node.
            visit.add(nextstate[0])
            possible = problem.getSuccessors(nextstate[0])
            for x in possible:  # for every tuple
                if x[0] not in visit:  # if we have not considered the 'possible next step'
                    nextnext = (x[0], nextstate[1] + [x[1]])
                    # we update the path by combining the current path with the next direction
                    # because x[1] is a single string, we have to convert to singleton list to join.
                    fringe.push(nextnext)
                    # we push the step into the fringe (stack) , with updated path
    return list() #we return a empty list if we could not reach the goal state




def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    visit = set() #the visit check must be implemented with a closed set instead of a list for efficiency reasons.
    fringe = util.Queue() # BFS uses queue with First In First Out strategy
    fringe.push( (problem.getStartState(), []) ) #we push (enqueue) the current state to the queue
    #Because it is the start state, the list (containing paths to get to that node) is empty

    while not fringe.isEmpty(): #if the fringe is empty, we have considered everything.
        nextstate = fringe.pop()
        #we then consider the node that is highest in priority from the fringe
        if problem.isGoalState(nextstate[0]):  # if the poped node (current one that we are considering) is a goal
            return nextstate[1]  #we return the path that we took to get to that point

        if nextstate[0] not in visit: #becasue this is a graph search, we do not consider the node that we already searched.
            #because in a tree the childs will be identical, it is highly inefficient for us to consider the visited node.
            visit.add(nextstate[0]) #check that we have considered this node
            possible = problem.getSuccessors(nextstate[0]) #get the successors
            #getSuccessors returns a list containing tuples
            #tuples inside -> ( (x,y) , direction, cost)
            for x in possible: #for every tuple
                if x[0] not in visit: #if we have not considered the 'possible next step'
                    nextnext = (x[0], nextstate[1] + [x[1]])
                    #we update the path by combining the current path with the next direction
                    fringe.push(nextnext)
                    #we push the step into the fringe, with updated path

    return list() #we return a empty list if we could not reach the goal state


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    #the fringe for UCS uses a priority Queue. We need to prioritize what we would pull of the fringe first.
    #this case, it would be the cost.
    visit = set()
    fringe.push( (problem.getStartState(), [], 0) , 0)
    #priority queue from the util library takes in two arguments when we push into the queue.
    # 1. the actual tuple -> ( (x,y) , list of steps to get to that point, cost to get to that point)
    # 2. the cost to get to that point (this will later be explained in A*search)
    while not fringe.isEmpty():
        nextstate = fringe.pop() #priority queue from the util library spits out only the actual tuple when popped.

        if problem.isGoalState( nextstate[0] ):
            return nextstate[1]

        if nextstate[0] not in visit:
            visit.add(nextstate[0])
            possible = problem.getSuccessors( nextstate[0] )
            for x in possible:
                if x[0] not in visit:
                    xcost = x[2]
                    #the third argument of the tuple x is the cost that it takes to take a single action to get to x.
                    nextnext = ( x[0], nextstate[1] + [x[1]] , nextstate[2] + xcost)
                    #we need to add the two costs (cost so far + cost to get to the next possible point x)
                    #this results in cost it takes from the starting state to the possible x.
                    fringe.push( nextnext, nextstate[2] + xcost )
                    #the added cost is then pushed in as an indicator for priority within the queue
    return list() #도달 못했으면 빈 리스트 리턴


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    visit = set()

    fringe.push((problem.getStartState(), [], 0), 0 + heuristic(problem.getStartState() , problem) )
    #We use heuristic + UCS to implement A* search
    #the difference between UCS and A*
    # --The priority considered when put into the queue is not only the cost to get there, but a combination of heuristic and the cost.

    while not fringe.isEmpty():
        nextstate = fringe.pop()

        if problem.isGoalState(nextstate[0]):
            return nextstate[1]

        if nextstate[0] not in visit:
            visit.add(nextstate[0])
            possible = problem.getSuccessors(nextstate[0])
            for x in possible:
                if x[0] not in visit:
                    xcost = x[2]
                    nextnext = (x[0], nextstate[1] + [x[1]], nextstate[2] + xcost)
                    #becuase the third component of the tuple is only the cost to get to that point, we do not add the heuristic.
                    fringe.push(nextnext, nextstate[2] + xcost + heuristic(x[0] , problem) )
                    #However, when pused into the fringe, we add the heuristic
                    #This is because...
                    # heuristic is not the actual cost to get to that point, but is a variable to be considered when popped out of the fringe

    return list()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
