difficulty=$(curl -sS -X POST http://127.0.0.1:18081/json_rpc -d'{"jsonrpc":"2.0","id":"0","method":"getblock","params":{"height":1583841}}' -H 'Content-Type: application/json' | jq '.result .block_header .difficulty')

nonce=$(curl -sS -X POST http://127.0.0.1:18081/json_rpc -d'{"jsonrpc":"2.0","id":"0","method":"getblock","params":{"height":1583841}}' -H 'Content-Type: application/json' | jq '.result .block_header .nonce')

prevhash=$(curl -sS -X POST http://127.0.0.1:18081/json_rpc -d'{"jsonrpc":"2.0","id":"0","method":"getblock","params":{"height":1583841}}' -H 'Content-Type: application/json' | jq '.result .block_header .prev_hash')