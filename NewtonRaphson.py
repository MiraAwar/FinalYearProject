import math
from random import randint as rand
from numpy import polyfit as fit
import matplotlib.pyplot as plt

#number of iterations in Newton-Raphson
iterations = 100
#error tolerance for Newton-Raphson
error_tolerance = 1

#our goal is to make the sparse graph we have more dense
#specify degree of polynomial you are trying to fit
#later, one can use certain methods/heuristic to get closer to the optimal degree
degree = 5
C = [degree]

#x and y coordinates of our data points
months = 10
X=[float(i) for i in range(months*4)]
#bond yield between 1% and 9.99%
Y=[rand(400.0, 500.0)/100.0 for i in range(months*4)]

#function to calculate f(x) for a given x 
def f(x, C): 
  res = 0.0
  for i in range(len(C)):
    res += C[i] * (x**i)
  return res

#function to calculate derivative of f(x)
def f_prime(x, C): 
  res = 0.0
  for i in range(1, len(C)):
    res += i * C[i] * (x**(i-1))
  return res

def NewtonRaphson(x, C):
  #formula, but calling the two functions, since
  #x is being updated every iteration.
  for it in range(iterations): 
    if(f_prime(x, C) == 0):
      continue
    x -= f(x, C)/f_prime(x, C)
  #get f close enough to 0
  counter = 100
  while (counter and abs(f(x, C)) >= error_tolerance): 
    if(f_prime(x, C) == 0):
      break
    x -= f(x, C)/f_prime(x, C)
    counter -= 1
  if(not counter or x<0 or x>months*4):
     return -1
  return x

plt.subplots(6,1,figsize=(20, 15))

def predict(X, Y):
  #number of "graph-densifying" iterations
  repeat = 25
  
  while(repeat):
    #our final refined predicted value of yield at x
    repeat -= 1 
    
    #get range of our data points
    minY = min(Y)
    maxY = max(Y)
    #get range of our roots
    minX = min(X)
    maxX = max(X)

    #coefficients of our function f based on data points
    C = fit(X, Y, degree).tolist()
    #for easier manipulation, have C[i] represent degree i 
    #i.e. f(x) = C[0] + C[1]*x + C[2]*(x**2) + ... + C[i]*(x**i) + ... + C[degree]*(n**degree)
    C.reverse()
    
    if(repeat%5 == 0):
        plt.subplot(6, 1, 6 - repeat//5)
        plt.plot(X,Y,'k')
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.title("GBP in USD")
        print(f(inpt, C))
    
    #for each possible value that the graph can take, find a root using Newton-Raphson
    #these will be our new data points
    for i in range (int(minY*100), int(maxY*100), 1):
      C[0] -= i/100.0
      #start with a random estimate
      value = rand(0.0, float(months*4)) 
      root = NewtonRaphson(value, C)
      C[0] += i/100.0
      if(root!= -1 and not root in X):
          X.append(root)
          Y.append(i/100.0)
          
    Y = [y for _, y in sorted(zip(X, Y))]
    X.sort()

inpt = float(input("To predict yield at x, enter x: "))

plt.subplot(6, 1, 1)
plt.plot(X,Y,'k')
plt.xlabel("Weeks")
plt.ylabel("Value in %")
plt.title("Single Bond Yield")

#calculations are made to refine the function f
predict(X, Y)