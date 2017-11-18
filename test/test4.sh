DEV=$1
setdelay=`tc -s qdisc show dev $DEV | grep 'delay' | sed 's/^.*delay //g' | sed 's/ .*$//g' | sed 's/us/ us/g' | sed 's/ms/ ms/g' | sed 's/s/ s/g' | sed 's/u/1/g' |sed 's/m/1000/g' | sed 's/s/1000000/g' | awk '{print $1*$2}'`
while true;do
sentpkt1=`tc -s class show dev $DEV | grep 'pkt' | tr -cd ' [0-9]' | awk '{print $2}'`
START=`date +%s%N`
while true;do
sentpkt2=`tc -s class show dev $DEV | grep 'pkt' | tr -cd ' [0-9]' | awk '{print $2}'`
END=`date +%s%N`
if [ $sentpkt2 -gt $sentpkt1 ];then
delay=$(awk 'BEGIN{ print ('$END'-'$START')/1000 }')
echo $delay
break
fi
done
done

