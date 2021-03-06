from pulp import *
import random
import math
from itertools import combinations, chain


#initialize
filename="/home/goutham/Desktop/CS-747/Assignment-2/data/MDP2.txt"
algorithm="lp"
batchsize=5
randomseed=1

def get_mdp(printinp,filename):
    fp = open(filename)
    S = int(fp.readline())
    A = int(fp.readline())
    R = [[0.0 for x in range(A)] for y in range(S)]
    T = [[0.0 for x in range(A)] for y in range(S)]
    #reading R
    for s in range(0, S):
        for a in range(0, A):
            line = fp.readline()
            R[s][a]=[float(x) for x in line.split()]
            #for sPrime in range(0, S):
            #	R[s][a][sPrime] = tmp[sPrime]
    #reading T
    for s in range(0, S):
        for a in range(0, A):
            line = fp.readline()
            T[s][a]=[float(x) for x in line.split()]
    gamma = float(fp.readline())
    fp.close()

    if printinp==1:
        print "S:",S
        print "A:",A
        print "R:"
        for s in range(0, S):
            for a in range(0, A):
                print "State:"+str(s)+", Action:"+str(a)+" ->",
                for sPrime in range(0, S):
                    print str(R[s][a][sPrime]) + " ",
                print "\n",   
        print "T:"
        for s in range(0, S):
            for a in range(0, A):
                print "State:"+str(s)+", Action:"+str(a)+" ->",
                for sPrime in range(0, S):
                    print str(T[s][a][sPrime]) + " ",
                print "\n",
        print "Discount:",gamma
    return S,A,R,T,gamma

def find_Pi(S,A,R,T,gamma,V):
    Pi = range(S)
    for s in range(S):
        Pi[s]=0
        tmp_max_val = sum([T[s][0][sPrime]*(R[s][0][sPrime]+gamma*V[sPrime]) for sPrime in range(S)])
        for a in range(1,A):
            tmp=sum([T[s][a][sPrime]*(R[s][a][sPrime]+gamma*V[sPrime]) for sPrime in range(S)])
            if tmp>tmp_max_val:
                Pi[s]=a
                tmp_max_val=tmp
    return Pi

def find_V(S,A,R,T,gamma,Pi):
    V = [0 for i in range(S)]
    count = 0
    while True:
        flag=True
        V1 = [V[i] for i in range(S)]
        count+=1
        #print count
        for s in range(S):
            V[s]=sum([T[s][Pi[s]][sPrime]*(R[s][Pi[s]][sPrime]+gamma*V[sPrime]) for sPrime in range(S)])
            if abs(V1[s]-V[s])>0.00000001:
                flag=False
        if flag or count>10000:
            break
        else:
            V1=V
    return V

def find_Q(S,A,R,T,gamma,V):
    Q = [[0.0 for x in range(A)] for y in range(S)]
    for s in range(S):
        for a in range(A):
            Q[s][a]=sum([T[s][a][sPrime]*(R[s][a][sPrime]+gamma*V[sPrime]) for sPrime in range(S)])
    return Q

S,A,R,T,gamma = get_mdp(0,filename)

if algorithm=="lp":
    prob = LpProblem("MDP",LpMaximize)
    lamb=[]
    for s in range(S):
        tmp=[]
        for a in range(A):
            tmp.append(LpVariable("lamb"+str(str(s)+","+str(a))))
        lamb.append(tmp)
    objective=0
    for s in range(S):
        for a in range(A):
            for sPrime in range(S):
                objective += lamb[s][a]*T[s][a][sPrime]*R[s][a][sPrime]    
    prob += objective,"Expected Discounted Reward"
    count=0
    for sPrime in range(S):
        prob += lpSum([lamb[sPrime][aPrime] for aPrime in range(A)]) == 1 + lpSum([[(T[s][a][sPrime]*gamma*lamb[s][a]) for a in range(A)] for s in range(S)]), "Constraint"+str(count)
        count +=1
    #print prob
    #prob.writeLP("MDP.lp")
    prob.solve()
    #print("Status:", LpStatus[prob.status])
    Pi_opt = find_Pi(S,A,R,T,gamma,V_opt)
    l=[]
    tmp=[]
    for v in prob.variables():
        V_opt.append(float(v.varValue))
        #print(v.name, "=", v.varValue)
    
    #V2 = find_V(S,A,R,T,gamma,Pi_opt)
    for s in range(S):
        print "{0:.8f}".format(V_opt[s]),Pi_opt[s]
        #print V2[s],Pi_opt[s]

#All policy iteration code has been written for 2-action MDPs
elif algorithm=="hpi":
    Pi = [0 for i in range(S)]
    V = find_V(S,A,R,T,gamma,Pi)
    count=0
    while True: 
        count=count+1
        Q = find_Q(S,A,R,T,gamma,V)
        Improvable = [0 for i in range(S)]
        imp_states = []
        for s in range(S):
            if Q[s][abs(Pi[s]-1)]>Q[s][Pi[s]]:
                Improvable[s]=1
                imp_states.append(s)
        print Pi
        print V
        print imp_states
        if sum(Improvable)==0:
            break
        else:
            for i in imp_states:
                Pi[i] = abs(Pi[i]-1)
            V = find_V(S,A,R,T,gamma,Pi)
    for s in range(S):
        print "{0:.8f}".format(V[s]),Pi[s]
elif algorithm=="rpi":
    Pi = [0 for i in range(S)]
    V = find_V(S,A,R,T,gamma,Pi)
    random.seed(randomseed)
    count=0
    while True:
        count+=1 
        Q = find_Q(S,A,R,T,gamma,V)
        Improvable = [0 for i in range(S)]
        imp_states = []
        for s in range(S):
            if Q[s][abs(Pi[s]-1)]>Q[s][Pi[s]]:
                Improvable[s]=1
                imp_states.append(s)
        if sum(Improvable)==0:
            break
        else:
            #print imp_states
            states_flip=[] #random subset of states to flip
            for i in imp_states:
                random_index = random.randrange(0,2)
                if random_index==1:
                    states_flip.append(i)
            #print "Index:",random_index
            #print "Element:",all_subsets[random_index]
            for i in states_flip:
                #print i
                Pi[i] = abs(Pi[i]-1)
            V = find_V(S,A,R,T,gamma,Pi)
        #print Pi
        #print V
    for s in range(S):
        print "{0:.8f}".format(V[s]),Pi[s]
elif algorithm=="bspi":
    Pi = [0 for i in range(S)]
    V = find_V(S,A,R,T,gamma,Pi)
    count=0
    while True:
        count+=1 
        Q = find_Q(S,A,R,T,gamma,V)
        Improvable = [0 for i in range(S)]
        imp_states = []
        for s in range(S):
            if Q[s][abs(Pi[s]-1)]>Q[s][Pi[s]]:
                Improvable[s]=1
                imp_states.append(s)
        if sum(Improvable)==0:
            break
        else:
            #print "Imp states",imp_states
            cur_ind = int((math.ceil(float(S)/batchsize))*batchsize-1)
            flag=False
            while True:
                #print "Cur:",cur_ind
                states_flip=[]
                for i in range(cur_ind,max(-1,cur_ind-batchsize),-1):
                    if i in imp_states:
                        states_flip.append(i)
                        flag=True
                if flag:
                    break
                else:
                    cur_ind = cur_ind - batchsize
                if cur_ind<0: #sanity check
                    break
            #print "Flip:",states_flip
            for i in states_flip:
                Pi[i] = abs(Pi[i]-1)
            V = find_V(S,A,R,T,gamma,Pi)
        #print "Pi:",Pi
        #print V
    for s in range(S):
        print "{0:.8f}".format(V[s]),Pi[s]

print "Iterations:",count