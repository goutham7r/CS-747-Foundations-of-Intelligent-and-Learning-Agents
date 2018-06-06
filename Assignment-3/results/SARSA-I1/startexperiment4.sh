for((n=0;n<50;n++))
do
    echo "----------------    SARSA \0.8 $n    ------------------"
    python3 ../.././server/server.py -port $((7300+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda0.8_$n.txt" &
    sleep 1
    python3 ../.././client/client.py -port $((7300+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.8
done

for((n=0;n<50;n++))
do
    echo "----------------    SARSA \1.0 $n    ------------------"
    python3 ../.././server/server.py -port $((7300+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda1.0_$n.txt" &
    sleep 1
    python3 ../.././client/client.py -port $((7300+$n)) -rs $n -gamma 1 -algo sarsa -lambda 1.0
done