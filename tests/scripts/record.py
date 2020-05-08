import os
from pprint import pprint
from random import randint, random
from time import sleep

from pyaestro.utilities.executor import Executor, ExecTaskState

# Pathing
success = './tests/scripts/sleep.sh'
fail = './tests/scripts/fail.sh'
ws = './workspace'

# Configuration
j_min = 5    # seconds
j_max = 300  # seconds
fail_rate = 0.15
max_workers = 4
n = 30

# Setup
os.makedirs(ws, exist_ok=True)
executor = Executor(max_workers)
jobids = []

# Start processes
for i in range(0, n):
    p_fail = random()
    if p_fail > fail_rate:
        print("Running a success.")
        jobid = executor.submit(
            success, ws, str(randint(j_min, j_max)))
    else:
        print("Running a failure.")
        jobid = executor.submit(
            fail, ws, str(randint(j_min, j_max)))

    jobids.append(jobid)
    print("JOBID: ", jobid, " -- ", executor.get_status(jobid))
    print(f"{i}: Looping...")

pprint(dict(executor.get_all_status()))

for uuid, state in executor.get_all_status():
    if state == ExecTaskState.RUNNING:
        executor.cancel(uuid)

while True:
    print("Waiting...")
    print(executor.get_all_status())
    sleep(30)
