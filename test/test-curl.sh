data=`cat test-curl.py`
curl -X POST -d "script=666666" "http://127.0.0.1:5000/debug/test2/save"
#curl "http://127.0.0.1:5000/debug/test2/save?script=123"
