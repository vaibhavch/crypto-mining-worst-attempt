num=$(curl 'http://192.168.64.2/index.php?d=agents&c=agents&m=get_new_requests&last_request_id=0' -X POST -H 'Origin: http://192.168.64.2' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36' -H 'Accept: application/json, text/plain, */*' -H 'Referer: http://192.168.64.2/index.php?d=agents&c=agents' -H 'Cookie: PHPSESSID=a752bf38df115bc3c4ee06504bc195d7; pRjWu3Ox_session=b655e528b3cf5833bd832e3c74c16a17cb0b6f33' -H 'Connection: keep-alive' -H 'Content-Length: 0' --compressed | jq '.data .new_requests' | grep -o '[0-9]\+')
echo $num
if [[ $num -gt 0 ]];
	echo -e "\a"