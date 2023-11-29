import numpy as np
from numpy import genfromtxt
import csv
import math

def findCoefficients(data):
    x = data[:,0] # first column: vector x
    y = data[:,1] # second column: vector y
    z = data[:,2] # third column: vector z
    A = np.vstack([x,y,np.ones(len(x))]).T
    Ap = np.linalg.pinv(A)
    a,b,c = Ap.dot(z)
    return a,b,c

def main():
    coeffData=genfromtxt('ass3Data.csv',delimiter=',')
    a,b,c = findCoefficients(coeffData)
    a_str=str(a)
    b_str=str(b)
    c_str=str(c)
    file=open("leastSquares.txt","w+")
    file.write("a="+a_str+"\n")
    print("a=",a)
    file.write("b="+b_str+"\n")
    print("b=",b)
    file.write("c="+c_str+"\n")
    print("c=",c)
    file.close()

if __name__ == "__main__":
    main()
