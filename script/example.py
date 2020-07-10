from math import pi, sqrt
from hpp.corbaserver.manipulation.ur5 import Robot
from hpp.corbaserver.manipulation import Client, ConstraintGraph,\
    ConstraintGraphFactory, ProblemSolver
from hpp.gepetto.manipulation import ViewerFactory
from hpp_idl.hpp import Equality, EqualToZero

class Ground (object):
  rootJointType = 'anchor'
  urdfFilename = "package://example/urdf/ground.urdf"
  srdfFilename = "package://example/srdf/ground.srdf"

class Box (object):
  rootJointType = 'freeflyer'
  urdfFilename = "package://example/urdf/box.urdf"
  srdfFilename = "package://example/srdf/box.srdf"

class Cylinder (object):
  rootJointType = 'freeflyer'
  urdfFilename = "package://example/urdf/cylinder.urdf"
  srdfFilename = "package://example/srdf/cylinder.srdf"

Robot.urdfFilename = "package://example-robot-data/robots/ur_description/urdf/ur3_gripper.urdf"
Robot.srdfFilename = "package://example-robot-data/robots/ur_description/srdf/ur3_gripper.srdf"

from hpp.corbaserver import loadServerPlugin
loadServerPlugin ("corbaserver", "manipulation-corba.so")
Client ().problem.resetProblem ()

robot = Robot('2ur3-box', 'r0')
robot.setJointPosition ('r0/root_joint', [-.25, 0, 0, 0, 0, 0, 1])
ps = ProblemSolver (robot)
vf = ViewerFactory (ps)

vf.loadRobotModel (Robot, "r1")
robot.setJointPosition ('r1/root_joint', [.25, 0, 0, 0, 0, 1, 0])

# Change bounds of robots to increase workspace and avoid some collisions
robot.setJointBounds ('r0/shoulder_pan_joint', [-pi, 4])
robot.setJointBounds ('r1/shoulder_pan_joint', [-pi, 4])
robot.setJointBounds ('r0/shoulder_lift_joint', [-pi, 0])
robot.setJointBounds ('r1/shoulder_lift_joint', [-pi, 0])
robot.setJointBounds ('r0/elbow_joint', [-2.6, 2.6])
robot.setJointBounds ('r1/elbow_joint', [-2.6, 2.6])

vf.loadObjectModel (Cylinder, 'object')
vf.loadEnvironmentModel (Ground, "ground")
robot.setJointBounds ('object/root_joint',
                      [-1.,1.,-1.,1.,-.1,1.,-1.0001, 1.0001,-1.0001, 1.0001,
                       -1.0001, 1.0001,-1.0001, 1.0001,])

## Initial configuration of manipulator arms
q0_r0 = [pi/6, -pi/2, pi/2, 0, 0, 0,]
q0_r1 = q0_r0 [::]
q0_object = [0, 0, 0.041, 0, 0, 0, 1]

q0 = q0_r0 + q0_r1 + q0_object

## Gripper
#
grippers = ["r0/gripper", "r1/gripper"]

## Handles
#
objects = ["object"]
handlesPerObject  = [['object/handle1', 'object/handle2']]
## Contact surfaces
contactsPerObject = [['object/surface1', 'object/surface2']]
envContactSurface = ['ground/ground']

cg = ConstraintGraph(robot,"manipulation")
factory = ConstraintGraphFactory(cg)
factory.setGrippers(grippers)
factory.setObjects(objects, handlesPerObject, contactsPerObject)
factory.environmentContacts(envContactSurface)
factory.generate()
for e in cg.edges.keys():
    try:
        cg.setWeight(e, 1)
    except Exception as exc:
        pass
cg.initialize()

e = 'ur3/gripper > object/handle1 | f'
for i in range(00):
    q = robot.shootRandomConfig()
    res, q1, err = cg.generateTargetConfig(e,q0,q)
    if res: break

q_init = q0[::]
q_goal = q0[::]

q_goal[-4:] = [1, 0, 0, 0]

ps.setInitialConfig(q_init)
ps.addGoalConfig(q_goal)
ps.solve()
