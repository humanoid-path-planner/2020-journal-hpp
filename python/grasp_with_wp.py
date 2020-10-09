from math import sqrt
from hpp import Transform
from hpp.corbaserver.manipulation import ConstraintGraph, \
    ConstraintGraphFactory, Constraints
from hpp.corbaserver import Client
Client ().problem.resetProblem ()
from manipulation import robot, vf, ps, Ground, Box, Pokeball, PathPlayer, gripperName, ballName

vf.loadEnvironmentModel (Ground, 'ground')
vf.loadObjectModel (Pokeball, 'pokeball')
robot.setJointBounds ('pokeball/root_joint', [-.4,.4,-.4,.4,-.1,2.,
                                              -1.0001, 1.0001,-1.0001, 1.0001,
                                              -1.0001, 1.0001,-1.0001, 1.0001,])


q1 = [0, -1.57, 1.57, 0, 0, 0, .3, 0, 0.025, 0, 0, 0, 1]

## Create constraint graph
graph = ConstraintGraph (robot, 'graph')

# Required calls
factory = ConstraintGraphFactory (graph)
factory.setGrippers (['ur5/gripper'])
factory.setObjects (["pokeball", ], [['pokeball/handle'],], [['pokeball/bottom'],])
# Optionally
factory.environmentContacts (['ground/surface'])
factory.generate ()
# graph is initialized

ps.selectPathValidation ("Dichotomy", 0)
ps.selectPathProjector ("Progressive", 0.1)
graph.initialize ()

## Project initial configuration on state 'placement'
res, q_init, error = graph.applyNodeConstraints ('free', q1)
q2 = q1 [::]
q2 [7] = .2

## Project goal configuration on state 'free'
res, q_goal, error = graph.applyNodeConstraints ('free', q2)

## Define manipulation planning problem
ps.setInitialConfig (q_init)
ps.addGoalConfig (q_goal)

# v = vf.createViewer ()
# pp = PathPlayer (v)
# v (q1)

## Build relative position of the ball with respect to the gripper
# for i in range (100):
#   q = robot.shootRandomConfig ()
#   res,q3,err = graph.generateTargetConfig ('grasp-ball', q_init, q)
#   if res and robot.isConfigValid (q3): break;

# if res:
#   robot.setCurrentConfig (q3)
#   gripperPose = Transform (robot.getJointPosition (gripperName))
#   ballPose = Transform (robot.getJointPosition (ballName))
#   gripperGraspsBall = gripperPose.inverse () * ballPose
#   gripperAboveBall = Transform (gripperGraspsBall)
#   gripperAboveBall.translation [2] += .1

robot.isConfigValid(q_init)
ps.client.basic.problem.clearConfigValidations()
ps.addConfigValidation('CollisionValidation')
robot.isConfigValid(q_init)

# Run benchmark
#
import datetime as dt
totalTime = dt.timedelta (0)
totalNumberNodes = 0
for i in range (20):
    ps.clearRoadmap ()
    ps.resetGoalConfigs ()
    ps.setInitialConfig (q_init)
    ps.addGoalConfig (q_goal)
    t1 = dt.datetime.now ()
    ps.solve ()
    t2 = dt.datetime.now ()
    totalTime += t2 - t1
    print (t2-t1)
    n = ps.numberNodes ()
    totalNumberNodes += n
    print ("Number nodes: " + str(n))

print ("Average time: " +
       str ((totalTime.seconds+1e-6*totalTime.microseconds)/float (20)))
print ("Average number nodes: " + str (totalNumberNodes/float (20)))

