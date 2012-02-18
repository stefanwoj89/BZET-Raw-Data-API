#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define DLLEXPORT extern "C" __declspec(dllexport)
DLLEXPORT char* set(char *set, int x){
	int bitIndex = x%8;
	set[x>>3] |= 1<<bitIndex;
	return set;
}
DLLEXPORT char* unset(char* set, int x, int len) {
	if ( (x>>3) > len-1){
		printf("Out of bounds");
		return set;
	}
	int bitIndex = x%8;
	set[x>>3] &= 1<<bitIndex^0xFF;
	return set;
}
DLLEXPORT char* flip(char* set,int x, int len){
	if ( (x>>3) > len-1){
			printf("Out of bounds");
			return set;
		}
	int bitIndex = x%8;
	set[x>>3] ^= 1<<bitIndex;
	return set;
}
DLLEXPORT char* invert(char* set, int len){
	for(int i = 0; i<len;i++)
	{
		set[i] ^=0xFF;
	}
	return set;
}
DLLEXPORT char* clear(char* set, int len){
	for(int i = 0; i<len; i++){
		set[i] = 0;
	}
	return set;
}
DLLEXPORT int count(char* set, int len){
	int count = 0;
	for(int i = 0; i<(len*8);i++)
	{
		int bitIndex = i%8;
		if(set[i>>3] & (1 << bitIndex))
			count++;
	}
	return count;

}
DLLEXPORT int first(char* set, int len){
	for(int i = 0; i<(len*8);i++)
	{
		int bitIndex = i%8;
		if(set[i>>3] & (1 << bitIndex ))
			return i;
	}
	return -1;

}
DLLEXPORT int last(char* set, int len){
	for(int i = (len*8)-1; i>=0; i--)
	{
			int bitIndex = i%8;
			if(set[i>>3] & (1 << bitIndex))
				return i;
	}
	return -1;
}
DLLEXPORT int test(char* set, int x, int len){
	if(x>>3 > (len-1))
		return 0;
	int bitIndex = x%8;
	if( set[x>>3] & (1 <<bitIndex))
		return 1;
	else
		return 0;

}
DLLEXPORT char* c_and(char* set1, char* set2, char* returnSet, int len){
	for(int i = 0; i<(len);i++){
		returnSet[i] = set1[i] & set2[i];
	}
	return returnSet;
}
DLLEXPORT char* c_or(char* set1, char* set2, char* returnSet, int len){
	for(int i = 0; i<(len); i++){
	returnSet[i] = set1[i] | set2[i]; //is this the correct most efficient way to do this?
	}
	return returnSet;
}
DLLEXPORT char* c_xor(char* set1, char* set2, char* returnSet, int len){
	for(int i = 0; i<(len); i++){
	returnSet[i] = set1[i] ^ set2[i]; //is this the correct most efficient way to do this?
	}
	return returnSet;
}
DLLEXPORT int c_eq(unsigned char* set1,unsigned char* set2, int len){
	int is_equal = 0;
	for(int i = 0; i<(len); i++){
		is_equal += (set1[i] ^ set2[i]);
		//printf("set1 is %i, set2 is %i, is equal is %i \n",set1[i],set2[i],is_equal);
	}
	if(is_equal > 0)
		return 0;
	else
		return 1;
}
