import tkinter as tk
import copy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

root = tk.Tk()


class Process:
    def __init__(self, ta, tb, name, *priority):
        self.ta = ta    #arrival time
        self.tb = tb    #burst time
        self.priority = priority
        self.name = name
        self.tr = 1

def get_runtime(ready):
    return sum([x.tb for x in ready])

#done and working
def FCFS(ready):
    running = []
    ready = sorted(ready, key=lambda x: x.ta)
    tmp = ready.copy()
    runtime = get_runtime(ready)
    for i in range(runtime):
        tmp[0].tb = tmp[0].tb - 1
        running.append(copy.copy(tmp[0]))
        if tmp[0].tb == 0: del tmp[0]
    return running

#done and working
def RR(ready, quantum):
    running = []
    tmp = ready.copy()
    tmp = sorted(tmp, key=lambda x: x.name)
    n = len(ready)
    i = 0
    while (tmp != []):
        if tmp[i].tb > quantum:
            tmp[i].tb = tmp[i].tb - quantum
            running = running + quantum * [copy.copy(tmp[i])]
        else:
            running = running + tmp[i].tb * [copy.copy(tmp[i])]
            tmp[i].tb = 0
            del tmp[i]
            n = n-1
            i = i - 1
            if n == 0: break
        i = (i + 1) % n
    return running

#done and working
def priority_nonpre(ready):
    ready = sorted(ready, key=lambda x: x.priority)
    tmp = ready.copy()
    runtime = get_runtime(ready)
    running = []
    for i in range(runtime):
        tmp[0].tb = tmp[0].tb - 1
        running.append(copy.copy(tmp[0]))
        if tmp[0].tb == 0: del tmp[0]
    return running
#done and working
def priority_pre(ready):
    ready = sorted(ready, key=lambda x: x.ta)
    running = []
    tmp = []
    runtime = get_runtime(ready)
    for i in range(runtime):
        for x in ready:
            if (x.ta == i):
                tmp.append(copy.copy(x))
        tmp = sorted(tmp, key=lambda x: x.priority)
        tmp[0].tb = tmp[0].tb - 1
        tmp[0].tr = 1
        running.append(copy.copy(tmp[0]))
        if tmp[0].tb == 0: del tmp[0]

    return running

#done and working
def SJF(ready):
    ready = sorted(ready, key=lambda x: x.tb)
    tmp = ready.copy()
    runtime = get_runtime(ready)
    running = []
    for i in range(runtime):
        tmp[0].tb = tmp[0].tb - 1
        running.append(copy.copy(tmp[0]))
        if tmp[0].tb == 0: del tmp[0]
    return running

#done and working
def SRTF(ready):
    ready = sorted(ready, key=lambda x: x.ta)
    running = []
    tmp = []
    runtime = get_runtime(ready)
    for i in range(runtime):
        for x in ready:
            if (x.ta == i):
                tmp.append(copy.copy(x))
        tmp = sorted(tmp, key=lambda x: x.tb)
        tmp[0].tb = tmp[0].tb - 1
        tmp[0].tr = 1
        running.append(copy.copy(tmp[0]))
        if tmp[0].tb == 0: del tmp[0]

    return running

#waiting time = time of last beginning - CPU time before then - arrival time
def get_waitingtime(ready, running, runtime):
    p_list = sorted(ready, key=lambda x: x.name)
    waiting = 0
    n = len(ready)
    m = len(running)
    for i in range(n):
        last_start = runtime
        CPU_time = 0
        index = 0
        #get last_start
        for j in range(1,m+1):
            last_start = last_start - running[-j].tr
            if running[-j].name == p_list[i].name:
                index = m-j
                break
        #get CPU time before
        for j in range(index):
            if running[j].name == p_list[i].name: CPU_time = CPU_time + running[j].tr

        waiting = waiting + last_start - p_list[i].ta - CPU_time
    average_waiting = waiting/n
    return average_waiting
        


    avg_waiting = waiting / n
    return avg_waiting


def Reshape(running):
    tmp = running.copy()
    out = [copy.copy(tmp[0])]
    del tmp[0]
    while (tmp != []):
        if tmp[0].name==out[-1].name: out[-1].tr = out[-1].tr + 1
        else: out.append(copy.copy(tmp[0]))
        del tmp[0]
    return out

def Gantt(running, runtime, ready):
    running = Reshape(running)
    df = pd.DataFrame({"average\nwaiting\ntime = {t}".format(t=get_waitingtime(ready, running, runtime)) : [i.tr for i in running]}, index=[i.name for i in running])
    df = df.transpose()
    dp = df.plot(kind='barh', stacked=True, legend=True, xticks=range(runtime+1))

    dp.legend(ncol=len(ready))
    dp.grid(axis = 'x', linestyle='--', color = 'grey')
    plt.show()


def Calc(Tbs, Tas, Priorities, Qu, var):
    running = []
    ready = []
    tbs = Tbs.get()
    tbs = [int(i) for i in tbs.split()]
    tas = Tas.get()
    tas = [int(i) for i in tas.split()]
    priorities = Priorities.get()
    priorities = [int(i) for i in priorities.split()]
    quantum = Qu.get()
    if quantum != '': quantum = int(quantum)

    if (priorities == [] and tas == []): 
        for i in range(len(tbs)):
                ready.append(Process(0, tbs[i], "P{id}".format(id=i+1)))
    elif (priorities == []): 
        for i in range(len(tbs)):
                ready.append(Process(tas[i], tbs[i], "P{id}".format(id=i+1)))
    elif (tas == []): 
        for i in range(len(tbs)):
                ready.append(Process(0, tbs[i], "P{id}".format(id=i+1), priorities[i]))
    else: 
        for i in range(len(tbs)):
                ready.append(Process(tas[i], tbs[i], "P{id}".format(id=i+1), priorities[i]))

    runtime = get_runtime(ready)
    alg = var.get()
    if alg == 1: running = FCFS(ready)
    elif alg == 2: running = SRTF(ready)
    elif alg == 3: running = SJF(ready)
    elif alg == 4: running = priority_pre(ready)
    elif alg == 5: running = priority_nonpre(ready)
    else: running = RR(ready, quantum)

    running = Reshape(running)
    time = get_waitingtime(ready, running, runtime)
    Gantt(running, runtime, ready)



Tbs = tk.StringVar()
text_tb = tk.Label(root, text="Enter CPU burst times separated by a space, e.g. 1 10 4 5")
tbs = tk.Entry(root, textvariable=Tbs)

Tas = tk.StringVar()
text_ta = tk.Label(root, text="Enter arrival times separated by a space (for preemptive algorithms only)")
tas = tk.Entry(root, textvariable=Tas)

Priorities = tk.StringVar()
text_priority=tk.Label(root, text="Enter priority of tasks separated by a space (for priority algorithms only)")
priorities = tk.Entry(root, textvariable=Priorities)

Qu = tk.StringVar()
text_qu = tk.Label(root, text="Enter quantum (for RR only)")
qu = tk.Entry(root, textvariable=Qu)

var = tk.IntVar()
R1 = tk.Radiobutton(root, text="FCFS", variable=var, value=1)
R2 = tk.Radiobutton(root, text="SJF (Preemptive)", variable=var, value=2)
R3 = tk.Radiobutton(root, text="SJF (Non-preemptive)", variable=var, value=3)
R4 = tk.Radiobutton(root, text="Priority (Preemptive)", variable=var, value=4)
R5 = tk.Radiobutton(root, text="Priority (Non-preemptive)", variable=var, value=5)
R6 = tk.Radiobutton(root, text="Round Robin", variable=var, value=6)

B = tk.Button(root, text="Plot", command=lambda: Calc(Tbs, Tas, Priorities, Qu, var))


text_tb.pack()
tbs.pack()
R1.pack()
R2.pack()
R3.pack()
R4.pack()
R5.pack()
R6.pack()
text_ta.pack()
tas.pack()
text_priority.pack()
priorities.pack()
text_qu.pack()
qu.pack()
B.pack()
root.mainloop()