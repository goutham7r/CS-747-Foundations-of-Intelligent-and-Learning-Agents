# demonstrates how to call the server and the client
# modify according to your needs

mkdir results

for((n=0;n<1;n++))
do
    echo "----------------    lamb_1 \0 $n    ------------------"
    python3 ./server/server.py -port $((6000+$n)) -i 0 -rs 5 -nobf false -side 10 -ne 1000 -q | tee "results/lamb1_i0_rs$n.txt" &
    sleep 1
    ./startclient.sh -port $((6000+$n)) -rs $n -gamma 1 -algo qlearning -lambda 1.0
done
