import numpy as np
import math
import time
from funVel import *

def DistBetweenAgents(X,NStart,N):
    n = N-NStart		# Agent quantity
    mDist = np.zeros([N,N])	# Matrix initialization

    for i in range(NStart,N):
        for j in range(NStart,N):
            dij1 = X[0,i] - X[0,j]
            dij2 = X[1,i] - X[1,j]
            normdij = math.sqrt(dij1**2 + dij2**2)    # distance between i & j agents
            mDist[i,j] = normdij		         # distance added to the matrix
    return mDist

def DistBetweenAgentsV2(X,NStart,N):
    mDist = np.zeros([N,N])	# Matrix initialization
    
    diff = X[:, :, np.newaxis] - X[:, np.newaxis, :]
    dist_matrix = np.linalg.norm(diff, axis = 0)
    mDist = dist_matrix

    return mDist

def FormationError(FAct, FDes, NStart, N):
    s1 = len(FAct[0])
    suma = 0
    for i in range(NStart,N):
        for j in range(NStart,N):
            mDif = (FAct[i][j] - FDes[i][j])**2 # Squared difference
            suma = suma + mDif		   # columns and rows sum
    tot = (NStart-N)**2		   # Agent quantity
    error = suma/tot			   # mean error
    return error

def FormationErrorV2(FAct, FDes, NStart, N):
    FDes_resized = FDes[:N, :N]  # Solo la submatriz necesaria de FDes
    diff_squared = np.square(FAct - FDes_resized)
    mse = np.mean(diff_squared)
    return mse


form_shape = 1
rigidity_level = 8
formation_edge = 0.3
formation_matrix = Fmatrix(form_shape,rigidity_level)

#agents = [1,2,3,4,5,6,7,8,9,10]
agents = [1,2,3,4,5,6]
obs = [18,19,20]
obj = [11]
markers = agents + obj + obs

NMax = 10
NStart = 0
N = len(agents)

posActuales = np.ones([2,N])
for i in range(0,N):
    posActuales[0][i] = posActuales[0][i] + i*7
    posActuales[1][i] = posActuales[1][i] + i*3
print(f"pos actuales\n {posActuales} \n")

tic = time.perf_counter_ns()
actual_adjacency = (1/formation_edge)*DistBetweenAgents(posActuales,NStart,N) 
formation_mse = FormationError(actual_adjacency,formation_matrix,NStart,N)
toc = time.perf_counter_ns()
t1 = (toc - tic)*(10**-6)
print(f"actual adjacency: \n{actual_adjacency}\n")
print(f"error: {formation_mse}")
print(f"tiempo (ms): {t1: .4f}\n")

tic = time.perf_counter_ns()
actual_adjacency = (1/formation_edge)*DistBetweenAgentsV2(posActuales,NStart,N) 
formation_mse = FormationErrorV2(actual_adjacency,formation_matrix,NStart,N)
toc = time.perf_counter_ns()
t2 = (toc - tic)*(10**-6)
print(f"actual adjacency: \n{actual_adjacency}\n")
print(f"error optimizado: {formation_mse}")
print(f"tiempo (ms): {t2: .4f}\n")

