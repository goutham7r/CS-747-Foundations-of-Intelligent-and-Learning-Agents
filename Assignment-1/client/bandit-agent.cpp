#include <iostream>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <math.h>
#include <vector>
#include <random>
#include <string>

#include "gsl/gsl_rng.h"
#include "gsl/gsl_randist.h"

#include <boost/math/special_functions/beta.hpp>

#define MAXHOSTNAME 256

using namespace std;

void options(){

  cout << "Usage:\n";
  cout << "bandit-agent\n"; 
  cout << "\t[--numArms numArms]\n";
  cout << "\t[--randomSeed randomSeed]\n";
  cout << "\t[--horizon horizon]\n";
  cout << "\t[--hostname hostname]\n";
  cout << "\t[--port port]\n";
  cout << "\t[--algorithm algorithm]\n";
  cout << "\t[--epsilon epsilon]\n";

}


/*
  Read command line arguments, and set the ones that are passed (the others remain default.)
*/
bool setRunParameters(int argc, char *argv[], int &numArms, int &randomSeed, unsigned long int &horizon, string &hostname, int &port, string &algorithm, double &epsilon){

  int ctr = 1;
  while(ctr < argc){

    //cout << string(argv[ctr]) << "\n";

    if(string(argv[ctr]) == "--help"){
      return false;//This should print options and exit.
    }
    else if(string(argv[ctr]) == "--numArms"){
      if(ctr == (argc - 1)){
	return false;
      }
      numArms = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--randomSeed"){
      if(ctr == (argc - 1)){
	return false;
      }
      randomSeed = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--horizon"){
      if(ctr == (argc - 1)){
	return false;
      }
      horizon = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--hostname"){
      if(ctr == (argc - 1)){
	return false;
      }
      hostname = string(argv[ctr + 1]);
      ctr++;
    }
    else if(string(argv[ctr]) == "--port"){
      if(ctr == (argc - 1)){
	return false;
      }
      port = atoi(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else if(string(argv[ctr]) == "--algorithm"){
      if(ctr == (argc - 1)){
  return false;
      }
      algorithm = string(argv[ctr + 1]);
      ctr++;
    }
     else if(string(argv[ctr]) == "--epsilon"){
      if(ctr == (argc - 1)){
  return false;
      }
      epsilon = atof(string(argv[ctr + 1]).c_str());
      ctr++;
    }
    else{
      return false;
    }

    ctr++;
  }

  return true;
}

/* ============================================================================= */
/* Write your algorithms here */

double kl(double p, double q)
{
  if (p==0)
    return log2(1/(1-q));
  else if (p==1)
    return log2(1/q);
  else
    return (p*(log2(p/q))+(1-p)*(log2((1-p)/(1-q))));
}

double get_klucb_val(int s, int f, int t)
{
  int u = s+f;
  double p_hat = (double)s/u;
  //cout<<"Entered: "<<s<<" "<<f<<" "<<t<<"\n";
  double m = (log2(t)+ 3*(log2(log2(t))))/u;
  //cout<<"P_Hat="<<p_hat<<",    Max="<<m<<"\n";

  //Find max q such that KL(p_hat,q) is less than max using binary search
  double a,b,c; //upper and lower bounds for binary search for q
  a=p_hat;
  b=1;
  double val;
  double delta = 0.0000001; //margin of error
  int count=0;
  if (kl(p_hat,1)<=m)
      return 1;
  while(true)
  {
    count++;
    //cout<<"["<<a<<", "<<b<<"]"<<"\n";
    c=(a+b)/2;
    if((m-kl(p_hat,a))<delta)
    {
      //cout<<"Iterations:"<<count<<"\n";
      //cout<<a<<", KL: "<<kl(p_hat,a)<<"\n";
      //cout<<"P_Hat="<<p_hat<<",    Max="<<m<<"\n";
      return a; 
    }
    val=kl(p_hat,c);
    //cout<<"KL of "<<c<<"="<<val<<"\n";
    if(val>m)
      b=c;
    else
      a=c;
  }
}



int sampleArm(string algorithm, double epsilon, int pulls, float reward, int numArms, int *f, int *s)
{   
  double random;
  int armToPull=-1;

  double *temp = new double[numArms];
  for(int i=0;i<numArms;i++)
  {
    temp[i]=0;
  }

  if(algorithm.compare("rr") == 0)
  {
    armToPull = pulls % numArms;
  }
  else if(algorithm.compare("epsilon-greedy") == 0)
  {
    random = (double)rand()/(double)RAND_MAX;
    for(int i=0;i<numArms;i++)
    {
      if (s[i]+f[i]>0)  
        temp[i]=(double)s[i]/(s[i]+f[i]);
    }

    if(random<epsilon)
    { 
      //cout<<"Random pull, random="<<random<<"\n"<<"[";
      armToPull = (rand()%numArms);
    }
    else 
    {
      int max_arm=0;
      double max_prob_hat=temp[0];
      for(int i=1;i<numArms;i++)
      {
        if (temp[i]>max_prob_hat)  
        {
          max_prob_hat=temp[i];
          max_arm=i;
        }
      }
      //cout<<"Greedy pull:"<<random<<"\n"<<"[";
      armToPull=max_arm;
    }
    /*
    for(int i=0;i<numArms;i++)
    {
      cout<<s[i]<<" ";
    }
    cout<<"]"<<"       [";
    for(int i=0;i<numArms;i++)
    {
      cout<<f[i]<<" ";
    }
    cout<<"]"<<"       [";
    for(int i=0;i<numArms;i++)
    {
      cout<<temp[i]<<" ";
    }
    cout<<"]"<<"\n";
    */
  }
  else if(algorithm.compare("UCB") == 0)
  {
    for(int i=0;i<numArms;i++)
    {
      if ((s[i]+f[i]>0)&&(pulls>0))  
        temp[i]=((double)s[i]/(s[i]+f[i])) + sqrt((2*log2(pulls))/(s[i]+f[i]));
    }

    if(pulls<numArms)
      armToPull=pulls;
    else
    {
      int max_arm=0;
      double max_prob_hat=temp[0];
      for(int i=1;i<numArms;i++)
      {
        if (temp[i]>max_prob_hat)  
        {
          max_prob_hat=temp[i];
          max_arm=i;
        }
      }
      armToPull=max_arm;
    }
    /*
    cout<<"Arm Pulled: "<< armToPull<<"\n [";
    for(int i=0;i<numArms;i++)
    {
      cout<<s[i]<<" ";
    }
    cout<<"]"<<"       [";
    for(int i=0;i<numArms;i++)
    {
      cout<<f[i]<<" ";
    }
    cout<<"]"<<"       [";
    for(int i=0;i<numArms;i++)
    {
      cout<<temp[i]<<" ";
    }
    cout<<"]"<<"\n";
    */
  }
  else if(algorithm.compare("KL-UCB") == 0)
  {
    if(pulls<numArms)
      armToPull=pulls; //pull each arm atleast once before starting algorithm
    else
    {
      for(int i=0;i<numArms;i++)
      {
        //cout<<"Arm "<<i<<"\n";
        temp[i]=get_klucb_val(s[i],f[i],pulls);
      }

      int max_arm=0;
      double max_prob_hat=temp[0];
      for(int i=1;i<numArms;i++)
      {
        if (temp[i]>max_prob_hat)  
        {
          max_prob_hat=temp[i];
          max_arm=i;
        }
      }
      armToPull=max_arm;
    }
    cout<<"Arm Pulled: "<< armToPull<<"\n [";
    for(int i=0;i<numArms;i++)
    {
      cout<<s[i]<<" ";
    }
    cout<<"]"<<"       [";
    for(int i=0;i<numArms;i++)
    {
      cout<<f[i]<<" ";
    }
    cout<<"]"<<"       [";
    for(int i=0;i<numArms;i++)
    {
      cout<<temp[i]<<" ";
    }
    cout<<"]"<<"\n";
  }
  else if(algorithm.compare("Thompson-Sampling") == 0)
  {
    for(int i=0;i<numArms;i++)
    {
      random = (double)rand()/(double)RAND_MAX; //sample from uniform distribution
      temp[i]=boost::math::ibeta_inv(s[i]+1, f[i]+1, random);  //sample from beta distribution
    }
    int max_arm=0;
    double max_prob_hat=temp[0];
    for(int i=1;i<numArms;i++)
    {
      if (temp[i]>max_prob_hat)  
      {
        max_prob_hat=temp[i];
        max_arm=i;
      }
    }
    armToPull=max_arm;
    /*
    cout<<"Arm Pulled: "<< armToPull<<"\n [";
    for(int i=0;i<numArms;i++)
    {
      cout<<s[i]<<" ";
    }
    cout<<"]"<<"       [";
    for(int i=0;i<numArms;i++)
    {
      cout<<f[i]<<" ";
    }
    cout<<"]"<<"       [";
    for(int i=0;i<numArms;i++)
    {
      cout<<temp[i]<<" ";
    }
    cout<<"]"<<"\n";
    */
  }
  else
  {
    armToPull = -1;
  }
  delete temp;
  return armToPull;
}

/* ============================================================================= */


int main(int argc, char *argv[]){
  // Run Parameter defaults.
  int numArms = 5;
  int randomSeed = time(0);
  unsigned long int horizon = 200;
  string hostname = "localhost";
  int port = 5000;
  string algorithm="random";
  double epsilon=0.0;

  //Set from command line, if any.
  if(!(setRunParameters(argc, argv, numArms, randomSeed, horizon, hostname, port, algorithm, epsilon))){
    //Error parsing command line.
    options();
    return 1;
  }

  struct sockaddr_in remoteSocketInfo;
  struct hostent *hPtr;
  int socketHandle;

  bzero(&remoteSocketInfo, sizeof(sockaddr_in));
  
  if((hPtr = gethostbyname((char*)(hostname.c_str()))) == NULL){
    cerr << "System DNS name resolution not configured properly." << "\n";
    cerr << "Error number: " << ECONNREFUSED << "\n";
    exit(EXIT_FAILURE);
  }

  if((socketHandle = socket(AF_INET, SOCK_STREAM, 0)) < 0){
    close(socketHandle);
    exit(EXIT_FAILURE);
  }

  memcpy((char *)&remoteSocketInfo.sin_addr, hPtr->h_addr, hPtr->h_length);
  remoteSocketInfo.sin_family = AF_INET;
  remoteSocketInfo.sin_port = htons((u_short)port);

  if(connect(socketHandle, (struct sockaddr *)&remoteSocketInfo, sizeof(sockaddr_in)) < 0){
    //code added
    cout<<"connection problem"<<".\n";
    close(socketHandle);
    exit(EXIT_FAILURE);
  }


  char sendBuf[256];
  char recvBuf[256];

  int *s; //vector storing number of successes for each arm
  s = new int[numArms];
  int *f; //vector storing number of failures for each arm
  f = new int[numArms];
  for(int i=0;i<numArms;i++)
  {
    s[i]=0;
    f[i]=0;
  }
  srand(time(NULL));

  float total_reward=0;
  float reward = 0;
  unsigned long int pulls=0;
  int armToPull = sampleArm(algorithm, epsilon, pulls, reward, numArms, f, s);

  sprintf(sendBuf, "%d", armToPull);

  cout << "Sending action " << armToPull << ".\n";
  while(send(socketHandle, sendBuf, strlen(sendBuf)+1, MSG_NOSIGNAL) >= 0){

    char temp;
    recv(socketHandle, recvBuf, 256, 0);
    sscanf(recvBuf, "%f %c %lu", &reward, &temp, &pulls);
    cout << "Received reward " << reward << ".\n";
    cout<<"Num of  pulls "<<pulls<<".\n"<<"\n";
    if (reward==0)
      f[armToPull]++;
    else
      s[armToPull]++;
    total_reward = total_reward + reward;

    armToPull = sampleArm(algorithm, epsilon, pulls, reward, numArms, f, s);


    sprintf(sendBuf, "%d", armToPull);
    cout << "Sending action " << armToPull << ".\n";
  }
  
  close(socketHandle);

  cout << "Terminating.\n";
  cout<<total_reward<<"\n";  

  return 0;
}
          
