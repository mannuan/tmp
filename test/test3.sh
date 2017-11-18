DEV=`echo s1-eth3`
tc -s qdisc show dev $DEV | grep 'loss' | tr -cd ' .[0-9]' | awk '{print $6}'
