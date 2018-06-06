for((n=0;n<50;n++))
do
    echo "----------------    SARSA \0 $n    ------------------"
    python3 ../.././server/server.py -port $((7000+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda0_$n.txt" &
    sleep 1
    python3 ../.././client/client.py -port $((7000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0
done

for((n=0;n<50;n++))
do
    echo "----------------    SARSA \0.05 $n    ------------------"
    python3 ../.././server/server.py -port $((7000+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda0.05_$n.txt" &
    sleep 1
    python3 ../.././client/client.py -port $((7000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.05
done

for((n=0;n<50;n++))
do
    echo "----------------    SARSA \0.1 $n    ------------------"
    python3 ../.././server/server.py -port $((7000+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda0.1_$n.txt" &
    sleep 1
    python3 ../.././client/client.py -port $((7000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.1
done
