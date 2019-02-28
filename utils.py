import numpy as np
import random
import copy
import sys


class Board:
    def __init__(self, n = 10, k=15):
        self.n = n
        self.k = k
        self.board = np.array([ [0]*n for i in range(n)])
        self.coords = []
        for j in range(k):
            here = [ np.random.randint(n) for i in range(2) ]
            if here in self.coords:
                while here in self.coords:
                    here = [ np.random.randint(n) for i in range(2) ]
            self.coords.append(here)  
            self.board[here[0], here[1]] = 1
            
    def loc(self, x):
        i,j = x
        if (0 <= i < self.n) and (0 <= j < self.n):
            return self.board[i,j]
        else:
            return -1
    
    def __repr__(self):
        return str(self.board)
    
    
class Bebechy(): 
    def __init__(self):
        self.chromosome = []
        
    def L(self):
        return self.x, self.y-1
    
    def D(self):
        return  self.x+1, self.y
    
    def P(self):
        return self.x, self.y
        
    def U(self):
        return self.x-1, self.y
    
    def R(self):
        return self.x, self.y+1
    
    def screen(self):
        g = {}
        g['L'] = self.board.loc(self.L())
        g['D'] = self.board.loc(self.D())
        g['P'] = self.board.loc(self.P())
        g['U'] = self.board.loc(self.U())
        g['R'] = self.board.loc(self.R())
        return g
    
    def action(self, a='P'):
        if a == 'P':
            val = self.board.loc((self.x, self.y))
            self.bag += max(0, val)
            if val > 0:
                self.board.board[self.x, self.y] = 0
        else:
            self.x, self.y = eval('self.%s()' % a)
    
    def move(self):
        d = self.decision()
        self.memory.append(d)
        self.action(d)
        
   
    def run(self, board, N=50):
        self.n = board.n - 1
        self.x0 = np.random.randint(self.n)
        self.y0 = np.random.randint(self.n)
        self.x, self.y = self.x0, self.y0
        self.board = board
        self.bag = 0
        self.memory = [(self.x0, self.y0)]
        
        for i in range(N):
            self.move()
            
        return self.bag
    

class Robot_v1(Bebechy):

    def decision(self):
        possibilities = self.screen()
        if possibilities['P'] == 1:
            self.action('P')
            possibilities['P'] = -1
        if max(possibilities.values()) == 1:
            good_possibilities = [ k for k, v in possibilities.iteritems() if v == 1]
        else:
            good_possibilities = [ k for k, v in possibilities.iteritems() if v == 0]
        decision = np.random.choice(good_possibilities)
        return decision
        
        
class Robot_v2(Bebechy):
    
    def choose_direction(self, possibilities):
        omit_wall = [ k for k,v in possibilities.iteritems() if not v == -1]
        return np.random.choice(omit_wall)
    
    def decision(self):
        possibilities = self.screen()
        if possibilities.values() not in [ gene for gene,d in self.chromosome ]:
            decision = self.choose_direction(possibilities)
            self.chromosome += zip([possibilities.values()],decision)
        else:
            decision = [ d for gene,d in self.chromosome if gene == possibilities.values() ][0]
        return decision
    