import random
import numpy as np
import time
import math
import sys

class RandomAgent:
    def __init__(self):
        self.step = 0

    def getAction(self):
        '''samples actions in a round-robin manner'''
        self.step = (self.step + 1) % 4
        return 'up down left right'.split()[self.step]

    def observe(self, newState, reward, event):
        pass

#action definitions: 0=up, 1=down, 2=left, 3=right 
class QlearningAgent:
    def __init__(self,numStates,state,gamma,randomseed):
        self.episodes=1
        self.step=0
        self.alpha=0.8
        self.epsilon=0.5
        self.numStates=numStates
        self.init_state=state
        self.state=state
        self.gamma=1
        self.cumRew=0
        random.seed(randomseed)
        self.Q=np.random.rand(self.numStates,4)
        self.action = self.decideAction()
        self.tic=time.time()
        #print("Q learning agent initialized:"+str(state))

    def getAction(self):
        self.step = self.step + 1
        ac = 'up down left right'.split()[self.action]
        #print("Action taken:"+ac)
        return ac

    def decideAction(self):
        r = random.random()
        if r<self.epsilon:
            action = random.randint(0, 3)
        else:
            action=np.argmax(self.Q[self.state])
        return action

    def observe(self, newState, reward, event):
        self.cumRew+=reward
        self.Q[self.state][self.action]+=self.alpha*(reward+(self.gamma*np.amax(self.Q[newState]))-self.Q[self.state][self.action])
        self.state=newState
        self.action=self.decideAction()
        if event!='continue':
            #print("Episode No."+str(self.episodes)+", Reward:"+str(self.cumRew)+", Time taken:{:.3f}".format(time.time()-self.tic))
            if self.episodes%100==0:
                #print("#",end='')
            self.step=0
            self.state=self.init_state
            self.action = self.decideAction()
            self.episodes+=1
            self.cumRew=0
            self.tic=time.time()
            if self.episodes>100 and self.epsilon>=0.1:
                self.epsilon-=0.002
            if self.episodes>100 and self.alpha>=0.3:
                self.alpha-=0.002
            if event=='goal':
                for a in range(4):
                    self.Q[newState][a]=0
            # side=int(math.sqrt(self.numStates))
            # m=np.amax(self.Q,axis=1)
            # Pi=np.argmax(self.Q,axis=1)
            # for y in range(side):
            #     print('  |', end='')
            #     for x in range(side):
            #         state = y*side + x
            #         print(' {:.3f} {} |'.format(m[state],'up down left right'.split()[Pi[state]]), end='')
            #     print()

class SarsaAgent:
    def __init__(self,numStates,state,gamma,lamb,randomseed):
        self.episodes=1
        self.step=0
        self.alpha=1
        self.epsilon=0.25
        self.numStates=numStates
        self.init_state=state
        self.state=state
        self.gamma=gamma
        self.lamb=lamb
        self.cumRew=0
        random.seed(randomseed)
        self.Q=np.random.rand(self.numStates,4)
        self.e=np.zeros((self.numStates,4))
        self.action = self.decideAction(self.state)
        self.tic=time.time()
        #print("SARSA agent initialized:"+str(state))

    def getAction(self):
        self.step = self.step + 1
        ac = 'up down left right'.split()[self.action]
        #print("Action taken:"+ac)
        return ac

    def decideAction(self,state):
        r = random.random()
        if r<self.epsilon:
            action = random.randint(0, 3)
        else:
            action=np.argmax(self.Q[state])
        return action

    def observe(self, newState, reward, event):
        self.cumRew+=reward
        q=time.time()
        next_action = self.decideAction(newState)
        delta = reward + (self.gamma*self.Q[newState][next_action]) - self.Q[self.state][self.action] 
        self.e[self.state][self.action]=1     #replacing traces
        #self.e[self.state][self.action]+=1     #accumulating traces
        b=time.time()
        for s in range(self.numStates):
            for a in range(4):
                self.Q[s][a]=self.Q[s][a]+self.alpha*delta*self.e[s][a]
                self.e[s][a]=self.gamma*self.lamb*self.e[s][a]
        self.state=newState
        self.action=next_action
        c=time.time()
        #print("Observe Time: {0},{1}".format(b-q,c-b))
        #print("SARSA Observed reward:"+str(reward)+"newState:"+str(newState))
        if event!='continue':
            # if time.time()-self.tic>2:
            #     print("Episode No."+str(self.episodes)+", Reward:"+str(self.cumRew)+", Time taken:{:.3f}".format(time.time()-self.tic))
            # elif self.episodes%10==0:
            #     print(".")
            #print("Episode No."+str(self.episodes)+", Reward:"+str(self.cumRew)+", Time taken:{:.3f}".format(time.time()-self.tic))
            self.step=0
            self.state=self.init_state
            self.e=np.zeros((self.numStates,4))
            self.action = self.decideAction(self.state)
            self.episodes+=1
            self.cumRew=0
            self.tic=time.time()
            if self.episodes>50 and self.epsilon>=0.05:
                self.epsilon-=0.001
            if self.episodes>50 and self.alpha>=0.5:
                self.alpha-=0.002
            # if event=='goal':
            #     for a in range(4):
            #         self.Q[newState][a]=0
            side=int(math.sqrt(self.numStates))
            m=np.amax(self.Q,axis=1)
            Pi=np.argmax(self.Q,axis=1)
            # if self.episodes%10==0:
            #     for y in range(side):
            #         print('  |', end='')
            #         for x in range(side):
            #             state = y*side + x
            #             print('{:.2f}{}|'.format(m[state],'u d l r'.split()[Pi[state]]), end='')
            #         print()
            # elif self.episodes%20==0:
            #     pass
            #     for y in range(side):
            #         print('  |', end='')
            #         for x in range(side):
            #             state = y*side + x
            #             print('{}|'.format('u d l r'.split()[Pi[state]]), end='')
            #         print() 

class Agent:
    def __init__(self, numStates, state, gamma, lamb, algorithm, randomseed):
        '''
        numStates: Number of states in the MDP
        state: The current state
        gamma: Discount factor
        lamb: Lambda for SARSA agent
        '''
        if algorithm == 'random':
            self.agent = RandomAgent()
        elif algorithm == 'qlearning':
            self.agent = QlearningAgent(numStates,state,gamma,randomseed)
        elif algorithm == 'sarsa':
            self.agent = SarsaAgent(numStates,state,gamma,lamb,randomseed)

    def getAction(self):
        '''returns the action to perform'''
        return self.agent.getAction()

    def observe(self, newState, reward, event):
        '''
        event:
            'continue'   -> The episode continues
            'terminated' -> The episode was terminated prematurely
            'goal'       -> The agent successfully reached the goal state
        '''
        self.agent.observe(newState, reward, event)

