

mkdir results

for((n=0;n<13;n++))
do
    echo "----------------    SARSA \0 $n    ------------------"
    python3 ./server/server.py -port $((7000+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda0_$n.txt" &
    sleep 1
    python3 ./client/client.py -port $((7000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0
done

for((n=0;n<13;n++))
do
    echo "----------------    SARSA \0.05 $n    ------------------"
    python3 ./server/server.py -port $((7000+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda0.05_$n.txt" &
    sleep 1
    python3 ./client/client.py -port $((7000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.05
done

for((n=0;n<13;n++))
do
    echo "----------------    SARSA \0.1 $n    ------------------"
    python3 ./server/server.py -port $((7000+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda0.1_$n.txt" &
    sleep 1
    python3 ./client/client.py -port $((7000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.1
done

for((n=0;n<13;n++))
do
    echo "----------------    SARSA \0.45 $n    ------------------"
    python3 ./server/server.py -port $((7000+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda0.45_$n.txt" &
    sleep 1
    python3 ./client/client.py -port $((7000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.45
done

for((n=0;n<13;n++))
do
    echo "----------------    SARSA \0.6 $n    ------------------"
    python3 ./server/server.py -port $((7000+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda0.6_$n.txt" &
    sleep 1
    python3 ./client/client.py -port $((7000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.6
done

for((n=0;n<13;n++))
do
    echo "----------------    SARSA \0.7 $n    ------------------"
    python3 ./server/server.py -port $((7000+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda0.7_$n.txt" &
    sleep 1
    python3 ./client/client.py -port $((7000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.7
done

for((n=0;n<13;n++))
do
    echo "----------------    SARSA \0.8 $n    ------------------"
    python3 ./server/server.py -port $((7000+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda0.8_$n.txt" &
    sleep 1
    python3 ./client/client.py -port $((7000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.8
done

for((n=0;n<13;n++))
do
    echo "----------------    SARSA \0.9 $n    ------------------"
    python3 ./server/server.py -port $((7000+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda0.9_$n.txt" &
    sleep 1
    python3 ./client/client.py -port $((7000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.9
done

for((n=0;n<13;n++))
do
    echo "----------------    SARSA \1.0 $n    ------------------"
    python3 ./server/server.py -port $((7000+$n)) -i 1 -rs $n -ne 750 -side 32 -q | tee "sarsa_accum_i1_lambda1.0_$n.txt" &
    sleep 1
    python3 ./client/client.py -port $((7000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 1.0
done
