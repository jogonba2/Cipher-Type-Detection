#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.svm import SVC,LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import numpy as np
import Utils as ut
import Corpus as cr
    
if __name__ == "__main__":
    
    fname_samples = "synthetic_samples2"
    fname_classes = "synthetic_classes2"
    fname_train_samples  = "samples2.train"
    fname_train_classes  = "classes2.train"
    fname_test_samples   = "samples2.test"
    fname_test_classes   = "classes2.test"
    
    # Uncomment after samples generation #
    
    synthetic_samples,synthetic_classes = cr.generate_synthetic_hash_samples(1000,16,4)
    
    cr.generate_corpus(synthetic_samples,synthetic_classes,fname_train_samples,
    	fname_train_classes,fname_test_samples,fname_test_classes,0.8)
    print "Corpus generado"
    ######################################
    
    X_train,Y_train,X_test,Y_test = cr.load_corpus(fname_train_samples,fname_train_classes,
						fname_test_samples,fname_test_classes)
    
    pca = PCA(n_components=2)
    pca.fit(X_test)
    Z = pca.transform(X_test)
    X_0,X_1,X_2,X_3 = ut.get_x_separate_class(Z,Y_test)
    X01,X02 = ut.unzip_2d(X_0)
    X11,X12 = ut.unzip_2d(X_1)
    X21,X22 = ut.unzip_2d(X_2)
    X31,X32 = ut.unzip_2d(X_3)
    plt.plot(X01,X02,'ro')
    plt.plot(X11,X12,'bo')
    plt.plot(X21,X22,'go')
    plt.plot(X31,X32,'yo')
    plt.show()
    
    classifier = RandomForestClassifier(n_estimators=100)
    classifier.fit(X_train,Y_train)
    r = classifier.predict(X_test)
    print "% Error: ", float(sum(r!=Y_test))/len(Y_test)
