#include <iostream>
using namespace std;
int mini(int n,double* x)
{
	double tmp = x[1];
	for(int i=1,k=1;i<=n;i++)
		if(x[i] < tmp){
			tmp = x[i];
			k=i;
		}
	return k;
}
int maxi(int n,double* x)
{
	T tmp = x[1];
	for(int i=1,k=1;i<=n;i++)
		if(x[i] > tmp){
			tmp = x[i];
			k = i;
		}
	return k;
}
double maxgap(int n,double* x)
{
	double minx = x[mini(n,x)],maxx = x[maxi(n,x)];
	int *count = new int[n+1];
	double *low = new double[n+1];
	double *high = new double[n+1];
	for(int i=1;i <= n-1;i++){
		count[i] = 0;
		low[i] = maxx;
		high[i] = minx;
	}
	for(i=1;i<=n;i++){
		int bucket = int((n-1)*(x[i]-minx)/(maxx-minx)) + 1;
		count[bucket]++;
		if(x[i]<low[bucket]) low[bucket] = x[i];
		if(x[i]>high[bucket]) high[bucket] = x[i];
	}
	double tmp = 0,left = high[1];
	for(i=2;i<=n-1;i++)
		if(count[i]){
			double thisgap = low[i] - left;
			if(thisgap > tmp) tmp=thisgap;
			left = high[i];
		}
	return tmp;
}
