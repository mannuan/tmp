DEV=$1
if [ $# -eq 1 ];then INTERVAL=1;remainbwfile="remainbw";delayfile="delay";jitterfile="jitter";lossfile="loss";qosoverlldpshfile="dynamic-qos.sh";path="/tmp/dynamic-qos_qosoverlldp/";else INTERVAL=$2;remainbwfile=$3;delayfile=$4;jitterfile=$5;lossfile=$6;qosoverlldpshfile=$7;path=$8;fi
Clear(){
rm -rf $path$DEV$remainbwfile $path$DEV$delayfile $path$DEV$jitterfile $path$DEV$lossfile $path$qosoverlldpshfile
if [ "`ls -A $path`" = "" ];then rm -rf $path;fi
break
}
while true;do
cd /sys/devices/virtual/net/$DEV/statistics/;if [ $? -ne 0 ];then Clear;fi
rtbit1=`cat rx_bytes tx_bytes | xargs | awk '{print ($1+$2)*8}'`
sentpkt_dropped1=`tc -s class show dev $DEV | grep 'pkt' | tr -cd ' [0-9]' | awk '{print $2,$3}'`
sleep $INTERVAL
rtbit2=`cat rx_bytes tx_bytes | xargs | awk '{print ($1+$2)*8}'`
sentpkt_dropped2=`tc -s class show dev $DEV | grep 'pkt' | tr -cd ' [0-9]' | awk '{print $2,$3}'`
setbw=`tc class show dev $DEV | grep 'rate' | sed 's/^.*rate //g' | sed 's/bit.*$//g' | sed 's/K/000/g' | sed 's/M/000000/g' | sed 's/G/000000000/g'`
occupybw=$(awk 'BEGIN{print int(('$rtbit2'-'$rtbit1')/('$INTERVAL'+0.1))}')
remainbw=$(awk 'BEGIN{if('$setbw'<'$occupybw') print 100; else print '$setbw'-'$occupybw'}');if [ $? -ne 0 ];then Clear;fi
pkt=`echo $sentpkt_dropped1 $sentpkt_dropped2 | awk '{print $3-$1}'`;if [ $? -ne 0 ];then Clear;fi
setloss=`tc -s qdisc show dev $DEV | grep 'loss' | tr -cd ' .[0-9]' | awk '{print $6}'`
loss=`echo $sentpkt_dropped1 $sentpkt_dropped2 | awk '{if(($3-$1)<=0) print 0; else print ($4-$2)/($4+$3-$2-$1)*100}'`;if [ $? -ne 0 ];then Clear;fi
loss=$(awk 'BEGIN{if('$loss'>'$setloss') print '$setloss'; else print '$loss'}')
setdelay=`tc -s qdisc show dev $DEV | grep 'delay' | sed 's/^.*delay //g' | sed 's/ .*$//g' | sed 's/us/ us/g' | sed 's/ms/ ms/g' | sed 's/s/ s/g' | sed 's/u/1/g' |sed 's/m/1000/g' | sed 's/s/1000000/g' | awk '{print $1*$2}'`
setjitter=`tc -s qdisc show dev $DEV | grep 'delay' | sed 's/^.*  //g' | sed 's/ .*$//g' | sed 's/us/ us/g' | sed 's/ms/ ms/g' | sed 's/s/ s/g' | sed 's/u/1/g' |sed 's/m/1000/g' | sed 's/s/1000000/g' | awk '{print $1*$2}'`
delay=$(awk 'BEGIN{if('$pkt'>0) print ('$INTERVAL'/'$pkt' )*1000000; else print 0}')
delay=$(awk 'BEGIN{if('$delay'>'$setdelay') print '$setdelay'; else print '$delay'}');if [ $? -ne 0 ];then Clear;fi
if [ -f "$path$DEV$jitterfile" ];then predelay=`cat $path$DEV$delayfile`;else predelay=0;fi
jitter=$(awk 'BEGIN{if('$delay' > '$predelay') print '$delay' - '$predelay'; else print '$predelay' - '$delay'}')
cd $path;if [ $? -ne 0 ];then Clear;fi
echo $remainbw > $DEV$remainbwfile;echo $loss > $DEV$lossfile;echo $delay > $DEV$delayfile;echo $jitter > $DEV$jitterfile
done
