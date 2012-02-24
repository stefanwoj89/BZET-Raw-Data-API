#!/usr/bin/env python3
# vi: ts=4 sw=4 et ai sm
# This version does not violate pythons byte stuff.
# It just makes copies.
from struct import *
from ctypes import *
import sys
import struct
from   os.path import dirname

bzetv = "v0.7"     # your version number
vdate = "12-02-20" # date of the version

lib = cdll.LoadLibrary('./_raw.so') #uncomment this to run in linux

dlldir = dirname(__file__)
# print( "DLL Directory:", dlldir )
dlldir.replace( '\\', '\\\\' )
# print( "DLL File:", dlldir+'\\_raw.dll' )
#lib = cdll.LoadLibrary(dlldir+'\\_raw.dll')

PBZ = c_void_p
ULL = c_ulonglong
LL  = c_longlong

# Bzet Set a bit Operation
RAWset = lib.set
RAWset.argtypes = [ PBZ, ULL ]
RAWset.restype  = None

# Bzet Unset a bit Operation
RAWunset = lib.unset
RAWunset.argtypes = [ PBZ, ULL ]
RAWunset.restype  = None

# Bzet Flip a bit Operation
RAWflip = lib.flip
RAWflip.argtypes = [ PBZ, ULL ]
RAWflip.restype  = None

# Bzet Invert Bits Operation (In place)
RAWinvert = lib.invert
RAWinvert.argtypes = [ PBZ, ULL ]
RAWinvert.restype  = None

# Bzet Count Bits Operation
RAWcount = lib.count
RAWcount.argtypes = [ PBZ, ULL ]
RAWcount.restype  = ULL

# Bzet Find First Bit Operation
RAWfirst = lib.first
RAWfirst.argtypes = [ PBZ, ULL ]
RAWfirst.restype  = LL

# Bzet Find Last Bit Operation
RAWlast = lib.last
RAWlast.argtypes = [ PBZ, LL ]
RAWlast.restype  = LL

# Bzet Test bit Operations
RAWtest = lib.test
RAWtest.argtypes = [ PBZ, ULL, ULL ]
RAWtest.restype  = c_int

# Bzet And Operations
RAWc_and = lib.c_and
RAWc_and.argtypes = [ PBZ, PBZ, PBZ, ULL ]
RAWc_and.restype  = None

# Bzet Or Operations
RAWc_or = lib.c_or
RAWc_or.argtypes = [ PBZ, PBZ, PBZ, ULL ]
RAWc_or.restype  = None

# Bzet Xor Operations
RAWc_xor = lib.c_xor
RAWc_xor.argtypes = [ PBZ, PBZ, PBZ, ULL ]
RAWc_xor.restype  = None

# Bzet EQ Operations
# Test if two bitsets are equal
RAWc_eq = lib.c_eq
RAWc_eq.argtypes = [ PBZ, PBZ, ULL ]
RAWc_eq.restype  = c_int


# This magic gets 2 or 3 for Python2.xx or Python3.xx
python_v = sys.version_info.major
# This magic tells if it is a 32 or 64 bit implementation
python_64bit = 8 * struct.calcsize("P") == 64

class Raw:
    @classmethod
    def BLevel(mymethod):
        return 0
    
    @classmethod
    def NewBLevel(mymethod,n):
        return
    
    @classmethod
    def Version(mymethod):        
        bv = "32"
        if python_64bit:
            bv = "64"
        return "RawC-" + bv + " " + bzetv + " BL0" + " " + vdate
    
    MT = ''          # a Bits value of the Empty Bitset
    tbits = type(3)  # the type Bits
    # This MTbytes is the internal Bits.v value
    MTbytes = b''
    # Type constants
    tbytes = type(bytes([]))
    tint   = type(3)
    tbarray= type(bytearray([]))
    tbool  = type(True)
    ttuple = type((0,))
    
    def getVal(self):
        return self.v
    
    def LEV(self):
        return 0
    
    def size(self):
            return len(self.v)
        
    def HEX(self):
        return str(self.v)
    
    def __repr__(self):
        r = 'L0 len=' + str(len(self.v))
        for i in range(len(self.v)):
            if i% 8 == 0: r += ' 0x'
            c = hex(self.v[i])[2:]
            if len(c) == 1: c = '0' + c
            r += c
            if (i+1)%16 == 0: r += '\n        '
            
        if r[-1] == '\n': r = r[:-1]
        return r

    @staticmethod
    def HEX( pbs ): return __repr__(pbs)

    def __len__(self): return len(self.v) * 8

    def __bool__(self): return bool( len(_normalize_(self.v)) )

    def __getitem__(self,ix):
        if ix < 0: raise error
        return self.TEST(ix)

    def __setitem__(self, ix, val):
        if ix < 0: raise error
        bval = bool(val)
        if bval:
            self.SET(ix)
        else:
            self.UNSET(ix)
        return self

    def __eq__(self,other):
        return self.EQ(other)

    def __ne__(self,other):
        return not self.EQ(other)
        
    def __or__    (self,other): return self.OR(other)
    def __and__   (self,other): return self.AND(other)
    def __xor__   (self,other): return self.XOR(other)
    def __invert__(self):       return self.INVERT()
    def __ior__   (self,other): return self.OR(other)
    def __iand__  (self,other): return self.AND(other)
    def __ixor__  (self,other): return self.XOR(other)
    
    def SET(self,x):
        if x < 0 : raise LookupError
        slen = self.size()
        copy = ''
        if x>>3 > slen-1:
            count = (x>>3) - (slen-1);
            copy = create_string_buffer(self.v, self.size()+count)
        else:
            copy = create_string_buffer(self.v, self.size())
        RAWset( byref(copy), x )
        self.v = bytes(copy.raw[:])
        return self
    
    def UNSET(self,x):
        if x < 0 : raise LookupError
        copy = create_string_buffer(self.v, self.size())
        RAWunset( byref(copy), x, self.size() )
        self.v = bytes(copy.raw)
        return self
    
    def FLIP(self,x):
        if x < 0 : raise LookupError
        copy = create_string_buffer(self.v, self.size())
        RAWflip( byref(copy), x, self.size() )
        self.v = bytes(copy.raw)
        return self
    
    def INVERT(self):
        copy = create_string_buffer(self.v, self.size())
        RAWinvert( byref(copy),self.size() )
        self.v = bytes(copy.raw)
        return self
    
    def NOT(self):
        copy = create_string_buffer(self.v, self.size())
        RAWinvert( byref(copy),self.size() )
        r = Raw(None)
        r.v = bytes(copy.raw)
        return r
    
    def CLEAR(self):
        self.v = MTbytes
        return self
    
    def COUNT(self):
        return RAWcount(self.v, self.size())
    
    def FIRST(self):
        return RAWfirst(self.v, self.size())
            
    def LAST(self):
        return RAWlast(self.v, self.size())
    
    def LIST_T(self,dstart=0,limit=None):
        top = limit
        if limit == None: top = len(self)
        c = 0
        for x in range(dstart,len(self)):
            if self.TEST(x):
                c += 1
                yield x
                if c >= top: return
        return
    
    @staticmethod
    def _align_(bset1, bset2 ):
        numBytes = bset1.size() - bset2.size()
        absNumBytes = abs(numBytes)
        copy1 = bset1.v[:] 
        copy2 = bset2.v[:]
        r1 = Raw(1)
        r2 = Raw(1)
        if bset1.size() > bset2.size():
            copy2 += bytes(absNumBytes)
        else :
            copy1 += bytes(absNumBytes)
        r1.v = copy1[:]
        r2.v = copy2[:]
        return r1,r2

    @staticmethod
    def _normalize_( bitset ):
        # Remove unneccessary zeros at the end of the bitset        
        # Check for length 0 empty or nothing to do.
        bslen = len(bitset)
        if bslen == 0:   return Raw.MTbytes
        done = -1
        for i in range(bslen-1,-1,-1):
            if bitset[i]:
                done = i
                break
        if done == -1:      return Raw.MTbytes
        if done == bslen-1: return bitset
        return bytes(bitset[:done])
            
    def TEST(self,x):
        return bool( RAWtest( self.v, x, self.size()) )
    
    def RANGE(s,n):
        # s is index of first bit
        # n is number of bits after that to set
        # OK this works now you can fix it to make it efficient
        if n < 0: raise range_error
        if s < 0: raise index_error
        size = s + n  # In bits
        bsize = size>>3
        if size & 0x7: bsize += 1
        r = Raw(None)
        #     size in bytes
        r.v = bytes( bsize )
        for x in range(s,s+n):
            r.SET(x)                  
        return r
    
    def AND(self,bset2):
        r1,r2 = self._align_(self,bset2)
        r3 = create_string_buffer(r1.size())
        RAWc_and( r1.v, r2.v, byref(r3), r1.size() )
        r = Raw(None)
        r.v = Raw._normalize_(r3.raw)
        return r

    def OR(self,bset2):
        r1,r2 = self._align_(self,bset2)
        r3 = create_string_buffer(r1.size())
        RAWc_or( r1.v, r2.v, byref(r3), r1.size() )
        r = Raw(None)
        r.v = Raw._normalize_(r3.raw)
        return r
    
    def XOR(self,bset2):
        r1,r2 = self._align_(self,bset2)
        r3 = create_string_buffer(r1.size())
        RAWc_xor( r1.v, r2.v, byref(r3), r1.size() )
        r = Raw(None)
        r.v = Raw._normalize_(r3.raw)
        return r
    
    def EQ(self,bset2):
        set1,set2 = self._align_(self,bset2)
        return bool( RAWc_eq( set1.v, set2.v, set1.size()) )
    
    def lengthen(self,length):
        self.v += bytes(length-self.size())
        
    @staticmethod
    def _int_(n):
        copy = create_string_buffer((n>>3)+1)
        RAWset( byref(copy), n )
        newByte = bytes(copy.raw)
        return newByte

    def __init__(self, x):
        if x == None:                 self.v = Raw.MTbytes        
        elif type(x) == self.tbytes:  self.v = x[:]
        elif type(x) == self.tbarray: self.v = bytes(x[:])
        elif type(x) == self.tint:    self.v = Raw._int_(x)
        elif type(x) == type([]):
            r = self.MT
            for ix in x:
                if type(ix) == self.tint:
                    r = r.OR( Raw(ix) )
                elif type(ix) == self.ttuple and len(ix) == 2:
                    s = ix[0] if ix[0] < ix[1] else ix[1]
                    n = abs( ix[1]-ix[0] )
                    if n > 1:
                        x = Raw.RANGE(s,n)
                        r = r.OR( x )
                    else:
                        r = r.OR( Raw(s) )
                else: raise error
            self.v = r.v
        elif type(x) == self.tbits:   raise error
        else: raise error
        return

Raw.MT    = Raw(None)
Raw.tbits = type(Raw(None))
    
if __name__ =="__main__":
    def Bitb(x):
        y = Raw(bytes(x))
        return y

    print( '\n\n' + Raw.Version() )
    
    ##################################
    #                                #
    #           Test Cases           #
    #                                #
    ##################################

    
    #Test if instantiation is working correctly.

    #Test empty set return
    bset1 = Raw(None)
    print("Argument 'None' returns: ", bset1.getVal())
    
    # Test if Integer argument returns
    # bitset with index of integer value turned on
    bset1 = Raw([(1,100)])
    bset2 = Raw([(1,100)])
    print("Bset1 (1-100) is          ", bset1 )
    print("Bset2 (1-100) is          ", bset2 )

    bset1.INVERT()
    print("Invert bset1 returns:     ", bset1 )
    bset1.FLIP(1)
    print("Flip 1 of bset1 returns:  ", bset1 )
    bset1.UNSET(2)
    print("Unset 2 of bset1 returns: ", bset1 )
    print("bset1 now is:             ", bset1 )
    bset1.COUNT()
    print("Count of bset1 returns:   ", bset1.COUNT() )
    bset1.LAST()
    print("Last of bset1 returns:    ", bset1.LAST() )
    bset1.FIRST()
    print("First of bset1 returns:   ", bset1.FIRST() )
    andResult = bset1.AND(bset2)
    print("bset1 AND bset2 returns:  ", andResult )
    orResult = bset1.OR(bset2)
    print("bset1 OR bset2 returns:   ", orResult )   
    xorResult = bset1.XOR(bset2)
    print("bset1 XOR bset2 returns:  ", xorResult )
    eqResult = bset1.EQ(bset2)
    print("bset1 EQ bset2 returns:   ", eqResult )
    for i in range (0,1000):
        bset1.INVERT()
        bset1.FLIP(1)
        bset1.UNSET(2)
        bset1.COUNT()
        bset1.LAST()
        bset1.FIRST()
        andResult = bset1.AND(bset2)
        orResult = bset1.OR(bset2)
        xorResult = bset1.XOR(bset2)
        eqResult = bset1.EQ(bset2)


    #Test if Integer list argument turns on specified bits
    bset1 = Raw([7,15])
    print("Argument '[7,15]' returns: ", bset1 )
    #Test if tuple sets all bits inclusively on
    bset1 = Raw([(7,15)])
    print("Argument '(7,15)' returns: ",bset1 )
    print("bits set for argument '(7,15)' returns: ",bset1 )
    #Test if a spec list argument is setting bits on
    bset2 = Raw([2,30,50, (50,100),101])
    print("Argument '[2,30,50, (50,100),101]' returns: ",bset2 )
    print("bits set for argument '[2,30,50, (50,100),101]' returns: ",
          [x for x in bset2.LIST_T()] )
    
    #####################################
    #                                   #
    #      Test Binary Operations       #
    #                                   #
    #####################################

    
    bset1 = Raw(0)
    bset2 = Raw(1)
    andBset = bset1.AND(bset2)
    print("And result of x01(01) and x02(10): ",andBset )
    orBset = bset1.OR(bset2)
    print("OR result of x01(01) and x02(10): ", orBset )
    bset1 = Raw([0,1,2])
    bset2 = Raw([0])
    xorBset = bset1.XOR(bset2)
    print("XOR result of x01(01) and x02(10): ", xorBset )
    bset1 = Raw([(5,10)])
    bset2 = Raw([(5,10)])
    eqBset = bset1.EQ(bset2)
    print("EQ result of same instantiation: ", eqBset )
    bset1 = Raw([(5,10)])
    bset2 = Raw([(5,10),300])
    eqBset = bset1.EQ(bset2)
    print("EQ result of different instantiation: ", eqBset )
    
