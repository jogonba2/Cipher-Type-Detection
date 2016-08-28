#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from math import log
from random import randint

def get_streaks(binary_string,max_len_streaks):
    r,j = [],0
    aux_string = binary_string[:]
    while j<len(aux_string)-1:
	if aux_string[j]!=aux_string[j+1]:
	    r.append(aux_string[0:j+1])
	    aux_string = aux_string[j+1:]
	    j = 0
	else: j += 1
    if aux_string: r.append(aux_string)
    rn = [0.0 for i in xrange(max_len_streaks)]
    for i in xrange(len(r)):
	if len(r[i])<=max_len_streaks: rn[len(r[i])-1] += 1
    for i in xrange(len(rn)): rn[i] /= len(binary_string)
    return rn + [float(len(r))]
	    
def get_frequencies(binary_string):
    return [float(binary_string.count("0"))/len(binary_string),
	    float(binary_string.count("1"))/len(binary_string)]

def get_entropy(frequencies):
    return [(frequencies[0]*log(frequencies[0],2))+(frequencies[1]*log(frequencies[1],2))]

def get_bit_flips(binary_string):
    zero_to_one,one_to_zero,one_to_one,zero_to_zero = 0.0,0.0,0.0,0.0
    for i in xrange(len(binary_string)-1):
	if binary_string[i]=='0' and binary_string[i+1]=='0': zero_to_zero += 1
	elif binary_string[i]=='0' and binary_string[i+1]=='1': zero_to_one += 1
	elif binary_string[i]=='1' and binary_string[i+1]=='0': one_to_zero += 1
	else: one_to_one += 1
    return [zero_to_zero/len(binary_string),zero_to_one/len(binary_string),
	    one_to_zero/len(binary_string),one_to_one/len(binary_string)]

def get_self_correlation_sum(binary_string):
    correct,err,ac,t = 0.0,0.0,0.0,len(binary_string)
    for i in xrange(1,t):
	correct    = sum(map(lambda s: s[0]==s[1],zip(binary_string,binary_string[i:]+binary_string[:i])))
	err        = (len(binary_string)-correct)
	ac        += float(correct-err)/t
    return [ac/t]
