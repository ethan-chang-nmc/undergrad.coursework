"""
CTRNN class

Implementation of the neuronal network following the CTRNN structure outlined in Gong et al. 2024

Author: Ethan Chang
April 2025
"""
import numpy as np

class CTRNN:

    def __init__(self, size, dt = 0.01):
        """
        Model Parameters for the CTRNN

        W (weights) initialized using uniform distribution

        """
        self.size = size
        self.dt = dt

        W = np.random.uniform(-1 / np.sqrt(self.size), 1 / np.sqrt(self.size), (self.size, self.size))
        