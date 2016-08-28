#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import lowercase
from random import randint

def generate_random_string(n_bytes): 
    return "".join([lowercase[randint(0,len(lowercase)-1)] for i in xrange(n_bytes)])
    
def unzip_2d(samples):
    X,Y = [],[]
    for i in xrange(len(samples)): 
	X.append(samples[i][0])
	Y.append(samples[i][1])
    return X,Y

def get_x_separate_class(X,Y):
    X_0,X_1,X_2,X_3 = [],[],[],[]
    for i in xrange(len(Y)):
	if Y[i]==0:   X_0.append(X[i])
	elif Y[i]==1: X_1.append(X[i])
	elif Y[i]==2: X_2.append(X[i])
	elif Y[i]==3: X_3.append(X[i])
    return X_0,X_1,X_2,X_3  
