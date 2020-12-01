# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 14:23:07 2018

@author: 565637
"""

mystring = "6/1/2018"
number = int.from_bytes(mystring.encode('utf-8'), 'little')
print ("Encoded : ", number)
recoveredstring = number.to_bytes((number.bit_length() + 7) // 8, 'little').decode('utf-8')
print ("recoveredstring >> ", recoveredstring)
