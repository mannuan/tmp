DEV=$1
while true;do
	cd /sys/devices/virtual/net/$DEV/statistics/;if [ $? -ne 0 ];then break;fi
	rbyte1=`cat rx_bytes`;
	while true;do
		rbyte2=`cat rx_bytes`;
		START=`date +%s%N`;
		if [ $rbyte2 -gt $rbyte1 ];then break;fi;
	done
	cd /sys/devices/virtual/net/`echo $DEV|cut -c1-2`/statistics/;if [ $? -ne 0 ];then break;fi
	rbyte1=`cat rx_bytes`;
	while true;do
		rbyte2=`cat rx_bytes`;
		END=`date +%s%N`;
		if [ $rbyte2 -gt $rbyte1 ];then break;fi;
	done
	delay=$(awk 'BEGIN{ print ('$END'-'$START')/1000 }');
	echo $delay;
done
