#删除奇数行
cat 3-2.txt | sed 's/[\:\;\(\)\<\>a-z]//g' | sed '1~2d' | sed 's/省/省 /g' | sed 's/市/市 /g' | sed 's/区/区 /g' | sed 's/县/县 /g' | sed 's/镇/镇 /g' | sed 's/乡/乡 /g' | sed 's/,/ /g'| sed 's/  / /g'| sed 's/ 乡/乡/g' | sed 's/街道/街道 /g' | sed 's/柳市 /柳市/g' | awk '{for(i=1;i<=NF-1;i++){printf("cross(name:cross;type:cross)<%s,%s>\n",$NF,$i);printf("crossed(name:crossed;type:crossed)<%s,%s>\n",$i,$NF);}}' > 1.txt