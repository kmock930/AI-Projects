import vacuumworld
from vacuumworld.vwc import action,direction

class MyMind:
    def __init__(self):
        self.grid_size=0
    def decide(self): #action
        return action.move()
    def revise(self,observation,messages): #beliefs
        self.observation=observation #percepts
vacuumworld.run(MyMind())