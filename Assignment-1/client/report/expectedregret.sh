#!/bin/bash

#bash script used for simulation to calculate expected regret

PWD=`pwd`

horizon=100000
port=5001
nRuns=100
hostname="localhost"
banditFile="$PWD/data/instance-5.txt"

algorithm="UCB"
# Allowed values for algorithm parameter(case-sensitive)
# 1. epsilon-greedy 
# 2. UCB 
# 3. KL-UCB 
# 4. Thompson-Sampling
# 5. rr

epsilon=0.1

SERVERDIR=./server
CLIENTDIR=./client

OUTPUTFILE=$PWD/serverlog.txt

randomSeed=0

pushd $CLIENTDIR
echo "Experiment" >> output.txt
popd

for instance in {1..2}
do
	if [ $instance -eq 1 ]
	then
		banditFile="$PWD/data/instance-5.txt"
	else 
		banditFile="$PWD/data/instance-25.txt"
	fi

	numArms=$(wc -l $banditFile | cut -d" " -f1 | xargs)

	pushd $CLIENTDIR
	echo $banditFile >> output.txt
	popd

	for algo in {1..4}
	do
		if [ $algo -eq 1 ]
		then
			algorithm="epsilon-greedy"
		elif [ $algo -eq 2 ]
		then
			algorithm="UCB"
		elif [ $algo -eq 3 ]
		then
			algorithm="KL-UCB"
		else 
			algorithm="Thompson-Sampling"
		fi


		pushd $CLIENTDIR
		echo $algorithm >> output.txt
		echo $horizon >> output.txt
		echo "  " >> output.txt
		popd

		for run in {1..100}
		do
			randomSeed=$((1 + RANDOM % 10000))

			pushd $SERVERDIR
			cmd="./startserver.sh $numArms $horizon $port $banditFile $randomSeed $OUTPUTFILE &"
			echo $cmd
			$cmd 
			popd

			sleep 0.1	

			pushd $CLIENTDIR
			cmd="./startclient.sh $numArms $horizon $hostname $port $randomSeed $algorithm $epsilon&"
			echo $cmd
			$cmd >> output.txt
			popd
		done
	done
done

