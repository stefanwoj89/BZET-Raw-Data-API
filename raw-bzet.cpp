#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define DLLEXPORT extern "C" __declspec(dllexport)
#define ull unsigned int
#define GetBit(set,index)   set[index>>3] &  0x80>>(index & 0x07)
#define SetBit(set,index)   set[index>>3] |= 0x80>>(index & 0x07)
#define UnSetBit(set,index) set[index>>3] &= (0x80>>(index & 0x07)) ^ 0xff

DLLEXPORT void set(char *set, ull x){
	// If it's out of bounds don't you need to extend the set?
	SetBit(set,x);
	return;
}

DLLEXPORT void unset(char* set, ull x) {
	// If it's out of bounds it is already zero so why check?
	// Just return
	UnSetBit(set,x);
	return;
}

DLLEXPORT void flip(char* set, ull x){
	// If the current bit is 0 and out of bounds shouldn't
	// you extend the set and flip the bit?
	if ( GetBit(set,x) )
		UnSetBit(set,x);
	else SetBit(set,x);
	return;
}

DLLEXPORT void invert(char* set, ull len){
	for(ull i = 0; i<len;i++)
	{	set[i] ^= 0xFF;
	}
	return;
}

//DLLEXPORT char* clear(char* set, ull len){
//	for(ull i = 0; i<len; i++){
//		set[i] = 0;
//	}
//	return set;
//}

DLLEXPORT ull count(char* set, ull len){
	ull count = 0;
	for(ull i = 0; i<(len*8); i++)
	{	if( GetBit(set,i) )	count++;
	}
	return count;

}

DLLEXPORT ull first(char* set, const ull len){
	for(ull i = 0; i<(len*8); i++)
	{	if( GetBit(set,i) )	return i;
	}
	return -1;
}

DLLEXPORT ull last(char* set, const ull len){
	for(ull i = (len*8)-1; i>=0; i--)
	{	if ( GetBit(set,i) ) return i;
	}
	return -1;
}

DLLEXPORT int test(char* set, ull x, ull len){
	if(x>>3 > (len-1))
		return 0;
	if ( GetBit(set,x) )
		 return 1;
	else return 0;

}

// The most efficient way to do these operation is to index and pick up either 4 or 8 bytes
// at a time. Depennding on a 32 or 64 bit processor then use the native register width
// operations. You should also get the byte alignment right.  But this will do for the moment.

DLLEXPORT void c_and(char* set1, char* set2, char* returnSet, ull len){
	for(ull i = 0; i<(len);i++){
		returnSet[i] = set1[i] & set2[i];
	}
	return;
}

DLLEXPORT void c_or(char* set1, char* set2, char* returnSet, ull len){
	for(ull i = 0; i<(len); i++){
		returnSet[i] = set1[i] | set2[i];
	}
	return;
}

DLLEXPORT void c_xor(char* set1, char* set2, char* returnSet, ull len){
	for(ull i = 0; i<(len); i++){
		returnSet[i] = set1[i] ^ set2[i];
	}
	return;
}

DLLEXPORT int c_eq(unsigned char* set1,unsigned char* set2, ull len){
	for(ull i = 0; i<(len); i++){
		if ( set1[i]!= set2[i] ) return 0;
	}
	return 1;
}
