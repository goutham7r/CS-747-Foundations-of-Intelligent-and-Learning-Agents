from pulp import *
import random
import math


def get_mdp(S,A,printinp,randomseed):
    R = [[0.0 for x in range(A)] for y in range(S)]
    T = [[0.0 for x in range(A)] for y in range(S)]
    random.seed(randomseed)
    #creating R
    for s in range(0, S):
        for a in range(0, A):
            R[s][a]=[float("{0:.6f}".format(random.uniform(-1.0,1.0))) for x in range(S)]
    #creating T
    for s in range(0, S):
        for a in range(0, A):
            tmp=[random.random() for x in range(S)]
            T[s][a]=[float("{0:.3f}".format(tmp[i]/sum(tmp))) for i in range(S)]
    gamma = float("{0:.3f}".format(random.uniform(0.9,0.99)))

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
    prob = LpProblem("Finding V",LpMinimize)
    V1 = LpVariable.dicts("V",(range(S)))
    prob += 1,"Cost"
    count=0
    for s in range(S):
        prob += V1[s] == lpSum([(T[s][Pi[s]][sPrime]*(R[s][Pi[s]][sPrime]+gamma*V1[sPrime])) for sPrime in range(S)]), "Constraint"+str(count)
        count+=1
    prob.solve()
    V=[]
    for v in V1:
        V.append(float(V1[v].varValue))
    return V

def find_Q(S,A,R,T,gamma,V):
    Q = [[0.0 for x in range(A)] for y in range(S)]
    for s in range(S):
        for a in range(A):
            Q[s][a]=sum([T[s][a][sPrime]*(R[s][a][sPrime]+gamma*V[sPrime]) for sPrime in range(S)])
    return Q

def MDPI(S,A,R,T,gamma,algorithm,batchsize):
    if algorithm=="hpi":
        Pi = [0 for i in range(S)]
        V = find_V(S,A,R,T,gamma,Pi)
        count=0
        while True: 
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
                count=count+1
                for i in imp_states:
                    Pi[i] = abs(Pi[i]-1)
                V = find_V(S,A,R,T,gamma,Pi)
            #print Pi
            #print V
    elif algorithm=="rpi":
        Pi = [0 for i in range(S)]
        V = find_V(S,A,R,T,gamma,Pi)
        count=0
        while True:
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
                count+=1 
                #print imp_states
                while True:
                    states_flip=[] #random subset of states to flip
                    for i in imp_states:
                        random_index = random.randrange(0,2)
                        if random_index==1:
                            states_flip.append(i)
                    if len(states_flip)>0:
                        break
                #print "Index:",random_index
                #print "Element:",all_subsets[random_index]
                for i in states_flip:
                    #print i
                    Pi[i] = abs(Pi[i]-1)
                V = find_V(S,A,R,T,gamma,Pi)
            #print Pi
            #print V
    elif algorithm=="bspi":
        Pi = [0 for i in range(S)]
        V = find_V(S,A,R,T,gamma,Pi)
        count=0
        while True: 
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
                count+=1
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
            #print 
    #for s in range(S):
    #    print "{0:.8f}".format(V[s]),Pi[s]
    print algorithm,batchsize,count
    return count

algos = []
algos.append("hpi")
algos.append("rpi")
algos.append("bspi")
batchsizes_arr=[1,2,3,5,10,15,20,25,35,45]
HPI=[]
RPI=[]
BSPI=[]

for i in range(100):
    S,A,R,T,gamma = get_mdp(50,2,0,i)
    for j in range(3):
        print i,
        if j==0:
            HPI.append(MDPI(S,A,R,T,gamma,algos[j],5))
        elif j==1:
            RPI.append(MDPI(S,A,R,T,gamma,algos[j],5))
        elif j==2:
            tmp=[]
            for k in range(10):
                tmp.append(MDPI(S,A,R,T,gamma,algos[j],batchsizes_arr[k]))
            BSPI.append(tmp)
            print

print HPI
print RPI
print BSPI

f_hpi = open('hpi.txt', 'w')
f_rpi = open('rpi.txt', 'w')
f_bspi = open('bspi.txt', 'w')
out_hpi=""
out_rpi=""
out_bspi=""

for i in range(len(HPI)):
    out_hpi+=str(HPI[i])+"\n"
    out_rpi+=str(RPI[i])+"\n"
    tmp=""
    for j in range(len(BSPI[i])):
        tmp+=str(BSPI[i][j])+" "
    out_bspi += tmp+"\n"

f_hpi.write(out_hpi)
f_rpi.write(out_rpi)
f_bspi.write(out_bspi)