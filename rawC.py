#this version does not violate pythons byte stuff. it just makes copies.
from struct import *
from ctypes import *


#ExternalLib = cdll.LoadLibrary('api.dll') #uncomment this to run in windows
ExternalLib = cdll.LoadLibrary('./api.so') #uncomment this to run in linux
class Raw:
    MT = ''         # a Bits value of the Empty Bitset
    tbits = type(3)  # the type Bits
    # This MTbytes is the internal Bits.v value
    #MTbytes = bytes([0x00,0x00,0x00])
    MTbytes = bytes(0x00)
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
    def SET(self,x):
        if x < 0 : raise LookupError
        copy = create_string_buffer(self.v, self.size())
        if x>>3 > self.size()-1:
            count = (x>>3) - (self.size()-1);
            copy =  create_string_buffer(self.v,self.size()+count)
        ExternalLib.set(copy,x)
        #print(copy.value)
        self.v = bytes(copy)
        return self
    
    def UNSET(self,x):
        if x < 0 : raise LookupError
        copy = create_string_buffer(self.v, self.size())
        ExternalLib.unset(copy,x, self.size())
        self.v = bytes(copy)
        return self
    
    def FLIP(self,x):
        if x < 0 : raise LookupError
        copy = create_string_buffer(self.v, self.size())
        ExternalLib.flip(copy,x, self.size())
        self.v = bytes(copy)
        return self
    
    def INVERT(self):
        copy = create_string_buffer(self.v, self.size())
        ExternalLib.invert(copy,self.size())
        self.v = bytes(copy)
        return self
    
    def CLEAR(self):
        copy = create_string_buffer(self.v, self.size())
        ExternalLib.clear(copy, self.size())
        self.v = bytes(copy)
        return self
    
    def COUNT(self):
        return ExternalLib.count(self.v, self.size())
    
    def FIRST(self): #this is traverses the array left to right.
        return ExternalLib.first(self.v, self.size())
            
    def LAST(self): #traverse the array right to left, it is more efficient
        return ExternalLib.last(self.v, self.size())
    
    def LIST_T(self):
        trueList = []
        for x in range(0,self.size()*8):
            if self.TEST(x):
                trueList.append(x)
        return trueList
    
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
        return bool(ExternalLib.test(self.v,x,self.size()))
    def RANGE(s,n):
        r1 = Raw(None) #need to fix this and check abotu the whole None thing...
        for x in range(s,n+1):
            r1.SET(x)
        return r1
    def AND(self,bset2):
        r1,r2 = self._align_(self,bset2)
        r3 = Raw(None)
        r3.lengthen(r1.size())
        ExternalLib.c_and(r1.v, r2.v,r3.v,r1.size())
        return r3


    def OR(self,bset2):
        r1,r2 = self._align_(self,bset2)
        r3 = Raw(None)
        r3.lengthen(r1.size())
        ExternalLib.c_or(r1.v, r2.v,r3.v,r1.size())
        return r3
    
    def XOR(self,bset2):
        r1,r2 = self._align_(self,bset2)
        r3 = Raw(None)
        r3.lengthen(r1.size())
        ExternalLib.c_xor(r1.v, r2.v,r3.v,r1.size())
        return r3
    
    def EQ(self,bset2):
        set1,set2 = self._align_(self,bset2)
        #print(set1.v,set2.v)
        isEqual = bool(ExternalLib.c_eq(set1.v,set2.v,set1.size()))
        return isEqual
    
    def lengthen(self,length):
        self.v += bytes(length-self.size())
        
    @staticmethod
    def _int_(n):
        copy = create_string_buffer((n>>3)+1)
        ExternalLib.set(copy,n)
        newByte = bytes(copy)
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
                    n = abs( ix[1])
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
    ##################################
    #                                #
    #           Test Cases           #
    #                                #
    ##################################

    
    #Test if instantiation is working correctly.

    #Test empty set return
    #bset1 = Raw(None)
    #print("Argument 'None' returns: ",bset1.getVal())
    #Test if Integer argument returns bitset with index of integer value turned on
    bset1 = Raw([(1,10000)])
    bset2 = Raw([(1,10000)])

    bset1.INVERT()
    print("Comparison 1 returns: ",bset1.getVal())
    bset1.FLIP(1)
    print("Comparison 2 returns: ",bset1.getVal())
    bset1.UNSET(2)
    print("Comparison 3 returns: ",bset1.getVal())
    bset1.COUNT()
    print("Comparison 4 returns: ",bset1.getVal())
    bset1.LAST()
    print("Comparison 5 returns: ",bset1.getVal())
    bset1.FIRST()
    print("Comparison 6 returns: ",bset1.getVal())
    andResult = bset1.AND(bset2)
    print("Comparison 7 returns: ",andResult.getVal())
    orResult = bset1.OR(bset2)
    print("bset1 is:", bset1.getVal())
    print("bset2 is:", bset2.getVal())
    print("Comparison OR returns: ",orResult.getVal())
    xorResult = bset1.XOR(bset2)
    print("Comparison 9 returns: ",xorResult.getVal())
    eqResult = bset1.EQ(bset2)
    print("Comparison 10 returns: ",eqResult)
    for i in range (0,10000):
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
    print("Argument '[7,15]' returns: ",bset1.getVal())
    #Test if tuple sets all bits inclusively on
    bset1 = Raw([(7,15)])
    print("Argument '(7,15)' returns: ",bset1.getVal())
    print("bits set for argument '(7,15)' returns: ",bset1.LIST_T())
    #Test if a spec list argument is setting bits on
    bset2 = Raw([2,30,50, (50,100),101])
    print("Argument '[2,30,50, (50,100),101]' returns: ",bset2.getVal())
    print("bits set for argument '[2,30,50, (50,100),101]' returns: ",bset2.LIST_T())
    
    #####################################
    #                                   #
    #      Test Binary Operations       #
    #                                   #
    #####################################

    bset1 = Raw(0)
    bset2 = Raw(1)
    andBset = bset1.AND(bset2)
    print("And result of x01(01) and x02(10): ",andBset.getVal())
    orBset = bset1.OR(bset2)
    print("OR result of x01(01) and x02(10): ", orBset.getVal())
    bset1 = Raw([0,1,2])
    bset2 = Raw([0])
    xorBset = bset1.XOR(bset2)
    print("XOR result of x01(01) and x02(10): ", xorBset.getVal())
    bset1 = Raw([(5,10)])
    bset2 = Raw([(5,10)])
    eqBset = bset1.EQ(bset2)
    print("EQ result of same instantiation: ", eqBset)
    bset1 = Raw([(5,10)])
    bset2 = Raw([(5,10),300])
    eqBset = bset1.EQ(bset2)
    print("EQ result of different instantiation: ", eqBset)
    
