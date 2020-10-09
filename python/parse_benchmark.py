import numpy as np
import datetime as dt
def parse(filename):
    times = list()
    nnodes = list()
    with open(filename, 'r') as f:
        state = "time"
        while state != "finished":
            line = f.readline()
            if line[:7] == "Average":
                break
            if state == "time":
                time = line.split(":")
                assert (len(time) == 3)
                times.append(dt.timedelta(hours=int(time[0]),
                                          minutes=int(time[1]),
                                          seconds=float(time[2])).total_seconds())
                state="number nodes"
            elif state == "number nodes":
                nnodes.append(int(line[14:].rstrip('\n')))
                state = "time"
    return np.array(times), np.array(nnodes)

def print_stat(times, nnodes):
    print("time (s) & {:.2f} & {:.2f} & {:.2f} & {:.2f} \\\\".format(min(times), max(times),
                                                     np.mean(times),
                                                     np.std(times)))
    print("nodes & {} &  {} & {:.2f} & {:.2f}".format(min(nnodes), max(nnodes),
                                                np.mean(nnodes),
                                                np.std(nnodes)))
