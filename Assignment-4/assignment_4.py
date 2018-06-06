import sys
import numpy as np
import random
import matplotlib.pyplot as plt

exp,N = np.array(sys.argv[1:3],dtype=np.int)
lamb = float(sys.argv[3])
w = np.array(sys.argv[4:],dtype=np.float)

print "Experiment:",exp,"\tN:",N,"\tLambda:",lamb,"\n"

x=[]
x.append([2,0,0,0,0,0,1])			#s1 -> 2w1+w7
x.append([0,2,0,0,0,0,1])			#s2 -> 2w2+w7
x.append([0,0,2,0,0,0,1])			#s3 -> 2w3+w7
x.append([0,0,0,2,0,0,1])			#s4 -> 2w4+w7
x.append([0,0,0,0,2,0,1])			#s5 -> 2w5+w7
x.append([0,0,0,0,0,1,2])			#s6 -> 2w7+w6
x.append([0,0,0,0,0,0,0])			#value of terminal state = 0
x=np.array(x,dtype=np.float)
# Value function vector = sum(x*w,axis=1)

# For code, si corresponds to x[i-1]

# print w
# print x
# print np.sum(x*w,axis=1)

gamma=0.99
alpha=0.001

def next_state(s):
	if s<5:
		return 5
	elif s==5:
		if random.random()<0.99:
			return 5
			#remains in same state
		else:
			return 6
			#terminal state


plot=False

if exp==1:
	V = np.sum(x*w,axis=1)
	
	if plot:
		V_all = []
		V_all.append(np.sum(x*w,axis=1))
	
	for i in range(N):
		s = i%6
		s_prime = next_state(s)
		w = w + alpha*(gamma*V[s_prime]-V[s])*x[s]
		V = np.sum(x*w,axis=1)

		# print V[0],V[1],V[2],V[3],V[4],V[5]
		
		# print w

		if i%50000==0:
			print w
			print V
			print 

		if plot:
			V_all.append(V)
	
	if plot:
		V_all=np.array(V_all)
		# print V_all.shape
		# print V_all
		print "Plotting graph..."

		x=range(N+1)
		plt.figure()
		plt.plot(x,V_all[:,0],x,V_all[:,1],x,V_all[:,2],x,V_all[:,3],x,V_all[:,4],x,V_all[:,5])
		plt.title('Experiment 1 \n Estimated value of state vs number of updates')
		plt.xlabel('Number of updates')
		plt.ylabel('Estimated value of state')
		plt.legend(('S1','S2','S3','S4','S5','S6'))
		plt.show()

elif exp==2:
	if plot:
		w_ori = w

		l=[0,0.2,0.4,0.6,0.8,1.0]
		V_all=[]
		for lamb in l:
			print "Running simulation for lambda:",lamb
			w=w_ori
			count=0
			s=random.randint(0,5)	
			e=np.zeros(w.shape)
			V = np.sum(x*w,axis=1)
			Val=[]
			Val.append(sum(V)/6)
			while count<N:
				s_prime = next_state(s)
				delta = gamma*V[s_prime]-V[s]
				e = gamma*lamb*e + x[s]
				w = w + alpha*delta*e
				V = np.sum(x*w,axis=1)
				if s_prime==6:
					s=random.randint(0,5)
					e=np.zeros(w.shape)
				else:
					s=s_prime
				
				count+=1

				Val.append(sum(V)/6)

			V_all.append(Val)

		V_all=np.array(V_all)

		x=range(N+1)
		plt.figure()
		plt.plot(x,V_all[0,:],x,V_all[1,:],x,V_all[2,:],x,V_all[3,:],x,V_all[4,:],x,V_all[5,:])
		plt.title('Experiment 2 \n Average Estimated value of states vs number of updates')
		plt.xlabel('Number of updates')
		plt.ylabel('Average estimated value of states')
		plt.legend(('lambda=0','lambda=0.2','lambda=0.4','lambda=0.6','lambda=0.8','lambda=1.0'))
		plt.show()


	else:
		count=0
		s=random.randint(0,5)	
		e=np.zeros(w.shape)
		V = np.sum(x*w,axis=1)
		while count<N:
			s_prime = next_state(s)
			delta = gamma*V[s_prime]-V[s]
			e = gamma*lamb*e + x[s]
			w = w + alpha*delta*e

			V = np.sum(x*w,axis=1)

			if s_prime==6:
				s=random.randint(0,5)
				e=np.zeros(w.shape)
			else:
				s=s_prime

			count+=1

			#print V[0],V[1],V[2],V[3],V[4],V[5]

			if count%50000==0:
				print w
				print V
				print 

		
