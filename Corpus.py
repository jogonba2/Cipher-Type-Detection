#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Crypto.Cipher import AES,DES,ARC4,ARC2
from Crypto import Random
from Crypto.Util import Counter
from Utils import generate_random_string
from random import randint
import FeatureExtraction as fe
import numpy as np
import hashlib


def generate_synthetic_cipher_samples(n_samples,plaintext_bytes,max_streaks):
    synthetic_samples = []
    synthetic_classes = []

    for i in xrange(n_samples):
	plaintext = generate_random_string(plaintext_bytes)
	cipher    = randint(0,3)
	
	if cipher == 0:
	    keyword   = generate_random_string(16)
	    cipher = AES.new(keyword,AES.MODE_ECB)
	    synthetic_classes.append(0)
	    
	elif cipher == 1:
	    keyword   = generate_random_string(8)
	    cipher = DES.new(keyword,DES.MODE_ECB)
	    synthetic_classes.append(1)
	    
	elif cipher == 2:
	    keyword   = generate_random_string(16)
	    cipher = ARC4.new(keyword)
	    synthetic_classes.append(2)
	
	elif cipher == 3:
	    keyword   = generate_random_string(16)
	    cipher = ARC2.new(keyword)
	    synthetic_classes.append(3)
	    
	    
	ciphertext   = cipher.encrypt(plaintext)
		
	plaintext  = "".join(map(bin,bytearray(plaintext))).replace("0b","")
	keyword    = "".join(map(bin,bytearray(keyword))).replace("0b","")
	ciphertext = "".join(map(bin,bytearray(ciphertext))).replace("0b","")
	
	plaintext_length       = [len(plaintext)]
	keyword_length         = [len(keyword)]
	ciphertext_length      = [len(ciphertext)]
	
	plaintext_frequencies  = fe.get_frequencies(plaintext)
	keyword_frequencies    = fe.get_frequencies(keyword)
	ciphertext_frequencies = fe.get_frequencies(ciphertext)
		
	plaintext_entropy  = fe.get_entropy(plaintext_frequencies)
	keyword_entropy    = fe.get_entropy(keyword_frequencies)
	ciphertext_entropy = fe.get_entropy(ciphertext_frequencies)
	
	plaintext_bit_flips  = fe.get_bit_flips(plaintext)
	keyword_bit_flips    = fe.get_bit_flips(keyword)
	ciphertext_bit_flips = fe.get_bit_flips(ciphertext)
		
	plaintext_bit_flips  = fe.get_bit_flips(plaintext)
	keyword_bit_flips    = fe.get_bit_flips(keyword)
	ciphertext_bit_flips = fe.get_bit_flips(ciphertext)
		
	plaintext_self_correlation  = fe.get_self_correlation_sum(plaintext)
	keyword_self_correlation    = fe.get_self_correlation_sum(keyword)
	ciphertext_self_correlation = fe.get_self_correlation_sum(ciphertext)
	
	plaintext_streaks  = fe.get_streaks(plaintext,max_streaks)
	keyword_streaks    = fe.get_streaks(keyword,max_streaks)
	ciphertext_streaks = fe.get_streaks(ciphertext,max_streaks)
	
	synthetic_samples.append(np.array(plaintext_length + plaintext_frequencies + plaintext_entropy + plaintext_bit_flips + \
				 plaintext_self_correlation + plaintext_streaks + keyword_length + keyword_frequencies + \
				 keyword_entropy + keyword_bit_flips + keyword_self_correlation + \
				 keyword_streaks + ciphertext_length + ciphertext_frequencies + ciphertext_entropy + \
				 ciphertext_bit_flips + ciphertext_self_correlation + ciphertext_streaks))
				 
    return (np.array(synthetic_samples),np.array(synthetic_classes))

def generate_synthetic_hash_samples(n_samples,plaintext_bytes,max_streaks):
    synthetic_samples = []
    synthetic_classes = []
    hash_algorithms   = [("md5",0),("sha1",1),("sha224",3),("sha256",4),("sha384",5),("sha512",6),
			 ("ripemd160",7),("whirlpool",8),("md4",9)]
    
    for i in xrange(n_samples):
	plaintext  = generate_random_string(plaintext_bytes)
	algorithm  = hash_algorithms[randint(0,len(hash_algorithms)-1)]
	synthetic_classes.append(algorithm[1])
	algorithm  = hashlib.new(algorithm[0])
	algorithm.update(plaintext)
	hashedtext = algorithm.hexdigest()
	plaintext  = "".join(map(bin,bytearray(plaintext))).replace("0b","")
	hashedtext = "".join(map(bin,bytearray(hashedtext))).replace("0b","")
	
	plaintext_length       = [len(plaintext)]
	hashedtext_length      = [len(hashedtext)]
	
	plaintext_frequencies  = fe.get_frequencies(plaintext)
	hashedtext_frequencies = fe.get_frequencies(hashedtext)
		
	plaintext_entropy  = fe.get_entropy(plaintext_frequencies)
	hashedtext_entropy = fe.get_entropy(hashedtext_frequencies)
	
	plaintext_bit_flips  = fe.get_bit_flips(plaintext)
	hashedtext_bit_flips = fe.get_bit_flips(hashedtext)
		
	plaintext_bit_flips  = fe.get_bit_flips(plaintext)
	hashedtext_bit_flips = fe.get_bit_flips(hashedtext)
		
	plaintext_self_correlation  = fe.get_self_correlation_sum(plaintext)
	hashedtext_self_correlation = fe.get_self_correlation_sum(hashedtext)
	
	plaintext_streaks  = fe.get_streaks(plaintext,max_streaks)
	hashedtext_streaks = fe.get_streaks(hashedtext,max_streaks)
	
	synthetic_samples.append(np.array(plaintext_length + plaintext_frequencies + plaintext_entropy + \
				 plaintext_bit_flips + plaintext_self_correlation + plaintext_streaks + hashedtext_length + \
				 hashedtext_entropy + hashedtext_bit_flips + hashedtext_self_correlation + hashedtext_streaks))
				 
    return (np.array(synthetic_samples),np.array(synthetic_classes))
    
def generate_corpus(synthetic_samples,synthetic_classes,fname_train_samples,fname_train_classes,fname_test_samples,
		    fname_test_classes,percent_train=0.8):
			
    assert len(synthetic_samples) == len(synthetic_classes) and 0<=percent_train<=1
    p = np.random.permutation(len(synthetic_samples))
    synthetic_samples = synthetic_samples[p]
    synthetic_classes = synthetic_classes[p]
    np.savetxt(fname_train_samples,synthetic_samples[:int(percent_train*len(synthetic_samples))])
    np.savetxt(fname_train_classes,synthetic_classes[:int(percent_train*len(synthetic_samples))])
    np.savetxt(fname_test_samples,synthetic_samples[int(percent_train*len(synthetic_samples)):])
    np.savetxt(fname_test_classes,synthetic_classes[int(percent_train*len(synthetic_samples)):])

def load_corpus(fname_train_samples,fname_train_classes,fname_test_samples,fname_test_classes):
    X_train,Y_train = np.loadtxt(fname_train_samples),np.loadtxt(fname_train_classes)
    X_test,Y_test   = np.loadtxt(fname_test_samples),np.loadtxt(fname_test_classes)
    return (X_train,Y_train,X_test,Y_test)
