DEV=$1
cd /sys/devices/virtual/net/$DEV/statistics/
rtbyte1=`cat rx_bytes tx_bytes | xargs`
