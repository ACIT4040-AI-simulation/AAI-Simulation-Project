import numpy as np

class ODESolver:
    """ODESolver superclass

    Any classes inheriting from this superclass must implement advance() method.
    """

    def __init__(self, k):
        self.k = k 
        # The problem will define it the SIR.py file.

    def advance(self): 
        # The main method which advances our problem on one step. 
        # Advance solution one time step.
        raise NotImplementedError

    def set_initial_conditions(self, U0): # U0 is the initial conditions.
        if isinstance(U0, (int, float)):
            # Scaler ODE
            self.number_of_equations = 1 
            U0 = float(U0)
        else:
            # System of equitions  
            U0 = np.asarray(U0)
            self.number_of_equations = U0.size
        self.U0 = U0 # Stroe it in the class.

    def solve(self, time_points):

        self.t = np.asarray(time_points)
        n = self.t.size

        self.uu = np.zeros((n, self.number_of_equations))

        self.uu[0, :] = self.U0

        # Integrate 

        for i in range (n - 1):
            self.i = i
            self.uu[i + 1] = self.advance()

        return self.uu[:i + 2], self.t[:i + 2]

class ForwardEuler(ODESolver):

    def advance(self):
        u, f, i, t = self.uu, self.k, self.i, self.t
        dt = t[i + 1] - t[i]
        return u[i, :] + dt * f(u[i, :], t[i])






    

