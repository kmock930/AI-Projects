import vacuumworld
from vacuumworld.vwc import action,direction,orientation,colour,agent

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

        #part 2 attributes
        self.hasMap = False
        self.allMsg = []
        self.counter = 0

        self.should_idle = False

        self.allCords = []
        self.target = None

        self.curCord = ()

        self.hasClean = False
    def decide(self): #action
        if self.observation.center.agent.colour == colour.white:
            if self.should_idle == True:
                if self.needToMove == True:
                    self.needToMove = False
                    return self.move()
            else:
                #mapping
                if self.grid_size == 0 and self.should_idle == False:
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
                    if self.grid_size % 2 == 1: #odd grid size case
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
                            self.hasMap = True
                            print('Grid Size: '+str(self.grid_size)+'x'+str(self.grid_size))
                            print('Visited Cordinates are as follows, in the formate (cordinates:True=Has Dirt): ')
                            print(self.visitedCords)
                            return None
                    else: #even
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
                            self.hasMap = True
                            print('Grid Size: '+str(self.grid_size)+'x'+str(self.grid_size))
                            print('Visited Cordinates are as follows, in the formate (cordinates:True=Has Dirt): ')
                            print(self.visitedCords)
                            return None

                if self.hasMap == True:
                    keylist=list(self.visitedCords.keys())
                    #communicate map to other agents
                    if self.counter < len(keylist):
                        self.counter += 1
                        return action.speak(str(keylist[self.counter-1])+":"+str(self.visitedCords[keylist[self.counter-1]]))
                    self.counter = 0
                    self.should_idle = True
                    return action.speak('Grid size: '+str(self.grid_size))


        else: #other agents
            if self.should_idle == True:
                if self.needToMove == True:
                    self.needToMove = False
                    return self.move()
                else:
                    return None
            else: #move (main task: received map from white then clean map)
                if self.needToMove == True:
                    self.needToMove = False
                    return self.move()
                keylist = list(self.visitedCords.keys())
                print(self.counter,len(keylist))
                if self.counter<len(keylist):
                    if self.hasClean == True:
                        self.hasClean = False
                        self.counter += 1
                        return None
                    target = keylist[self.counter]
                    hasDirt = self.visitedCords[target]
                    if hasDirt == None or str(hasDirt) != str(self.observation.center.agent.colour):
                        self.hasClean = True
                        return None
                    else:
                        #go to target
                        x = target[0]
                        y = target[1]
                        if (self.observation.center.coordinate.x == x and self.observation.center.coordinate.y == y): #found
                            self.hasClean = True
                            return action.clean()
                        else:
                            if self.observation.forward == None:
                                if self.observation.center.coordinate.x == 0:
                                    if self.observation.center.coordinate.x == x:
                                        if self.observation.center.coordinate.y < y:
                                            return self.go_south()
                                        elif self.observation.center.coordinate.y > y:
                                            return self.go_north()
                                    else:
                                        return self.go_east()
                                elif self.observation.center.coordinate.x == self.grid_size:
                                    if self.observation.center.coordinate.x == x:
                                        if self.observation.center.coordinate.y < y:
                                            return self.go_south()
                                        elif self.observation.center.coordinate.y > y:
                                            return self.go_north()
                                    return self.go_west()
                                elif self.observation.center.coordinate.y == 0:
                                    if self.observation.center.coordinate.y == y:
                                        if self.observation.center.coordinate.x < x:
                                            return self.go_east()
                                        elif self.observation.center.coordinate.x > x:
                                            return self.go_west()
                                    return self.go_south()
                                elif self.observation.center.coordinate.y == self.grid_size:
                                    if self.observation.center.coordinate.y == y:
                                        if self.observation.center.coordinate.x < x:
                                            return self.go_east()
                                        elif self.observation.center.coordinate.x > x:
                                            return self.go_west()
                                    return self.go_north()
                            if self.observation.center.coordinate.x != x:
                                if self.observation.center.coordinate.x<x:
                                    return self.go_east()
                                elif self.observation.center.coordinate.x>x:
                                    return self.go_west()
                            else:
                                if self.observation.center.coordinate.y < y:
                                    return self.go_south()
                                elif self.observation.center.coordinate.y > y:
                                    return self.go_north()
                else:
                    self.should_idle = True
                    print('Done')
                    return action.speak('Cleaning Tasks Done!') #tasks done



    def revise(self,observation,messages): #beliefs
        self.observation = observation  # percepts
        self.curCord = (self.observation.center.coordinate.x,self.observation.center.coordinate.y)

        if self.grid_size == 0 and self.observation.center.agent.colour != colour.white:
            self.should_idle = True
        if self.grid_size == 0 and self.observation.center.agent.colour == colour.white:
            self.should_idle == False
        if self.curCord not in self.visitedCords.keys():
            if self.observation.center.dirt != None:
                self.visitedCords.update({self.curCord: self.observation.center.dirt.colour})
            else:
                self.visitedCords.update({self.curCord:None}) #no dirt


        #process messages
        for msg in messages:
            if msg.content == "Please leave":
                self.needToMove = True
            if msg.content == "Arrived "+str(self.observation.center.coordinate):
                self.startExplore = True
            #part 2
            if self.observation.center.agent.colour!=colour.white:
                if msg.content[0]=='(':
                    temp = self.convMsg(msg.content)
                    x = temp[0]
                    y = temp[1]
                    val = temp[2]
                    self.visitedCords.update({(x,y):val})
                if msg.content[0] == 'G':
                    temp=msg.content[len("Grid size: "):]
                    self.grid_size=int(temp)
                    print(self.grid_size) #有reach呢句!
                    self.should_idle=False



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
            return action.move()
        elif self.observation.forward.agent != None: #have another agent in front
            if self.observation.center.agent.colour != colour.white and self.observation.forward.agent.colour == colour.white and self.should_idle==True:
                return action.turn(direction.left)
            elif self.observation.center.agent.colour == colour.white and self.observation.forward.agent.colour != colour.white and self.should_idle == True:
                return action.turn(direction.left)
            elif self.observation.center.agent.colour != colour.white and self.observation.forward.agent.colour != colour.white:
                return action.turn(direction.left)
            else:
                return action.speak("Please leave", self.observation.forward.agent.name)


    def convMsg(self,msg):
        x=0
        y=0
        temp=""
        for cr in msg:
            if cr=='(':
                continue
            elif cr==',':
                x=int(temp)
                temp=""
            elif cr==' ':
                continue
            elif cr==')':
                y=int(temp)
                temp=""
            elif cr==':':
                continue
            else:
                temp+=cr
        if temp=="None":
            temp=None
        return x,y,temp
vacuumworld.run(MyMind())