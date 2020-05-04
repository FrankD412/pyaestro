from pyaestro.utilities.executor import Executor
from time import sleep
from random import randint

if __name__ == "__main__":
    script = '/mnt/f/Code/Python/pyaestro/tests/scripts/sleep.sh'
    ws = '/mnt/f/Code/Python/pyaestro/tests/scripts'
    n = 30

    executor = Executor(4)
    jobid = []

    for i in range(0, n):
        jobid.append(executor.submit(script, ws, str(randint(5, 100))))
        print("JOBID: ", jobid[i], " -- ", executor.get_status(jobid[i]))
        print(f"{i}: Looping...")
        

    while True:
        print("Waiting...")
        print(executor.get_all_status())
        sleep(30)