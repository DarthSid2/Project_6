from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
import DroneDefencePath as DroneDefencePath
import SpaceJamClass as spaceJamClass
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from collideObjectBase import PlacedObject  






class SpaceJam(ShowBase):
    
    
    
    
    def __init__(self):
        ShowBase.__init__(self)
        self.sceneSetup()
        self.cTrav = CollisionTraverser()
        self.cTrav.traverse(self.render)
        self.pusher = CollisionHandlerPusher()
        self.cTrav.showCollisions(self.render)
        self.pusher.addCollider(self.ship1.collisionNode, self.ship1.modelNode)
        self.cTrav.addCollider(self.ship1.collisionNode, self.pusher)
       
    def DrawCloudDefense(self, centralObject, droneName): 
        unitVec = DroneDefencePath.Cloud()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()  
        spaceJamClass.Drone(self.loader, "./Assets/Drones/DroneDefender.obj", self.render, droneName, "./Assets/Drones/DroneDefender/octotoad1_auv.png", position, 10)
    
    
    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1): 
        unitVec = DroneDefencePath.BaseballSeams(step, numSeams, B = 0.4)
        unitVec.normalize()
        position = unitVec * radius * 500 + centralObject.modelNode.getPos()  
        spaceJamClass.Drone(self.loader, "./Assets/Drones/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/Drones/DroneDefender/octotoad1_auv.png", position, 5)
    
    
    def DrawAxisDronesXY (self, centralObject, droneName):
        unitVec = DroneDefencePath.axisDronesXY ()
        unitVec.normalize()
        position = unitVec * 550 + centralObject.modelNode.getPos()  
        spaceJamClass.Drone(self.loader, "./Assets/Drones/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/Drones/DroneDefender/octotoad1_auv.png", position, 5)
    
    
    def DrawAxisDronesXZ (self, centralObject, droneName):
        unitVec = DroneDefencePath.axisDronesXZ ()
        unitVec.normalize()
        position = unitVec * 600 + centralObject.modelNode.getPos()  
        spaceJamClass.Drone(self.loader, "./Assets/Drones/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/Drones/DroneDefender/octotoad1_auv.png", position, 5)
    
    
    def DrawAxisDronesYZ (self, centralObject, droneName):
        unitVec = DroneDefencePath.axisDronesYZ ()
        unitVec.normalize()
        position = unitVec * 650 + centralObject.modelNode.getPos()  
        spaceJamClass.Drone(self.loader, "./Assets/Drones/DroneDefender/DroneDefender.obj", self.render, droneName, "./Assets/Drones/DroneDefender/octotoad1_auv.png", position, 5)
    
     
    def setCamera(self):
        self.disableMouse()
        self.camera.reparentTo(self.Ship1.modelNode)
        self.camera.setFluidPos(0, 1, 0)

        

    def SetupScene(self):
        self.Universe = self.loader.loadModel("./Assets/Universe/Universe.obj")
        self.Universe.reparentTo(self.render)
        self.Universe.setScale(15000)

        self.Planet1 = self.loader.loadModel("./Assets/Planets/protoPlanet.x.obj")
        self.Planet1.reparentTo(self.render)
        self.Planet1.setPos(1100, 5000, 2500)
        self.Planet1.setScale(350)
        tex = self.loader.loadTexture("./Assets/Planets/Blue-Ice.jpg")
        self.Planet1.setTexture(tex, 1)

        self.Planet2 = self.loader.loadModel("./Assets/Planets/protoPlanet.x.obj")
        self.Planet2.reparentTo(self.render)
        self.Planet2.setPos(750, 10000, 2200)
        self.Planet2.setScale(450)
        tex = self.loader.loadTexture("./Assets/Planets/Color-Shift.jpg")
        self.Planet2.setTexture(tex, 1)

        self.Planet3 = self.loader.loadModel("./Assets/Planets/protoPlanet.x.obj")
        self.Planet3.reparentTo(self.render)
        self.Planet3.setPos(400, 3000, 4500)
        self.Planet3.setScale(400)
        tex = self.loader.loadTexture("./Assets/Planets/Concrete.png")
        self.Planet3.setTexture(tex, 1)

        self.Planet4 = self.loader.loadModel("./Assets/Planets/protoPlanet.x.obj")
        self.Planet4.reparentTo(self.render)
        self.Planet4.setPos(1200, 4550, 4000)
        self.Planet4.setScale(350)
        tex = self.loader.loadTexture("./Assets/Planets/Exo-Planet tex.jpg")
        self.Planet4.setTexture(tex, 1)

        self.Planet5 = self.loader.loadModel("./Assets/Planets/protoPlanet.x.obj")
        self.Planet5.reparentTo(self.render)
        self.Planet5.setPos(1500, 4000, 1500)
        self.Planet5.setScale(350) 
        tex = self.loader.loadTexture("./Assets/Planets/Hardening_Lava.png")
        self.Planet5.setTexture(tex, 1)


        self.Planet6 = self.loader.loadModel("./Assets/Planets/protoPlanet.x.obj")
        self.Planet6.reparentTo(self.render)
        self.Planet6.setPos(500, 5200, 1800)
        self.Planet6.setScale(350)
        tex = self.loader.loadTexture("./Assets/Planets/iceWorld.jpg")
        self.Planet6.setTexture(tex, 1)

        self.Ship1 = self.loader.loadModel("./Assets/Spaceships/spaceship.obj")
        self.Ship1.reparentTo(self.render)
        self.Ship1.setPos(100, 3280, 100)
        self.Ship1.setScale(15)
        self.Ship1.setTexture(tex, 1)
        (self.task_mgr, self.render, self.accept)

        self.Station1 = self.loader.loadModel("./Assets/SpaceStation1B/spaceStation.x")
        self.Station1.reparentTo(self.render)
        self.Station1.setPos(110, 3300, 120)
        self.Station1.setScale(25)
        self.Station1.setTexture(tex, 1)

        self.tex = self.loader.loadTexture("./Assets/Universe/starfield-in-blue.jpg")
        self.Universe.setTexture(self.tex, 1)
        
        fullCycle = 60
        self.setCamera()

        for j in range(fullCycle):
            spaceJamClass.Drone.droneCount += 1
            nickName = "Drone" + str(spaceJamClass.Drone.droneCount)
            self.DrawCloudDefense(self.Planet1, nickName)
            self.DrawBaseBallSeams(self.Planet2, nickName, j , fullCycle)
            self.DrawCircleXZ(self.Planet3, nickName)
            self.DrawCircleXY(self.Planet4, nickName)
            self.DrawCircleYZ(self.Planet5, nickName)
            

 







app = SpaceJam()
app.SetupScene()
app.run()