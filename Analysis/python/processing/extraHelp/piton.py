#!/usr/bin/env python

x = 13  #1101
#print 'X = 13 or 1101' 
#print 'X>> ',x>>1
#print 'X<< ',x<<1

#print x &(1<<0)
#print x &(1<<1)
#print x &(1<<2)

for i in range(9):
        bite =  x & (1<<i)
        print i, bite
	#if bite >0:
		#print i, bite
