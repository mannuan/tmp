DEV=`echo s1-eth3`
cd /sys/devices/virtual/net/$DEV/statistics/;if [ $? -ne 0 ];then Clear;fi
rtpkt1=`cat rx_packets tx_packets | xargs | awk '{print $1,$2}'`
sentpkt_dropped1=`tc -s class show dev $DEV | grep 'pkt' | tr -cd ' [0-9]' | awk '{print $2,$3}'`
sleep 1
rtpkt2=`cat rx_packets tx_packets | xargs | awk '{print $1,$2}'`
sentpkt_dropped2=`tc -s class show dev $DEV | grep 'pkt' | tr -cd ' [0-9]' | awk '{print $2,$3}'`

loss=`echo $rtpkt1 $sentpkt_dropped1 $rtpkt2 $sentpkt_dropped2`;
echo $loss
