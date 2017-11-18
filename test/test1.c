#include <stdio.h>
#include <stdlib.h>
#define MAX 10000
float findmin(float data[],int n){/*寻找数据序列中的最小值*/
   int index,i;
   float min,temp;
   temp=data[0];
   for(i=1;i<n;i++){
     if(data[i]<temp){
       temp=data[i];
       index=i;
     }
   }
   min=data[index];
   return min;
}
float findmax(float data[],int n){/*寻找数据序列中的最大值*/
   int index,i;
   float max,temp;
   temp=data[0];
   for(i=1;i<n;i++){
     if(data[i]>temp){
       temp=data[i];
       index=i;
     }
   }
   max=data[index];
   return max;
}
void initial(int n,int count[],float low[],float high[],float min,float max){/*初始化区间*/
   int i;
   for(i=0;i<n;i++){
     count[i]=0; //区间是否有数据存入 
     low[i]=max; //将区间的左端赋值最大值 
     high[i]=min; //将区间的右端复制最小值 
   }
}
void dataIn(float m,int count[],float low[],float high[],int n,float data[],float min){/*将数据序列依次放入对应区间*/
	int i,location;
	for(i=0;i<n;i++){
	location = int((data[i]-min)/m)+1;//判断数据进入哪个区间:按照等分区间，数据与最小值的差与区间大小的比值+1就是区间编号
     if(location==n)
       location--;
     count[location]++; //有数据存入，计数值加1 
     if(data[i]<low[location]) //如果数据比左端值小，则作为左端值 
       low[location]=data[i];
     if(data[i]>high[location]) //如果数据比右端值大，则作为右端值 
       high[location]=data[i];
   }
}
float findMaxGap(int n,float low[],float high[],int count[]){ /*找出最大间隙，整个问题的核心*/
/*函数说明*/
/*上面已经把对应数据放入相应的区间，在之前可以知道，总共有n-1区间，相应的只有n-2个值，那么就一定有一个区间不会有数据*/
/*因为最大值与最小值已经分别被设为最小区间的左端值和最大区间的右端值，所以中间的n-1区间只有n-2个值*/
/*那么可以想象，最大间隙肯定不会是在一个区间中，而一定是在空区间的两端，
最大间隙为空区间右边相邻区间的左端值空区间左边相邻区间的右端值；有可能有多个这种情况，找出最大就行了*/
   int i;
   float maxgap,dhigh,temp;
   dhigh=high[1];
   for(i=2;i<n;i++){
     if(count[i]){
       temp=low[i]-dhigh;
       if(maxgap<temp)
         maxgap=temp;
       dhigh=high[i];
     }
   } 
   return maxgap;
}
int main(){
  float data[MAX];
  int n,i=0;
  float min,max;
  float m,maxgap;
  float low[MAX],high[MAX];
  int count[MAX];
  scanf("%d",&n);
  for(i=0;i<n;i++)
    scanf("%f",&data[i]);
  min=findmin(data,n);
  max=findmax(data,n);
  m=(max-min)/(n-1);
  initial(n,count,low,high,min,max);
  dataIn(m,count,low,high,n,data,min);
  maxgap=findMaxGap(n,low,high,count);
  printf("%.1f",maxgap);
  system("pause");
  return 0;
}
