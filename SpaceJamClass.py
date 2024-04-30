from panda3d.core import * 
from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
from direct.task import Task
from collideObjectBase import * 
from typing import Callable
from direct.gui.OnscreenImage import OnscreenImage
from direct.task.Task import TaskManager
import DroneDefencePath as DroneDefencePath


class Universe(InverseSphereCollideObject):
    def __init__ (self, loader: Loader, modelPath: str, parentNode: NodePath, NodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Universe, self).__init__(loader, modelPath, parentNode, NodeName, 0, 1)
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
    
        self.modelNode.setName(modelPath)
        tex = loader. loadTexture(texPath)
        self.modelNode.setTexture(tex, 1 )


class Planets(SphereCollideObject):
    
    def __init__ (self, loader: Loader, modelPath: str, parentNode: NodePath, NodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Planets, self).__init__(loader, modelPath, parentNode, NodeName, 0, 1)
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
    
        self.modelNode.setName(modelPath)
        tex = loader. loadTexture(texPath)
        self.modelNode.setTexture(tex, 1 )    

class Drone(SphereCollideObject):
    droneCount = 0 
   
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Drone, self).__init__(loader, modelPath, parentNode, nodeName, 0, 2)
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1) 

class increment():
    Increment = 0            

class SpaceStation(CapsuleCollidableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
    

class yz():
    circleIncrement = 0

class xy():
     circleIncrement = 0

class xz():
    circleIncrement = 0

class Orbiter(SphereCollideObject):
    numOrbits = 0
    velocity = 0.005
    cloudTimer = 250

    def __init__(self, loader: Loader, taskMgr: TaskManager, modelPath: str, parentNode: NodePath, nodeName: str, scaleVec: Vec3, texPath: str,
                  centralObject: PlacedObject, orbitRadius: float, orbitType: str, staringAt: Vec3):
        
        super(Orbiter, self,).__init__(loader, modelPath, parentNode, nodeName, Vec3(0,0,0), 3.2)
        self.taskMgr = taskMgr
        self.orbitType = orbitType
        self.modelNode.setScale(scaleVec)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.staringAt = staringAt
        self.orbitObject = centralObject
        self.orbitRadius = orbitRadius
        Orbiter.numOrbits += 1

        self.cloudClock = 0
        self.taskFlag = "Traveler-" + str(Orbiter.numOrbits)
        taskMgr.add(self.Orbit, self.taskFlag)

    def Orbit(self, task):
        if self.orbitType == "MLB":
            positionVec = DroneDefencePath.BaseBallSeams(task.time * Orbiter.vecocity, self.numOrbits, 2.3)
            self.modelNode.setPos(positionVec * self.orbitRadius + self.orbitObject.modelNode.getPos())


        elif self.orbitType == "Cloud":
            if self.cloudClock < Orbiter.cloudTimer:
                self.cloudClock += 1 

            else:
                self.cloudClock = 0
                positionVec = DroneDefencePath.Cloud()
                self.modelNode.setPos(positionVec * self.orbitRadius + self.orbitObject.modelNode.getPos())

        self.modelNode.lookAt(self.staringAt.modelNode)
        return task.cont
    