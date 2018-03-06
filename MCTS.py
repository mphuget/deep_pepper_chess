import numpy as np

#this is hypothetical functions and classes that should be created by teamates.
import Board
import alpha_move
import alpha_prob
import stockfish_eval
import stockfish_move


def state_visited(list,state):
    if not list:
        return False, None
    for i in range(len(list)):
        if  np.array_equal(list[i].board, state):
            break
            return True, i
    return False, None



def Q(N,W):
    return W/N


def termination(state):
    if state:
        return True
    else:
        return False

class Leaf(Board):

    #This class inherit the Board class which control the board representation, find legale move and next board represenation.
    #It has the ability to store and update for each leaf the number of state-action N(s,a), Q(s,a) and P(s,a) 
    
    
    
    
    def __init__(board, init_W, init_P, init_N, explore_factor):

        self.board = board
        self.W = init_W
        self.P = init_P
        self.N = init_N
        self.explore_factor =explore_factor

    @property
    def Q(self):
        return self.W/self.N

    @property
    def U(self):

        return np.multiply( np.multiply( self.explore_factor , self.P) , np.divide( np.sqrt(np.sum(self.N)),(np.add(1., self.N))))
    def best_action(self):
        index = np.argmax(np.add(self.U, self.Q))
        # it is nice to decorate the legal move method with property
        return index

    @property
    def next_board(self):
        return self.render_action(self.board, self.best_action)#assuming the function you did

    def N_update(self,action_index):
        self.N[index]+=1

    def W_update(self, V_next, action_index):
        self.W[action_index]+=V_next

    def P_update(self, new_P):
        self.P = new_P


#state type and shape does not matter 


def MCTS(state,explore_factor,temp):#we can add here all our hyper-parameters
    # Monte-Carlo tree search function corresponds to the simulation step in the alpha_zero algorithm 
    # argumentes: state: the root state from where the stimulation start .
    #             explore_factor: hyper parameter to tune the exploration range in UCT
    #             temp: temperature constant for the optimum policy to control the level of exploration in the Play policy
    #             optional : dirichlet noise 
    # return: pi: vector of policy(action) with the same shape of legale move.
            
    
    #history of leafs for all previous runs  
    leafs=[] 
    for simulation in range (800):
        state_action_list=[]#list of leafs in the same run
        while not Termination(state):
            visited, index = state_visited(leafs,state)
            if visited:
                state_action_list.append(leafs[index])
            else:
                state_action_list.append(Leaf(state, init_W, alpha_prob(state), init_N, explore_factor)) #check the initialization strategy


            if  Termination(state):
                for i in list(reversed(range(len(state_action_list)))):

                    action_index = state_action_list[i].best_action
                    state_action_list[i].N_update(action_index)
                    if i == len(state_action_list) -1:
                        state_action_list[i].W_update(stock_fish_eval(state_action_list[i].next_board), action_index)
                        continue
                    state_action_list[i].W_update( alpha_eval(state_action_list[i].next_board) , action_index)
            state = state_action_list[-1].next_board
    N = leafs[0].N

    norm_factor = np.sum(np.power(N,temp))
    #optimum policy
    pi = np.divide(np.power(N,temp),norm_factor)

    return pi