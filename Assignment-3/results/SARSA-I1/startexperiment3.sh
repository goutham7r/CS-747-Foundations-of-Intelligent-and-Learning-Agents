for((n=0;n<50;n++))
do
    echo "----------------    SARSA \0.7 $n    ------------------"
    python3 ../.././server/server.py -port $((7200+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda0.7_$n.txt" &
    sleep 1
    python3 ../.././client/client.py -port $((7200+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.7
done

for((n=0;n<50;n++))
do
    echo "----------------    SARSA \0.9 $n    ------------------"
    python3 ../.././server/server.py -port $((7200+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda0.9_$n.txt" &
    sleep 1
    python3 ../.././client/client.py -port $((7200+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.9
done
