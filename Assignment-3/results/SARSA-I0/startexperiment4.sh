

for((n=7;n<8;n++))
do
    echo "----------------    SARSA \0.2 $n    ------------------"
    python3 ../.././server/server.py -port $((7300+$n)) -i 0 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i0_lambda0.2_$n.txt" &
    sleep 1
    python3 ../.././client/client.py -port $((7300+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.2
done


for((n=5;n<6;n++))
do
    echo "----------------    SARSA \0.6 $n    ------------------"
    python3 ../.././server/server.py -port $((7300+$n)) -i 0 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i0_lambda0.6_$n.txt" &
    sleep 1
    python3 ../.././client/client.py -port $((7300+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.6
done


for((n=1;n<2;n++))
do
    echo "----------------    SARSA \0 $n    ------------------"
    python3 ../.././server/server.py -port $((7300+$n)) -i 0 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i0_lambda0_$n.txt" &
    sleep 1
    python3 ../.././client/client.py -port $((7300+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0
done


for((n=38;n<39;n++))
do
    echo "----------------    SARSA \1.0 $n    ------------------"
    python3 ../.././server/server.py -port $((7300+$n)) -i 0 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i0_lambda1.0_$n.txt" &
    sleep 1
    python3 ../.././client/client.py -port $((7300+$n)) -rs $n -gamma 1 -algo sarsa -lambda 1.0
done

for((n=65;n<68;n++))
do
    echo "----------------    SARSA \1.0 $n    ------------------"
    python3 ../.././server/server.py -port $((7300+$n)) -i 0 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i0_lambda1.0_$n.txt" &
    sleep 1
    python3 ../.././client/client.py -port $((7300+$n)) -rs $n -gamma 0.99 -algo sarsa -lambda 1.0
done
