import sys
import numpy as np
import pseudoinverse
import math


def main():
    dataFn = sys.argv[1]
    data = np.genfromtxt(dataFn, delimiter=',')
    A1 = np.linalg.pinv(data,rcond=1e-6)
    A2 = pseudoinverse.compute(data,1e-6)
    D = A1-A2
    x = 0.0
    for i in range(0,D.shape[0]):
        for j in range(0,D.shape[1]):
            x += D[i,j]*D[i,j]
    print(math.sqrt(x))

if __name__ == "__main__":
    main()
    
    


