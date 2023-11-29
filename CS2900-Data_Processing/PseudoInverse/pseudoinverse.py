import numpy as np
import math

def compute(A,cutoff):
    U,D,V = np.linalg.svd(A)

    Dinv = np.zeros((A.shape[0],A.shape[1])).T
    Dinv[:D.shape[0],:D.shape[0]] = np.linalg.inv(np.diag(D))

    Ainv = V.T.dot(Dinv).dot(U.T)
    
    return Ainv

def main():
    A=np.array([[1.0,2.0],
                [-1.0,3.0],
                [3.0,1.0],
                [4.0,2.0]])
    Ainv = compute(A,1e-6)
    np.savetxt("pseudoinverse.txt",Ainv,fmt='%.8f')
    print(Ainv)


if __name__ == "__main__":
    main()
