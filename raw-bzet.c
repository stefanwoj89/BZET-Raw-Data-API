#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define ull unsigned long long
#define GetBit(set,index)   set[index>>3] &  0x80>>(index & 0x07)
#define SetBit(set,index)   set[index>>3] |= 0x80>>(index & 0x07)
#define UnSetBit(set,index) set[index>>3] &= (0x80>>(index & 0x07)) ^ 0xff

void set(char *set, ull x) {
	SetBit(set,x);
	return;
}

 void unset(char* set, ull x) {
	UnSetBit(set,x);
	return;
}

 void flip(char* set, ull x) {
	if ( GetBit(set,x) )
		UnSetBit(set,x);
	else SetBit(set,x);
	return;
}

 void invert(char* set, ull len){
	for(ull i = 0; i<len;i++)
	{	set[i] ^= 0xFF;
	}
	return;
}

//                                           10    11    12     13   14    15
//                                         b1010 b1011 b1100 b1101 b1110 b1111
//                          x0 x1 x2 x3 x4 x5 x6 x7 x8 x9 xa xb xc xd xe xf
static char fourbits[16] = { 0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4 }; 

 ull count(char* set, const ull len){
	register ull count = 0;
	register char byte;
	for(ull i=0; i<=len; i++)
	{	byte = set[i];
		count += fourbits[(byte>>4)&0x0f] + fourbits[byte&0x0f]; }
	return count;

}

 long long first(char* set, const ull len){
	// Scan bytes for a bit
	ull i = 0;
	int found = 0;
	for( i=0; i<=len; i++)
	{	if ( set[i] ) {	found = 1; break; }
		}
	if ( !found ) return -1;

	// Scan this byte for a bit
	char byte = set[i];
	for( int j=0; j < 8; j++ )
	{	if( byte & (0x80 >>j) )	return i*8+j; }

	// This should never happen
	return -1;
}

 long long last(char* set, const long long len){
	if ( !len ) return -1;
	// Scan bytes for a bit
	long long rlen = len-1;
	long long i;
	int found = 0;
	for( i=rlen; i>=0; i--)
	{	if ( set[i] ) {	found = 1; break; }
		}
	if ( !found ) return -1;

	// Scan this byte for a bit
	char byte = set[i];
	for( int j=0; j < 8; j++ )
	{	if( byte & (0x80>>j) )	return i*8+j; }

	// This should never happen
	return -1;
}

 int test(char* set, ull x, const ull len){
	if ( x>>3 > (len-1))	 return 0;
	if ( GetBit(set,x) )	 return 1;
	else return 0;

}

// The most efficient way to do these operation is to index and pick up either 4 or 8 bytes
// at a time. Depennding on a 32 or 64 bit processor then use the native register width
// operations. You should also get the byte alignment right.  But this will do for the moment.

 void c_and(char* set1, char* set2, char* returnSet, ull len){
	for(ull i = 0; i<(len);i++){
		returnSet[i] = set1[i] & set2[i];
	}
	return;
}

 void c_or(char* set1, char* set2, char* returnSet, ull len){
	for(ull i = 0; i<(len); i++){
		returnSet[i] = set1[i] | set2[i];
	}
	return;
}

 void c_xor(char* set1, char* set2, char* returnSet, ull len){
	for(ull i = 0; i<(len); i++){
		returnSet[i] = set1[i] ^ set2[i]; 
	}
	return;
}

int c_eq(unsigned char* set1,unsigned char* set2, ull len){
	for(ull i = 0; i<(len); i++){
		if ( set1[i]!= set2[i] ) return 0;
	}
	return 1;
}
