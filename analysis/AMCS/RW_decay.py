import pandas as pd
import numpy as np
from scipy.stats import binom
import math

# rascular wagner model with decaying
# This is the model used in paper stable representation of decision variable
class RW_dacay:
    def _init_(self):
        self.alpha = 0
        self.beta = 0
        self.V = [0, 0]
        self.choices = []
        self.diff = [] # array of V_a - V_b
        self.averse = 0 # number of aversive signals received in a trial
        self.nnl = 0
    
    def make_choice(self):
        if (np.exp(-self.beta*self.V[0]) + np.exp(-self.beta*self.V[1])) == 0:
            prob = 0
        else:
            prob = np.exp(-self.beta * self.V[0]) / (np.exp(-self.beta*self.V[0]) + np.exp(-self.beta*self.V[1]))
        # binom(1, 1-prob).rvs() returns 0 if A is chosen, and 1 if B is chosen
        choice = binom(1, 1-prob).rvs() + 1
        return choice
    
    # used for simulation
    def outcome(self, trial_ind, choice):
        noise_prob = [0.6, 0.8, 0.6, 0.65] # posibility of choosing A resulting in reward
        if choice == 1:
            chance = noise_prob[math.floor((trial_ind / 40) % 4)]
        else:
            chance = 1 - noise_prob[math.floor((trial_ind / 40) % 4)]
        if binom(1, chance).rvs():
            self.averse += 1
            return 1
        else:
            return 0

    def update(self, choice, trial_ind):
        outcome = self.outcome(trial_ind, choice)
        self.V[choice - 1] = self.V[choice - 1]  + self.alpha * (outcome - self.V[choice - 1])
        return outcome

    def simulate(self, trial_num, alpha, beta, va, vb):
        self.averse = 0
        self.choices = []
        self.outcomes = []
        self.diff = [] # Va - Vb
        self.alpha = alpha
        self.beta = beta
        self.V = [va, vb]

        for i in range(trial_num):
            choice = self.make_choice()
            outcome = self.update(choice, i)
            self.choices.append(choice)
            self.outcomes.append(outcome)
            self.diff.append(self.V[0] - self.V[1])
        
        self.choices = np.array(self.choices)
        self.outcomes = np.array(self.outcomes)


    # calculate the negative log likelihood given the real data and some initial values
    def nll(self, parameters, choices, outcomes):
        choice_prob = []
        self.alpha = parameters[0]
        self.beta = parameters[1]
        self.V = [0.5, 0.5]

        for i in range(choices.size):
            real_choice = choices[i] # 0 for A and 1 for B
            # avoid division by 0
            if (np.exp(-self.beta*self.V[0]) + np.exp(-self.beta*self.V[1])) == 0:
                prob = 0
            else:
                prob = abs(real_choice - np.exp(-self.beta * self.V[0]) / (np.exp(-self.beta*self.V[0]) + np.exp(-self.beta*self.V[1])))
            choice_prob.append(prob)
            self.V[real_choice] = self.V[real_choice] + self.alpha * (outcomes[i] - self.V[real_choice])
        
        choice_prob = np.array(choice_prob)
        choice_prob[choice_prob == 0] = np.finfo(float).eps
        nll = - np.sum(np.log(choice_prob))

        return nll
        