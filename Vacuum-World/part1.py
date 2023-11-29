import vacuumworld
from vacuumworld.vwc import action,direction,orientation,colour

import math

class MyMind:
    def __init__(self):
        self.grid_size = 0
        self.visitedCords = {}
        self.needToMove = False
        self.startpoint = ()

        self.startExplore = False
        self.arrivedFurthestCorner = False
        self.toWest = True
    def decide(self): #action
        if self.observation.center.agent.colour == colour.white:
            #mapping
            if self.grid_size == 0:
                if self.observation.center.agent.orientation == orientation.north:
                    return action.turn(direction.left)
                elif self.observation.center.agent.orientation == orientation.east:
                    return self.go_south()
                elif self.observation.center.agent.orientation == orientation.south: #main
                    if self.observation.forward == None:
                        self.grid_size = self.observation.center.coordinate.y + 1
                        return None
                    else:
                        return self.go_south()
                elif self.observation.center.agent.orientation == orientation.west:
                    return self.go_south()

            if self.arrivedFurthestCorner == False:
                if not (self.observation.center.coordinate.x == self.grid_size - 1 and self.observation.center.coordinate.y == self.grid_size - 1):
                    return self.go_east()
                else:
                    self.startExplore = True
                    self.arrivedFurthestCorner = True
                    return action.speak("Arrived "+str(self.observation.center.coordinate),self.observation.center.agent.name)

            if self.startExplore == True:
                #start
                if self.grid_size % 2 == 1: #odd case
                    if not (self.observation.center.coordinate.x == 0 and self.observation.center.coordinate.y == 0):
                        if self.toWest == True:
                            if self.observation.center.coordinate.x == 0:
                                if self.observation.center.agent.orientation != orientation.north:
                                    return action.turn(direction.right)
                                else:
                                    if self.observation.forward.agent != None:
                                        return self.go_north()
                                    else:
                                        self.toWest = False
                                        return self.go_north()
                            else:
                                return self.go_west()
                        else:
                            if self.observation.center.coordinate.x == self.grid_size - 1:
                                if self.observation.center.agent.orientation != orientation.north:
                                    return action.turn(direction.left)
                                else:
                                    if self.observation.forward.agent != None:
                                        return self.go_north()
                                    else:
                                        self.toWest = True
                                        return self.go_north()
                            else:
                                return self.go_east()
                    else:
                        self.startExplore = False #ended
                        print('Grid Size: '+str(self.grid_size)+'x'+str(self.grid_size))
                        print('Visited Cordinates are as follows, in the formate (cordinates:True=Has Dirt): ')
                        print(self.visitedCords)
                        return None
                else: #even case
                    if not (self.observation.center.coordinate.x == self.grid_size-1 and self.observation.center.coordinate.y == 0):
                        if self.toWest == True:
                            if self.observation.center.coordinate.x == 0:
                                if self.observation.center.agent.orientation != orientation.north:
                                    return action.turn(direction.right)
                                else:
                                    if self.observation.forward.agent != None:
                                        return self.go_north()
                                    else:
                                        self.toWest = False
                                        return self.go_north()
                            else:
                                return self.go_west()
                        else:
                            if self.observation.center.coordinate.x == self.grid_size - 1:
                                if self.observation.center.agent.orientation != orientation.north:
                                    return action.turn(direction.left)
                                else:
                                    if self.observation.forward.agent != None:
                                        return self.go_north()
                                    else:
                                        self.toWest = True
                                        return self.go_north()
                            else:
                                return self.go_east()
                    else:
                        self.startExplore = False #ended
                        print('Grid Size: '+str(self.grid_size)+'x'+str(self.grid_size))
                        print('Visited Cordinates are as follows, in the formate (cordinates:True=Has Dirt): ')
                        print(self.visitedCords)
                        return None


        else: #other agents
            if self.needToMove == True:
                self.needToMove = False
                return self.move()
            else:
                return None


    def revise(self,observation,messages): #beliefs
        self.observation = observation  # percepts
        if self.visitedCords == {} and self.startExplore == True:
            self.startpoint = self.observation.center.coordinate
            self.visitedCords.update({self.startpoint:self.observation.center.dirt != None}) #has dirt
        if self.observation.center.coordinate not in self.visitedCords.keys():
            self.visitedCords.update({self.observation.center.coordinate:self.observation.center.dirt!=None})

        #process messages
        for msg in messages:
            if msg.content == "Please leave":
                self.needToMove = True
            if msg.content == "Arrived "+str(self.observation.center.coordinate):
                self.startExplore = True

    #methods
    def metBound(self):
        if self.observation.forward == None:
            return action.turn(direction.left)
        else:
            return None

    def go_east(self):
        if self.observation.center.agent.orientation == orientation.east:
            #Facing east
            return self.move()
        elif self.observation.center.agent.orientation in [orientation.south,orientation.west]:
            #Facing South or West
            return action.turn(direction.left)
        else:
            #Facing North
            return action.turn(direction.right)
    def go_south(self):
        if self.observation.center.agent.orientation == orientation.south:
            return self.move()
        elif self.observation.center.agent.orientation in [orientation.east,orientation.north]:
            return action.turn(direction.right)
        else:
            return action.turn(direction.left)
    def go_west(self):
        if self.observation.center.agent.orientation == orientation.west:
            return self.move()
        elif self.observation.center.agent.orientation in [orientation.east,orientation.north]:
            return action.turn(direction.left)
        else:
            return action.turn(direction.right)
    def go_north(self):
        if self.observation.center.agent.orientation == orientation.north:
            return self.move()
        elif self.observation.center.agent.orientation in [orientation.south,orientation.west]:
            return action.turn(direction.right)
        else:
            return action.turn(direction.left)


    def move(self):
        if self.observation.forward == None:
            return self.metBound()
        if self.observation.forward != None and self.observation.forward.agent == None: #available
            self.visitedCords.update({self.observation.forward.coordinate:self.observation.forward.dirt != None}) #cord : has dirt
            return action.move()
        elif self.observation.forward.agent != None: #have another agent in front
            if self.observation.forward.agent.colour == colour.white:
                return action.turn(direction.left)
            else:
                return action.speak("Please leave", self.observation.forward.agent.name)

vacuumworld.run(MyMind())