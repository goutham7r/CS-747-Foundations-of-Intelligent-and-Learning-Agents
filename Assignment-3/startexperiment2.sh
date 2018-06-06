

mkdir results

for((n=0;n<50;n++))
do
    echo "----------------    SARSA \0.2 $n    ------------------"
    python3 ./server/server.py -port $((6000+$n)) -i 0 -rs $n -ne 1600 -nobf false -side 32 -q | tee "sarsa_accum_lambda0.2_$n.txt" &
    sleep 1
    python3 ./client/client.py -port $((6000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.2
done