for((n=0;n<50;n++))
do
    echo "----------------    qlearning $n    ------------------"
    python3 ../.././server/server.py -port $((7000+$n)) -i 0 -rs $n -ne 750 -side 32 -q | tee "qlearning_i0_$n.txt" &
    sleep 1
    python3 ../.././client/client.py -port $((7000+$n)) -rs $n -gamma 1 -algo qlearning -lambda 0
done


for((n=0;n<50;n++))
do
    echo "----------------    qlearning $n    ------------------"
    python3 ../.././server/server.py -port $((7000+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "qlearning_i1_$n.txt" &
    sleep 1
    python3 ../.././client/client.py -port $((7000+$n)) -rs $n -gamma 1 -algo qlearning -lambda 0.45
done

