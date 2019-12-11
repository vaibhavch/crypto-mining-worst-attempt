
START=1680000
END=1685583
 
for (( c=$START; c<=$END; c++ ))
do

 difficulty=$(curl -sS -X POST http://127.0.0.1:18081/json_rpc -d'{"jsonrpc":"2.0","id":"0","method":"getblock","params":{"height":'"$c"'}}' -H 'Content-Type: application/json' | jq '.result .block_header .difficulty')

 prevhash=$(curl -sS -X POST http://127.0.0.1:18081/json_rpc -d'{"jsonrpc":"2.0","id":"0","method":"getblock","params":{"height":'"$c"'}}' -H 'Content-Type: application/json' | jq '.result .block_header .prev_hash')

 timestamp=$(curl -sS -X POST http://127.0.0.1:18081/json_rpc -d'{"jsonrpc":"2.0","id":"0","method":"getblock","params":{"height":'"$c"'}}' -H 'Content-Type: application/json' | jq '.result .block_header .timestamp')

 txhash=$(curl -sS -X POST http://127.0.0.1:18081/json_rpc -d'{"jsonrpc":"2.0","id":"0","method":"getblock","params":{"height":'"$c"'}}' -H 'Content-Type: application/json' | jq '.result .miner_tx_hash')

 nonce=$(curl -sS -X POST http://127.0.0.1:18081/json_rpc -d'{"jsonrpc":"2.0","id":"0","method":"getblock","params":{"height":'"$c"'}}' -H 'Content-Type: application/json' | jq '.result .block_header .nonce')

 echo -n "$difficulty" | xxd -b | awk '{print $2}' | tr -d '\n'
 #echo "," | tr -d '\n'
 echo -n $timestamp | xxd -b | awk '{print $2}' | tr -d '\n'
 #echo "," | tr -d '\n'
 echo -n "$prevhash" | xxd -b | awk '{print $2}' | tr -d '\n'
 #echo "," | tr -d '\n'
 echo -n "$txhash" | xxd -b | awk '{print $2}' | tr -d '\n'
 echo "," | tr -d '\n'
 echo -n $nonce | xxd -b | awk '{print $2}' | tr -d '\n'
 #echo $nonce
 echo '\n'
	
done