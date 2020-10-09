e = 'r0/gripper > object/handle1 | f'
for i in range(10000):
    qrand = robot.shootRandomConfig()
    res,q,err = cg.generateTargetConfig(e, q0, qrand)
    q[6:12] = q_init[6:12]
    if not res: continue
    res, pid, msg = ps.directPath(q_init, q, False)
    if res: break

e = 'r1/gripper > object/handle2 | 0-0'
for i in range(10000):
    qrand = robot.shootRandomConfig()
    res,q,err = cg.generateTargetConfig(e, q1, qrand)
    if not res: continue
    res, pid, msg = ps.directPath(q1, q, False)
    if res: break
