import numpy as np
import glob
import matplotlib.pyplot as plt

lamb=[0,0.05,0.1,0.2,0.45,0.6,0.7,0.8,0.9,1.0]
sarsa_i1={}
all_txt=glob.glob("./results/SARSA-I1/*.txt")
for i in range(10):
	tmp={}
	for j in range(50):
		s="./results/SARSA-I1/sarsa_accum_i1_lambda"+str(lamb[i])+"_"+str(j)+".txt"
		if s in all_txt:
			#print "Read",s
			f=open(s,'r')
			l=f.readline()[:-2].split(',')
			#print len(l)
			if len(l)==750:
				tmp[j]=l
			f.close()
	sarsa_i1[lamb[i]]=tmp

avg_rew_in_epi_i1={}

for i in lamb:
	print i,len(sarsa_i1[i])
	tmp=np.zeros(750)
	for j in sarsa_i1[i]:
		#print np.array(sarsa_i1[i][j]).shape
		tmp+=np.array(sarsa_i1[i][j],type).astype(int)
	if len(sarsa_i1[i])>0:
		tmp/=len(sarsa_i1[i])
	avg_rew_in_epi_i1[i]=tmp

cum_500_i1=[]
for i in lamb:
	q=np.array(avg_rew_in_epi_i1[i])
	cum_500_i1.append(sum(q[:500]))

print cum_500_i1
plt.figure()
plt.plot(lamb,cum_500_i1)
plt.title('Cumulative Reward for 500 Episodes vs Lambda \n Instance 1')
plt.xlabel('Lambda')
plt.ylabel('Cumulative Reward')
#plt.show()


lamb=[0,0.05,0.1,0.2,0.45,0.6,0.7,0.8,0.9,1.0]
sarsa_i0={}
all_txt=glob.glob("./results/SARSA-I0/*.txt")
for i in range(10):
	tmp={}
	for j in range(50):
		s="./results/SARSA-I0/sarsa_accum_i0_lambda"+str(lamb[i])+"_"+str(j)+".txt"
		if s in all_txt:
			#print "Read",s
			f=open(s,'r')
			l=f.readline()[:-2].split(',')
			#print len(l)
			if len(l)==750:
				tmp[j]=l
			f.close()
	sarsa_i0[lamb[i]]=tmp

avg_rew_in_epi_i0={}

for i in lamb:
	print i,len(sarsa_i0[i])
	tmp=np.zeros(750)
	for j in sarsa_i0[i]:
		#print np.array(sarsa_i0[i][j]).shape
		tmp+=np.array(sarsa_i0[i][j],type).astype(int)
	if len(sarsa_i0[i])>0:
		tmp/=len(sarsa_i0[i])
	avg_rew_in_epi_i0[i]=tmp

cum_500_i0=[]
for i in lamb:
	q=np.array(avg_rew_in_epi_i0[i])
	cum_500_i0.append(sum(q[:500]))

print cum_500_i0
plt.figure()
plt.plot(lamb,cum_500_i0)
plt.title('Cumulative Reward for 500 Episodes vs Lambda \n Instance 0')
plt.xlabel('Lambda')
plt.ylabel('Cumulative Reward')
#plt.show()

qlearn_i0={}
all_txt=glob.glob("./results/Q-learning/*.txt")
q_avg_i0=np.zeros(750)
for j in range(50):
	s="./results/Q-learning/qlearning_i0_"+str(j)+".txt"
	if s in all_txt:
		#print "Read",s
		f=open(s,'r')
		l=f.readline()[:-2].split(',')
		#print len(l)
		if len(l)==750:
			qlearn_i0[j]=l
			q_avg_i0+=np.array(qlearn_i0[j],type).astype(int)
		f.close()
q_avg_i0/=50

qlearn_i1={}
all_txt=glob.glob("./results/Q-learning/*.txt")
q_avg_i1=np.zeros(750)
for j in range(50):
	s="./results/Q-learning/qlearning_i1_"+str(j)+".txt"
	if s in all_txt:
		#print "Read",s
		f=open(s,'r')
		l=f.readline()[:-2].split(',')
		#print len(l)
		if len(l)==750:
			qlearn_i1[j]=l
			q_avg_i1+=np.array(qlearn_i1[j],type).astype(int)
		f.close()
q_avg_i1/=50

x=300
best_i1=0.9
plt.figure()
plt.plot(range(x),avg_rew_in_epi_i1[best_i1][:x],range(x),q_avg_i1[:x])
plt.title('Expected Reward in Episode \n Instance 1')
plt.xlabel('Episode')
plt.ylabel('Expected Reward')
plt.legend(('Sarsa('+str(best_i1)+')','Q-learning'))
##plt.show()

best_i0=0.9
plt.figure()
plt.plot(range(x),avg_rew_in_epi_i0[best_i0][:x],range(x),q_avg_i0[:x])
plt.title('Expected Reward in Episode \n Instance 0')
plt.xlabel('Episode')
plt.ylabel('Expected Reward')
plt.legend(('Sarsa('+str(best_i0)+')','Q-learning'))
#plt.show()

best_i1=0.9
best_i0=0.9
avg_cum_rew_i0={}
avg_cum_rew_i1={}
for i in lamb:
	avg_cum_rew_i0[i]=np.cumsum(np.array(avg_rew_in_epi_i0[best_i0]))/np.array(range(1,751))
	avg_cum_rew_i1[i]=np.cumsum(np.array(avg_rew_in_epi_i1[best_i1]))/np.array(range(1,751))

q_avg_cum_i1=np.cumsum(q_avg_i1)/np.array(range(1,751))
q_avg_cum_i0=np.cumsum(q_avg_i0)/np.array(range(1,751))


x=400
plt.figure()
plt.plot(range(x),avg_cum_rew_i1[best_i1][:x],range(x),q_avg_cum_i1[:x])
plt.title('Cumulative Reward/Episodes \n Instance 1')
plt.xlabel('Episodes')
plt.ylabel('Cumulative Reward/Episodes')
plt.legend(('Sarsa('+str(best_i1)+')','Q-learning'))
#plt.show()

plt.figure()
plt.plot(range(x),avg_cum_rew_i0[best_i0][:x],range(x),q_avg_cum_i0[:x])
plt.title('Cumulative Reward/Episodes \n Instance 0')
plt.xlabel('Episode')
plt.ylabel('Cumulative Reward/Episodes')
plt.legend(('Sarsa('+str(best_i0)+')','Q-learning'))
plt.show()