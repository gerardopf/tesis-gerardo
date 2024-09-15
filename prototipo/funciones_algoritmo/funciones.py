""" =========================================================================
# FUNCTIONS TO MEASURE METRICS
# =========================================================================
# Autor: José Alejandro Rodríguez Porras
# ========================================================================= """

import numpy as np
import math

def FormationError(FAct, FDes, NStart, N):
# Calculates the mse error between the current formation and the desired one
# Parameters:
#   FAct = Adjacency matrix of the current formation
#   FDes = Adjacency matrix of the target (desired) formation
# Output:
#   error = Mean squared error of the current formation compared to the desired
# one
    suma = 0
    for i in range(NStart,N):
        for j in range(NStart,N):
            mDif = (FAct[i][j] - FDes[i][j])**2 # Squared difference
            suma = suma + mDif		   # columns and rows sum
    tot = (NStart-N)**2		   # Agent quantity
    error = suma/tot			   # mean error
    return error

def FormationErrorOptimized(FAct, FDes, NStart, N):
# Calculates the mse error between the current formation and the desired one
# Parameters:
#   FAct = Adjacency matrix of the current formation
#   FDes = Adjacency matrix of the target (desired) formation
# Output:
#   mse = Mean squared error of the current formation compared to the desired
# one
    FDes_resized = FDes[:N, :N]  # Solo la submatriz necesaria para que sea del tamaño de FAct
    diff_squared = np.square(FAct - FDes_resized)
    mse = np.mean(diff_squared)
    return mse

def DistBetweenAgents(X,NStart,N):
# Generates the matrix with the distance between the agents.
# Parameters:
#   X = Matrix with the current position of the agents vectors (x,y)
# Output:
#   mDist = Adjacency matrix of the graph produced by the current position
# of the agents
    mDist = np.zeros([N,N])	# Matrix initialization

    for i in range(NStart,N):
        for j in range(NStart,N):
            dij1 = X[0,i] - X[0,j]
            dij2 = X[1,i] - X[1,j]
            normdij = math.sqrt(dij1**2 + dij2**2)    # distance between i & j agents
            mDist[i,j] = normdij		         # distance added to the matrix
    return mDist

def DistBetweenAgentsOptimized(X,NStart,N):
# Generates the matrix with the distance between the agents.
# Parameters:
#   X = Matrix with the current position of the agents vectors (x,y)
# Output:
#   dist_matrix = Adjacency matrix of the graph produced by the current position
# of the agents
    diff = X[:, :, np.newaxis] - X[:, np.newaxis, :]
    dist_matrix = np.linalg.norm(diff, axis = 0)

    return dist_matrix