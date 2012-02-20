#this version does not violate pythons byte stuff. it just makes copies.
from struct import *
from ctypes import *
import sys
import struct
from   os.path import dirname

#lib = cdll.LoadLibrary('./_raw.so') #uncomment this to run in linux

dlldir = dirname(__file__)
print( "DLL Directory:", dlldir )
dlldir.replace( '\\', '\\\\' )
print( "DLL File:", dlldir+'\\_raw.dll' )
lib = cdll.LoadLibrary(dlldir+'\\_raw.dll')

PBZ = c_void_p
ULL = c_ulonglong

# Bzet Set a bit Operation
RAWset = lib.set
RAWset.argtypes = [ PBZ, ULL ]
RAWset.restype  = None

# Bzet Unset a bit Operation
RAWunset = lib.unset
RAWunset.argtypes = [ PBZ, ULL]
RAWunset.restype  = None

# Bzet Flip a bit Operation
RAWflip = lib.flip
RAWflip.argtypes = [ PBZ, ULL]
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
RAWfirst.restype  = ULL

# Bzet Find Last Bit Operation
RAWlast = lib.last
RAWlast.argtypes = [ PBZ, ULL ]
RAWlast.restype  = ULL

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



bzetv = "v0.4stefan"  # your version number
vdate = "12-02-20" # date of the version

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
        return int( ceil(log2(len(self.v)*8)) )
    
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

    def __len__(self): return len(self.v) * 8
    
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
    
    def CLEAR(self):
        self.v = MTbytes
        return self
    
    def COUNT(self):
        return RAWcount(self.v, self.size())
    
    def FIRST(self): #this traverses the array left to right
        return RAWfirst(self.v, self.size())
            
    def LAST(self): #traverse the array right to left, it is more efficient
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
        r.v = bsize * bytes( '\x00', 'utf8' )
        print( "size is", len(r.v), "r is", r )
        for x in range(s,s+n):
            r.SET(x)                  
        return r
    
    def AND(self,bset2):
        r1,r2 = self._align_(self,bset2)
        r3 = create_string_buffer(r1.size())
        RAWc_and( r1.v, r2.v, byref(r3), r1.size() )
        r = Raw(None)
        r.v = bytes(r3.raw)
        return r

    def OR(self,bset2):
        r1,r2 = self._align_(self,bset2)
        r3 = create_string_buffer(r1.size())
        RAWc_or( r1.v, r2.v, byref(r3), r1.size() )
        r = Raw(None)
        r.v = bytes(r3.raw)
        return r
    
    def XOR(self,bset2):
        r1,r2 = self._align_(self,bset2)
        r3 = create_string_buffer(r1.size())
        RAWc_xor( r1.v, r2.v, byref(r3), r1.size() )
        r = Raw(None)
        r.v = bytes(r3.raw)
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
    
