#!/bin/bash

mdp=$1
#echo $mdp

if [[ $mdp != "--mdp" ]]
then
	echo "Error, need --mdp"
	exit
fi

filepath=$2

alg=$3

if [[ $alg != "--algorithm" ]]
then
	echo "Error, need --algorithm"
	exit
fi

algo=$4


if [[ $algo == "lp" ]]
then
	batchsize=5
	randomseed=0
elif [[ $algo == "hpi" ]]
then
	batchsize=5
	randomseed=0
elif [[ $algo == "rpi" ]]
then
	rs=$5
	if [[ $rs == "--randomseed" ]]
	then
		batchsize=5
		randomseed=$6
	elif [[ $rs == "--batchsize" ]]
	then
		batchsize=$6
		rs=$7
		randomseed=$8
		if [[ $rs != "--randomseed" ]]
		then
			echo "Error, need --randomseed"
			exit
		fi
	else
		echo "Error, need --randomseed"
			exit
	fi
elif [[ $algo == "bspi" ]]
then
	bs=$5
	if [[ $bs == "--batchsize" ]]
	then
		batchsize=$6
		randomseed=0
	elif [[ $bs == "--randomseed" ]]
	then
		batchsize=$8
		bs=$7
		randomseed=$6
		if [[ $bs != "--batchsize" ]]
		then
			echo "Error, need --batchsize"
			exit
		fi
	else
		echo "Error, need --batchsize"
			exit
	fi
else
	echo "Enter valid algorithm name"
	exit
fi

chmod +x mdp.py
cmd="python ./mdp.py $filepath $algo $randomseed $batchsize"
#echo $cmd
$cmd