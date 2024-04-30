from direct.interval.LerpInterval import LerpFunc
from direct.gui.OnscreenImage import OnscreenImage
from direct.particles.ParticleEffect import ParticleEffect
import re
from collideObjectBase import *
from direct.task import Task
from typing import Callable
from panda3d.core import *



class SpaceShip(SphereCollideObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float, task, render, accept: Callable[[str, Callable], None]):
        super(SpaceShip, self).__init__(loader, modelPath, parentNode, nodeName, 0, 2)
        self.render = render
        self.accept = accept
        self.loader = loader

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.modelNode.setPos(posVec)
        self.taskManager = self.taskMgr()
        self.SetkeyBindings()

        self.reloadTime = .25
        self.missileDistance = 4250
        self.missleBay = 1
        self.ParticleEffectTime = .5
        self.SetParticles()

        self.handler.addInPattern("into")
        self.accept("into", self.HandleInto)

        self.traverser = traverser

        self.traverser = CollisionTraverser()
        self.handler = CollisionTraverserEvent()


        self.taskManager.add(self.CheckIntervals, 'checkMissiles', 40)
        self.cntExplode = 0
        self.explodeIntervals = {} 

        self.enableHUD()


    def CheckIntervals(self, task):
        for i in Missile.Intervals: 
            
            if not Missile.Intervals[i].isPlaying():
                
                Missile.cNodes[i].detachNode()
                Missile.fireModels[i].detachNode()   

                del Missile.Intervals[i]
                del Missile.fireModels[i]
                del Missile.cNodes[i]
                del Missile.collisionSolids[i]
                print(i + ' has reached the end of its fire solution')

                break
        return Task.cont

    def Thrust(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyThrust, 'Forward-thrust')
        else:
            self.taskManager.remove('Forward-thrust')

    def ApplyThrust(self, task):
        rate = 7
        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)
        return Task.cont

    def SetkeyBindings(self):
        self.accept("space", self.Thrust, [1])
        self.accept("space-up", self.Thrust, [0])
        self.accept("a", self.LeftTurn, [1])
        self.accept("a-up", self.LeftTurn, [0])
        self.accept("d", self.RightTurn, [1])
        self.accept("d-up", self.RightTurn, [0])
        self.accept("w", self.LookUp, [1])
        self.accept("w-up", self.LookUp, [0])
        self.accept("s", self.LookDown, [1])
        self.accept("s-up", self.LookDown, [0])
        self.accept("e", self.RollLeft, [1])
        self.accept("e-up", self.RollLeft [0])
        self.accept("q", self.RollRight, [1])
        self.accept("q-up", self.RollRight, [0])
        
    
    def RightTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRightTurn, 'Right-turn')

        else:
            self.taskManager.remove('Right-turn')

    def ApplyLeftTurn(self, task):
        rate = .7
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont        

    def LeftTurn(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyLeftTurn, 'Left-turn')

        else:
            self.taskManager.remove('Left-turn')           

    def ApplyRightTurn(self, task):
        rate = .7
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont        

    def LookUp(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyLookUp, 'Look-Up')

        else:
            self.taskManager.remove('Look-Up')

    def ApplyLookUp(self, task):
        rate = .7
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont        

    def LookDown(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyLookDown, 'Look-Down')

        else:
            self.taskManager.remove('Look-Down')

    def ApplyLookDown(self, task):
        rate = .7
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont 

    def RollLeft(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRollLeft, 'Roll-Left')

        else:
            self.taskManager.remove('Roll-Left')

    def ApplyRollLeft(self, task):
        rate = .7
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont

    def RollRight(self, keyDown):
        if keyDown:
            self.taskManager.add(self.ApplyRollRight, 'Roll-Right')

        else:
            self.taskManager.remove('Roll-Right')

    def ApplyRollRight(self, task):
        rate = .7
        self.modelNode.setH(self.modelNode.getH() + rate)
        return Task.cont                           


#fire Controlles
    def Fire(self):
        if self.missileBay:
            travRate = self.missileDistance
            aim = self.render.getRelativeVector(self.modelNode, Vec3.forward())

            aim.normalize()
            fireSolution = aim * travRate
            InFront = aim * 150 
            travVec = fireSolution + self.modelNode.getPos()
            self.missileBay -= 1
            tag = 'Missile' + str(Missile.missileCount)

            posVec = self.modelNode.getPos() + InFront

            #Creating the Missile
            CurrentMissile = Missile(self.loader, './Assets/phaser/phaser.egg', self.render, tag, posVec, 4.0)

            Missile.Intervals[tag] = CurrentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
            Missile.Intervals[tag].start()
        
        else:
            if not self.taskManager.hasTaskNamed('reload'):
                print('Initializing reload...')
                self.taskManager.doMethodLater(0, self.Reload, 'reload')
                return Task.cont


    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missileBay += 1
            if self.missleBay > 1:
                self.missleBay = 1
            print ("Reload Compete.")
            return Task.done

        elif task.time <= self.reloadTime:
            print("Reload Proceeding...")
            return Task.cont

    def enbleHUD(self):
        self.Hud = OnscreenImage(image = "./Assets/Hud/crossHair.png")

        self.Hud.setTransparency(TransparencyAttrib.MAlpha)   


    def HandleInto(self, entry):
        fromNode = entry.getFromNodePath().getName()
        print("fromNode:" + fromNode)
        intoNode = entry.getIntoNodePath().getName()
        print("intoNode:" + intoNode)

        intoPosition = Vec3(entry.getSurfacePoint(self.render))

        shooter = tempVar [0]
        tempVar = fromNode.split('_')
        tempVar = intoNode.split('_')
        tempVar = intoNode.split('_')
        tempVar = intoNode.split('ship')
        victim = tempVar [0] 

        pattern = r'[0-9]' 
        strippedString = re.sub(pattern, '', victim)

        if (strippedString == "Drone"):
            print(shooter + 'Is Gone') 
            Missile.InterVals[shooter].finish()
            print(victim, 'Hit At', intoPosition)
            self.DroneDestroy(victim, intoPosition)

            self.explode(intoPosition)

        else:
            Missile.InterVals[shooter].finish()


    def Explode(self, impactPoint):
        self.cntExplode += 1 
        tag = "particles" + str(self.cntExplode)

        self.explodeIntervals[tag] = LerpFunc(self.ExplodeLight, fromData = 0, toData = 1, duration = 5.0, extraArgs = [impactPoint])
        self.explodeIntervals[tag].start()

    def ExplodeLight(self, t, explosionPosition):
        self.SetParticles()

        if t == 1.3 and self.explodeEffect:
            self.explodeEffect.disable()

        elif t == 0:
            self.explodeEffect.start(self.explodeNode)

    def DroneDestroy(self, hitID, hitposition):
        nodeID = self.render.find(hitID)
        nodeID.detachNode()

        self.explodeNode += 1
        self.Explode(hitposition)

    def SetParticles(self):
        base.enableParticles()
        self.expldeEffect = ParticleEffect()
        self.explodeEffect.loadConfig("./Assets/particlefx/SP21-explosionIII.ptf")
        self.explodeEffect.setScale(25)
        self.expodeNode = self.render.attachNewNode("ExplosionEffects") 

    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missleBay += 1
            if self.missleBay > 1:
                self.missleBay = 1
            print("Reloading Complete.")
            return Task.done

        elif task.time <= self.reloadTime:
            print("Reload Proceeding..")

            return Task.cont                                  



class Missile(SphereCollideObject):
    fireModels = {}
    cNodes = {}
    InterVals = {}
    CollisionSolid = {}
    MissileCount = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, PosVec: Vec3, scaleVec: float = 1.0):
        super(Missile).__init__(loader, modelPath, parentNode, nodeName, Vec3(0,0,0), 3.0)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setPos(PosVec)

        Missile.MissileCount += 1

        Missile.fireModels[nodeName] = self.modelNode
        Missile.cNodes[nodeName] = self.collisionNode

        Missile.CollisionSolid[nodeName] = self.collisionNode.node().getSolid(0)
        Missile.cNodes[nodeName].show()

        print("Fire Torpedo # " + str(Missile.MissileCount))