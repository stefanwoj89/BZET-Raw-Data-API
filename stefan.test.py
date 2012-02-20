from rawC import Raw
def Bitb(x):
    y = Raw(bytes(x))
    return y

print( '\n\n' + Raw.Version() )

##################################
#                                #
#           Test Cases           #
#                                #
##################################


# Test if instantiation is working correctly.

#Test empty set return
bset1 = Raw(None)
print("Argument 'None' returns: ", bset1 )

bset1 = Raw(0)
print("Argument '0' returns:    ", bset1 )

bset1 = Raw(20)
print("Argument '20' returns:   ", bset1 )

bset1 = Raw(100)
print("Argument '100' returns:  ", bset1 )

bset1 = Raw.RANGE(8,8)
print("Range(8,8) returns:      ", bset1 )

# Test if Integer argument returns
# bitset with index of integer value turned on
bset1 = Raw([(1,100)])
print("Bset1 (1-100) is          ", bset1 )
bset2 = Raw([(1,100)])
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
