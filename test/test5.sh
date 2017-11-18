START=`date +%s%N`;
sleep 1;
END=`date +%s%N`;
time=$((END-START))
time=`expr $time / 1000`
echo $time us
