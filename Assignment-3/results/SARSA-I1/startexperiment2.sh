for((n=0;n<50;n++))
do
    echo "----------------    SARSA \0.2 $n    ------------------"
    python3 ../.././server/server.py -port $((7100+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda0.2_$n.txt" &
    sleep 1
    python3 ../.././client/client.py -port $((7100+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.2
done

for((n=0;n<50;n++))
do
    echo "----------------    SARSA \0.45 $n    ------------------"
    python3 ../.././server/server.py -port $((7100+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda0.45_$n.txt" &
    sleep 1
    python3 ../.././client/client.py -port $((7100+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.45
done

for((n=0;n<50;n++))
do
    echo "----------------    SARSA \0.6 $n    ------------------"
    python3 ../.././server/server.py -port $((7100+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda0.6_$n.txt" &
    sleep 1
    python3 ../.././client/client.py -port $((7100+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.6
done


